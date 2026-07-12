# AI-Enabled IT Infrastructure Monitoring Dashboard

This is a production-ready, full-stack MCA Mini Project built using Python (Flask), SQLAlchemy, PyMySQL, and Chart.js to monitor server/computer metrics in real time. It features rule-based AI recommendations, thresholds settings, email notifications, MySQL-backed alerting, and downloadable PDF/Excel reports.

## Technology Stack

- **Backend**: Python 3.12, Flask, Flask-SQLAlchemy, Flask-Login, Flask-Mail, PyMySQL, psutil
- **Frontend**: HTML5, CSS3, Bootstrap 5, Chart.js, Font Awesome
- **Database**: MySQL (using PyMySQL connector)
- **Architecture**: MVC (Model-View-Controller)

## Directory Structure

```text
E:\Mini project 2\
├── run.py                 # Application entry point
├── config.py              # Application settings & credentials
├── requirements.txt       # Python dependencies
├── README.md              # Documentation
├── app/                   # Core application package
│   ├── __init__.py        # App Factory & extensions initializations
│   ├── models/            # SQLAlchemy Database Models (User, Alert, Settings, MonitoringHistory)
│   ├── controllers/       # Controller logic (Auth, Dashboard, Monitor, Settings, Reports)
│   ├── routes/            # Blueprint routes definition
│   ├── templates/         # Jinja2 templates (Login, Register, Dashboard, Settings, etc.)
│   ├── static/            # Static assets (css/style.css, js/main.js, images/)
│   └── utilities/         # Monitoring agent, AI recommendation engine, and mail helpers
```

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Database**:
   - Ensure a MySQL server is running locally.
   - Create a database named `it_monitor_db`.
   - Update config variables in `config.py` if needed.

3. **Run the Application**:
   ```bash
   python run.py
   ```
   Open `http://localhost:5000` in your web browser.
