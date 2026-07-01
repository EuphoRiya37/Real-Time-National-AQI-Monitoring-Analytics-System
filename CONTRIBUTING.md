# Contributing to Real-Time AQI Monitoring System

Thank you for helping improve air quality monitoring!

## Setup for Development

### 1. Clone and Setup

```bash
git clone https://github.com/EuphoRiya37/Real-Time-National-AQI-Monitoring-Analytics-System.git
cd Real-Time-AQI-System
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

### 4. Database Setup

```bash
mysql -u root -p < schema.sql
```

## What to Work On

- Add new data sources / APIs
- Improve AQI calculation accuracy
- Enhance forecasting algorithms
- Add visualization dashboards
- Optimize database queries
- Add unit tests
- Improve documentation
- Add geographic mapping
- Implement alert system
- Performance optimization

## Before Submitting

- Test with live data
- Run tests: `pytest tests/`
- Check code style: `pylint src/`
- Update documentation
- Verify database migrations work
- Test alert notifications

## Reporting Issues

When reporting bugs:
- Describe the issue clearly
- Include error messages
- Mention your Python version
- Share sample data if relevant
- Specify which API source failed

## Questions?

Open an issue or discussion in the repository!

---

**License:** MIT + Commons Clause (see LICENSE file)
