# Real-Time National AQI Monitoring & Analytics System

Real-time ingestion, monitoring, and analytics system for live Air Quality Index (AQI)
data from authorized Indian government data feeds (data.gov.in), stored and processed
in a relational database.

## What it does
- Pulls live AQI readings from government API feeds across India
- Derives AQI category (Good / Satisfactory / Moderate / Poor / Very Poor) per reading
- Stores station, reading, and pollutant data in a normalized MySQL schema
- Flags high-pollutant readings via a derived `Is_High` attribute

## Setup
1. Copy `env.example` to `.env` and fill in your own values
2. Install dependencies: `pip install requests mysql-connector-python python-dotenv`
3. Run: `python aqi_sync.py`

## Schema
Built around a `Station` → `Reading` → `Reading_Pollutants` relational structure
(see ER diagram references in code comments).

## Tech stack
Python, MySQL, data.gov.in API
