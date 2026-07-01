import os
import requests
import mysql.connector
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 1. API Configuration (from environment variables — see .env.example)
API_KEY = os.environ.get('AQI_API_KEY')
RESOURCE_ID = os.environ.get('AQI_RESOURCE_ID', '3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69')
URL = f"https://api.data.gov.in/resource/{RESOURCE_ID}?api-key={API_KEY}&format=json&limit=500"

# 2. Database Connection
try:
    db = mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_NAME', 'AirQualityDB')
    )
    cursor = db.cursor()
    print("Successfully connected to MySQL database.")
except mysql.connector.Error as err:
    print(f"Database Connection Error: {err}")
    exit()


def get_aqi_category(value):
    """Fulfills the 'AQI_Category' Derived Attribute from ER diagram"""
    val = float(value)
    if val <= 50: return 'Good'
    elif val <= 100: return 'Satisfactory'
    elif val <= 200: return 'Moderate'
    elif val <= 300: return 'Poor'
    else: return 'Very Poor'


def fetch_and_store():
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    headers = {'User-Agent': 'Mozilla/5.0'}

    print("Requesting live data from data.gov.in...")
    try:
        response = session.get(URL, headers=headers, timeout=20)
        data = response.json()
    except Exception as e:
        print(f"API Request failed: {e}")
        return

    records_count = 0
    for record in data['records']:
        station_id = record.get('station', 'Unknown')
        val = record.get('pollutant_avg') or record.get('avg_value') or 0
        p_id = record.get('pollutant_id', 'NA')
        last_update = record.get('last_update')

        # ER Match: STATION (Composite Location split into Lat/Lon)
        cursor.execute("""
            INSERT IGNORE INTO Station (Station_ID, Name, Latitude, Longitude) 
            VALUES (%s, %s, %s, %s)
        """, (station_id, station_id, record.get('latitude'), record.get('longitude')))

        if last_update:
            try:
                ts = datetime.strptime(last_update, '%d-%m-%Y %H:%M:%S')

                # ER Match: Calculate Derived Attribute
                category = get_aqi_category(val)

                # ER Match: READING Weak Entity (Key: Station_ID + Timestamp)
                cursor.execute("""
                    INSERT IGNORE INTO Reading (Station_ID, Timestamp, Value, AQI_Category)
                    VALUES (%s, %s, %s, %s)
                """, (station_id, ts, val, category))

                # ER Match: Relationship 'Contains' and Attribute 'Is_High'
                is_high = 1 if float(val) > 100 else 0
                cursor.execute("""
                    INSERT IGNORE INTO Reading_Pollutants (Station_ID, Timestamp, P_Code, Is_High)
                    VALUES (%s, %s, %s, %s)
                """, (station_id, ts, p_id, is_high))

                records_count += 1
            except:
                continue

    db.commit()
    print(f"Successfully synced {records_count} records to AirQualityDB!")


if __name__ == "__main__":
    fetch_and_store()
    cursor.close()
    db.close()
