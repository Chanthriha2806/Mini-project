import os
import zipfile

presentation_dir = r"e:\Mini project 2\presentation_package"
os.makedirs(presentation_dir, exist_ok=True)

# 1. Executive Summary & Tech Stack
file1_content = """# Executive Summary & Technology Stack

## 1. Project Overview
- **Project Title**: AI-Enabled IT Infrastructure Monitoring Dashboard (MonitorAI)
- **Domain**: Cloud Computing, System Administration, MCA Mini Project / Software Engineering
- **Objective**: To provide real-time hardware telemetry monitoring, alert notification on threshold breaches, automated diagnostic troubleshooting recommendations using a rule-based AI engine, and comprehensive PDF/Excel auditing reports for IT administrators and remote servers.

---

## 2. Key Problem Statement & Solution
- **Problem**: Traditional server monitoring tools are either overly complex, lack real-time visual analytics, or require manual intervention to diagnose root causes when CPU, RAM, or Disk spikes occur.
- **Solution**: MonitorAI provides a full-stack dashboard featuring real-time client metric agent polling (psutil + HTTP API), dynamic multi-chart dashboard rendering (Chart.js), threshold breach detection with automatic email alerts, an AI-powered diagnostic engine providing causes and corrective actions, and single-click PDF/Excel report exports.

---

## 3. Technology Stack & Frameworks

| Tier | Technologies / Libraries | Function & Role |
| :--- | :--- | :--- |
| **Backend Framework** | Python 3.12, Flask | Web app server, REST API routing, session management |
| **Database & ORM** | MySQL, SQLAlchemy, PyMySQL | Relational storage for telemetry logs, user profiles, alert feeds, and settings |
| **Authentication & Mail** | Flask-Login, Flask-Mail | User authentication, session persistence, SMTP alert notification emails |
| **Hardware Telemetry** | `psutil`, `socket`, `platform` | Cross-platform OS metrics collection (CPU, Memory, Disk, Network I/O, Processes) |
| **AI Diagnostic Engine** | Custom Rule-Based Engine | Expert decision rules evaluating system telemetry against critical thresholds |
| **Frontend UI/UX** | HTML5, CSS3, Bootstrap 5, FontAwesome | Modern, dark-themed responsive dashboard interface |
| **Data Visualization** | Chart.js | Real-time multi-metric line and bar charts with dynamic live polling |
| **Reporting & Export** | ReportLab (PDF), openpyxl (Excel) | Automated compilation of infrastructure health reports |
| **Deployment & Build** | PyInstaller (`MonitorAI.spec`) | Standalone Windows EXE compilation capability |
"""

# 2. Full Project Structure
file2_content = """# Comprehensive Project Directory Structure

```text
E:\MINI PROJECT 2\
├── app/                                  # Core Application Package (MVC Architecture)
│   ├── __init__.py                       # Application Factory, Flask extensions & Auto-seeding
│   ├── controllers/                      # Business Logic Layer (Controllers)
│   │   ├── auth_controller.py            # Handles user registration, login verification, hashing
│   │   ├── dashboard_controller.py       # Metrics aggregation, alert checks, AI chat & process management
│   │   ├── monitor_controller.py         # Hardware detailed specs & system diagnostics logic
│   │   ├── reports_controller.py         # Handles PDF & Excel report generation queries
│   │   └── settings_controller.py        # Manages user threshold configuration updates
│   ├── models/                           # Database Schema Layer (SQLAlchemy ORM Models)
│   │   ├── __init__.py                   # Model exports
│   │   ├── user.py                       # User entity (id, username, email, password_hash, is_admin)
│   │   ├── setting.py                    # User thresholds (cpu_threshold, ram_threshold, disk_threshold, email)
│   │   ├── alert.py                      # Alert log entity (metric_type, message, value, threshold, status)
│   │   ├── monitoring.py                 # Time-series telemetry history log entity
│   │   └── report.py                     # Exported report registry entity
│   ├── routes/                           # Presentation / Route Blueprint Layer
│   │   ├── auth_routes.py                # Endpoints: /auth/login, /auth/register, /auth/logout
│   │   ├── dashboard_routes.py           # Endpoints: /, /api/metrics, /api/charts, /api/metrics/report, /api/ai/chat
│   │   ├── monitor_routes.py             # Endpoints: /monitor/specs, /monitor/api/details
│   │   ├── reports_routes.py             # Endpoints: /reports/, /reports/generate, /reports/download
│   │   └── settings_routes.py            # Endpoints: /settings/, /settings/update
│   ├── static/                           # Public Web Assets
│   │   ├── css/                          # Custom stylesheet styling & Bootstrap extensions
│   │   ├── js/                           # Dynamic frontend JavaScript (dashboard.js, Chart.js logic)
│   │   ├── downloads/                    # Generated instruction PDFs and guides
│   │   └── reports/                      # Generated PDF & Excel diagnostic reports storage
│   ├── templates/                        # Jinja2 HTML View Templates
│   │   ├── auth/                         # Authentication templates (login.html, register.html)
│   │   ├── base.html                     # Master layout page with navigation bar and footer
│   │   ├── dashboard.html                # Main monitoring dashboard UI with dynamic charts & AI modal
│   │   ├── monitor.html                  # Detailed hardware specs & active processes table
│   │   ├── profile.html                  # User profile details template
│   │   ├── reports.html                  # Report generation & download center template
│   │   └── settings.html                 # Threshold & notification configuration template
│   └── utilities/                        # Core Utility Libraries & Service Modules
│       ├── ai_engine.py                  # RecommendationEngine (Rule-based diagnostic expert system)
│       ├── mail_helper.py                # SMTP Email alert sender helper
│       ├── report_generator.py           # ReportLab PDF & openpyxl Excel document builders
│       └── system_monitor.py             # Local host hardware telemetry reader (psutil wrapper)
├── tests/                                # Test Suite Package
│   ├── __init__.py                       # Test package initializer
│   └── test_monitoring.py                # Unit tests for system monitor & alert threshold logic
├── client_agent.py                       # Standalone Python agent for monitoring remote client computers
├── config.py                             # Configuration management (Development, Production, Database URIs)
├── run.py                                # Application entry point (Starts server & launches browser)
├── schema.sql                            # Raw SQL DDL schema script for MySQL setup
├── requirements.txt                      # Project dependency list
├── MonitorAI.spec                        # PyInstaller specification file for EXE compilation
├── build_exe.py                          # Automated executable build script
├── create_db.py                          # Database creation script helper
└── initialize_database.py               # Database table initializer & seed script
```
"""

# 3. End to End Workflow
file3_content = """# End-to-End System Workflow & Architecture

## 1. System Execution Flow (First to Last)

```mermaid
sequenceDiagram
    autonumber
    actor User/Admin
    participant Browser as Web Frontend (Chart.js)
    participant Agent as Client Agent (psutil)
    participant Flask as Flask Server (run.py / Controllers)
    participant AI as AI Engine (ai_engine.py)
    participant DB as MySQL / SQLite Database
    participant Email as SMTP Mail Server

    Note over User/Admin, Flask: 1. System Boot & Initialization
    Flask->>DB: create_app() -> Auto-create tables & seed Default Admin / Settings
    User/Admin->>Flask: Navigate to http://localhost:5000/auth/login
    Flask-->>User/Admin: Authenticate Session & Render Dashboard

    Note over Agent, Flask: 2. Remote / Local Telemetry Gathering
    alt Local Server Mode
        Flask->>Flask: SystemMonitor.get_system_metrics() via psutil
    else Remote Client Agent Mode
        Agent->>Agent: psutil metrics capture (CPU, RAM, Disk, Net Speeds)
        Agent->>Flask: POST /api/metrics/report (JSON Telemetry Payload)
    end

    Note over Flask, DB: 3. Health Audit & Data Persistence
    Flask->>DB: Save metrics entry into monitoring_history table
    Flask->>Flask: Evaluate metrics against User Thresholds (CPU/RAM/Disk)
    
    opt Threshold Exceeded
        Flask->>DB: Insert ACTIVE alert entry into alerts table
        Flask->>Email: Trigger Async Alert Email to Administrator
    end

    Note over Flask, AI: 4. AI Recommendation & Frontend Update
    Flask->>AI: RecommendationEngine.generate_recommendations()
    AI-->>Flask: Returns diagnostic causes & corrective actions
    Browser->>Flask: Poll GET /api/metrics & GET /api/charts (Every 5s)
    Flask-->>Browser: JSON payload with live data, alerts, AI advice & charts

    Note over User/Admin, Flask: 5. Report Generation & Process Management
    User/Admin->>Flask: Request PDF/Excel Audit Report
    Flask->>Flask: ReportGenerator builds PDF/Excel file
    Flask-->>User/Admin: Downloadable file link provided
```

---

## 2. Core Subsystems Breakdown

### Step 1: Telemetry Collection Subsystem (`system_monitor.py` / `client_agent.py`)
- Reads CPU usage percentage, core count, frequency.
- Reads RAM total, used, available, and percentage.
- Reads Disk volume total, free, used, and percentage.
- Dynamically computes real-time Network upload/download speeds in KB/s using socket/net_io deltas.
- Extracts process list (Top 10 CPU/RAM consuming tasks with PID, process name, username).

### Step 2: Ingestion & Threshold Audit Subsystem (`dashboard_controller.py`)
- Receives telemetry via REST API or local fetch.
- Saves time-series records to `monitoring_history`.
- Compares metrics against user thresholds (e.g., CPU > 90%, RAM > 90%, Disk > 95%).
- Automatically triggers database alert creation (`Alert` model) and dispatches email notifications (`mail_helper.py`).

### Step 3: AI Diagnostic Engine Subsystem (`ai_engine.py`)
- Rule-based expert system evaluating multiple telemetry variables simultaneously.
- Identifies critical situations like **CPU Core Saturation**, **Physical RAM Depletion**, **Storage Depletion**, and **High Network Upload/Download Throughput**.
- Formulates root causes (e.g., memory leaks, unauthorized cryptomining, log accumulation) and actionable corrective steps.

### Step 4: Real-time UI Rendering Subsystem (`dashboard.html` / `dashboard.js`)
- Uses asynchronous polling (`setInterval` every 5 seconds) via Fetch API.
- Dynamically updates gauges, stat cards, alert feeds, and Chart.js time-series charts without full page refreshes.

### Step 5: Auditing & Reporting Subsystem (`report_generator.py`)
- Compiles custom-range telemetry statistics (mean, max, peak values).
- Generates formatted PDF documents using ReportLab Flowables.
- Generates structured Excel spreadsheets using openpyxl.
"""

# 4. Database Schema
file4_content = """# Database Schema & Entity Relationship

## Database Architecture
The application supports both **MySQL** (for production environments) and **SQLite** (for portable local deployment). It uses SQLAlchemy ORM for object mapping.

---

## Entity Relationship Diagram (ERD)

```text
  +------------------+         1 : 1          +-------------------+
  |      users       |<---------------------->|     settings      |
  +------------------+                        +-------------------+
  | PK  id           |                        | PK  id            |
  |     username     |                        | FK  user_id       |
  |     email        |                        |     cpu_threshold |
  |     password_hash|                        |     ram_threshold |
  |     created_at   |                        |     disk_threshold|
  +------------------+                        |     email_address |
          |                                   +-------------------+
          | 1 : N
          v
  +------------------+
  |monitoring_history|
  +------------------+
  | PK  id           |
  | FK  user_id      |
  |     hostname     |
  |     cpu_usage    |
  |     ram_usage    |
  |     disk_usage   |
  |     upload_speed |
  |     download_speed|
  |     created_at   |
  +------------------+

  +------------------+                        +-------------------+
  |      alerts      |                        |      reports      |
  +------------------+                        +-------------------+
  | PK  id           |                        | PK  id            |
  |     metric_type  |                        |     report_type   |
  |     message      |                        |     file_path     |
  |     value        |                        |     created_at    |
  |     threshold    |                        +-------------------+
  |     status       |
  |     created_at   |
  +------------------+
```

---

## Detailed Table Definitions

### 1. `users` Table
Stores user account authentication credentials.
- `id` (INT, Primary Key, Auto Increment)
- `username` (VARCHAR(50), Unique, Not Null)
- `email` (VARCHAR(120), Unique, Not Null)
- `password_hash` (VARCHAR(255), Not Null)
- `is_admin` (BOOLEAN, Default False)
- `created_at` (TIMESTAMP, Default Current Timestamp)

### 2. `settings` Table
Stores user-configurable health thresholds.
- `id` (INT, Primary Key, Auto Increment)
- `user_id` (INT, Foreign Key -> `users.id`, Unique)
- `cpu_threshold` (FLOAT, Default 90.0)
- `ram_threshold` (FLOAT, Default 90.0)
- `disk_threshold` (FLOAT, Default 95.0)
- `refresh_interval` (INT, Default 5)
- `email_address` (VARCHAR(120))

### 3. `alerts` Table
Logs system health threshold violations.
- `id` (INT, Primary Key, Auto Increment)
- `metric_type` (VARCHAR(20)) -- 'CPU', 'RAM', 'DISK'
- `message` (VARCHAR(255))
- `value` (FLOAT)
- `threshold` (FLOAT)
- `status` (VARCHAR(20), Default 'ACTIVE') -- 'ACTIVE', 'RESOLVED'
- `created_at` (TIMESTAMP)

### 4. `monitoring_history` Table
Time-series log of all reported system telemetry readings.
- `id` (INT, Primary Key, Auto Increment)
- `user_id` (INT, Foreign Key -> `users.id`, Nullable)
- `hostname` (VARCHAR(100))
- `cpu_usage` (FLOAT)
- `ram_usage` (FLOAT)
- `disk_usage` (FLOAT)
- `upload_speed` (FLOAT)
- `download_speed` (FLOAT)
- `created_at` (TIMESTAMP)

### 5. `reports` Table
Registry of generated diagnostic PDF and Excel export files.
- `id` (INT, Primary Key, Auto Increment)
- `report_type` (VARCHAR(20)) -- 'DAILY', 'WEEKLY', 'MONTHLY'
- `file_path` (VARCHAR(255))
- `created_at` (TIMESTAMP)
"""

# 5. AI Engine Algorithms
file5_content = """# AI Recommendation Engine & Diagnostic Algorithms

## 1. Engine Design Philosophy
The `RecommendationEngine` class (`app/utilities/ai_engine.py`) implements a rule-based expert system. Unlike black-box ML models that require high training data overhead, an expert rule engine provides **deterministic, instant, and zero-latency** hardware troubleshooting recommendations suitable for real-time infrastructure auditing.

---

## 2. Rule Evaluation Matrix

| Metric Category | Trigger Condition | Severity Level | Diagnostic Causes | Corrective Action Steps |
| :--- | :--- | :--- | :--- | :--- |
| **CPU Core** | `cpu > 90%` | **DANGER (Critical)** | Runaway process thread, OS indexer loop, malware/cryptomining | Terminate high CPU PID, restart server, scan for malware |
| **CPU Core** | `75% < cpu <= 90%` | **WARNING** | Multiple dev environments open, background updates | Close unused apps, defer compiler builds to off-peak hours |
| **RAM Memory** | `ram > 90%` | **DANGER (Critical)** | Memory leaks in daemon processes, excessive VM buffers | Kill memory hogging PID, flush standby lists, upgrade physical RAM |
| **RAM Memory** | `75% < ram <= 90%` | **WARNING** | High count of background services, browser tab inflation | Audit memory footprints, disable non-essential startup services |
| **Disk Storage** | `disk > 95%` | **DANGER (Critical)** | Raw log accumulation, full recycle bin, crash dump buildup | Run Disk Cleanup, purge temp/Docker containers, empty recycle bin |
| **Disk Storage** | `80% < disk <= 95%` | **WARNING** | Standard workspace growth, npm/pip package cache inflation | Clear packet manager caches, transfer large archives to NAS |
| **Network Upload** | `upload > 10MB/s` | **INFO** | Background cloud sync, p2p seeding, potential data exfiltration | Pause cloud folder sync, inspect `netstat` socket connections |
| **Network Download** | `download > 20MB/s` | **INFO** | Large installer download, heavy media streaming, DB replication | Verify download safety, apply bandwidth throttling during work hours |
| **Overall Health** | Threshold breach | **CRITICAL / WARNING** | Hardware threshold violated | Check Alerts feed, review hardware specs, verify cooling system |

---

## 3. Context-Aware AI Chat Assistant (`chat_with_ai`)
In addition to automated diagnostics, the system features an AI Chat endpoint (`/api/ai/chat`) that parses natural language questions from administrators alongside the live metrics context to deliver tailored troubleshooting suggestions.
"""

# 6. Slide Deck Outline
file6_content = """# Presentation Slide Deck Outline (10-Slide Blueprint)

Use this slide blueprint to create your slides or input into Claude to generate your presentation slides.

---

### Slide 1: Title Slide
- **Title**: AI-Enabled IT Infrastructure Monitoring Dashboard
- **Subtitle**: Real-Time Hardware Telemetry, Smart AI Troubleshooting & Automated Auditing
- **Presenter**: MCA Mini Project Review
- **Key Visual**: Server node icon with dynamic metric gauges

---

### Slide 2: Problem Statement & Objectives
- **Key Challenges in IT Monitoring**:
  - High complexity of conventional monitoring tools.
  - Lack of real-time proactive alert mechanisms.
  - Absence of integrated automated root-cause troubleshooting recommendations.
- **Project Objectives**:
  - Build a responsive, multi-tier monitoring solution for local and remote computers.
  - Provide automated rule-based AI troubleshooting recommendations.
  - Enable single-click PDF & Excel compliance audit exports.

---

### Slide 3: Technology Architecture & Stack
- **Backend**: Python 3.12, Flask, Flask-SQLAlchemy, Flask-Login, Flask-Mail
- **Database**: MySQL / SQLite relational storage with time-series history
- **Frontend**: HTML5, Bootstrap 5 (Dark Theme), Dynamic Chart.js visualizations
- **Telemetry Sensor**: Cross-platform `psutil` integration
- **Architecture Pattern**: Model-View-Controller (MVC)

---

### Slide 4: System Architecture & Workflow
- **End-to-End Flow**:
  1. Client Agent / Local Sensor captures live CPU, RAM, Disk & Network speeds.
  2. Telemetry reported via REST API (`/api/metrics/report`).
  3. Controller performs threshold audit against configured settings.
  4. Active alert logged in DB + Instant SMTP email sent on breach.
  5. Recommendation Engine formulates diagnostic advice for the UI.

---

### Slide 5: Core Features & User Capabilities
- **Real-Time Dynamic Dashboard**: Live line charts and progress rings updated every 5 seconds.
- **Remote Client Agent (`client_agent.py`)**: Standalone script allowing centralized admin oversight across remote network nodes.
- **Process Management**: Top 10 CPU/RAM consumer table with admin process termination (`kill`) capability.
- **Customizable Thresholds**: User-configurable warning triggers and email notification preferences.

---

### Slide 6: Rule-Based AI Recommendation Engine
- **Concept**: Deterministic, zero-latency diagnostic expert system.
- **Multi-Factor Analysis**: Evaluates combined states (e.g., high CPU + high RAM vs high Disk).
- **Output Structure**:
  - **Diagnostic Causes**: Identifies probable root causes (e.g., memory leak, cryptomining loop).
  - **Corrective Actions**: Provides immediate step-by-step remediation advice.

---

### Slide 7: Database Design & Schema
- **Entities & Tables**:
  - `users`: User authentication & admin roles.
  - `settings`: Threshold settings & notification preferences.
  - `monitoring_history`: Time-series hardware metric logs.
  - `alerts`: Active and resolved violation logs.
  - `reports`: Audit report file registry.

---

### Slide 8: Auditing & Report Generation
- **Supported Formats**: Professional PDF (ReportLab) & Excel (openpyxl).
- **Content Highlights**:
  - Telemetry averages and peak values.
  - Complete historical alerts log table.
  - Date-range filtering (Daily, Weekly, Monthly).

---

### Slide 9: Demonstration & Test Results
- **Testing Scenarios**:
  - Simulated high CPU/RAM utilization threshold breaches.
  - Instant SMTP Email alert delivery confirmation.
  - Standalone Client Agent remote reporting verification.
  - Executable EXE packaging using PyInstaller.

---

### Slide 10: Conclusion & Future Enhancements
- **Summary**: Delivered a production-ready, full-stack IT infrastructure monitoring dashboard with AI recommendations.
- **Future Work**:
  - Machine Learning predictive failure analysis (LSTM time-series forecasting).
  - Multi-tenant cloud agent deployment with SNMP/Docker support.
  - Mobile app push notification integration.
"""

# 7. Q&A Defense Guide
file7_content = """# Viva & Project Review Q&A Defense Guide

### Q1: Why did you choose a Rule-Based AI Engine instead of Machine Learning models?
**Answer**:
"For real-time infrastructure hardware monitoring, deterministic expert rule engines offer zero-latency execution, 100% explainability, and zero training data overhead. Standard ML models require vast historical failure datasets and can introduce black-box ambiguity. Our rule-based AI engine immediately maps metric anomalies to proven IT troubleshooting protocols without delay."

---

### Q2: How does the application handle real-time metric updates without refreshing the browser page?
**Answer**:
"The frontend uses asynchronous Fetch API polling (`setInterval` running every 5 seconds in `dashboard.js`). It queries the `/api/metrics` and `/api/charts` endpoints. The server responds with JSON payloads containing current metrics, which Chart.js and dynamic DOM manipulators render smoothly without full page reloads."

---

### Q3: How do remote client nodes communicate telemetry to the central server?
**Answer**:
"We implemented a standalone Python script called `client_agent.py`. It runs on remote client machines, uses `psutil` to collect hardware metrics, authenticates via session cookies, and sends JSON telemetry payloads to the server's `/api/metrics/report` HTTP POST endpoint every 5 seconds."

---

### Q4: What database architecture is used, and how is historical data tracked?
**Answer**:
"We use MySQL (or SQLite) managed via Flask-SQLAlchemy. The `monitoring_history` table stores time-series metric snapshots (CPU, RAM, Disk, Upload/Download speeds, timestamp, user_id, hostname). This historical data is queried to plot line charts and calculate mean/peak stats for PDF and Excel audit reports."

---

### Q5: How are alerts and notifications handled when a metric exceeds a threshold?
**Answer**:
"When telemetry is received, `dashboard_controller.py` compares the values against user thresholds stored in the `settings` table. If a value breaches the limit (e.g. CPU > 90%), an entry is inserted into the `alerts` table with state `ACTIVE`, and an email notification is dispatched asynchronously via Flask-Mail to the admin's registered email address."

---

### Q6: Can administrators kill runaway processes directly from the dashboard?
**Answer**:
"Yes. The system extracts top CPU/RAM consuming tasks via `psutil.process_iter()`. Administrators can click the 'Kill' button next to any process on the UI, which sends a POST request to `/api/process/kill`. The server verifies admin privileges and terminates the targeted PID using `psutil.Process(pid).terminate()`."
"""

files_to_write = {
    "01_PROJECT_SUMMARY_AND_TECH_STACK.md": file1_content,
    "02_FULL_PROJECT_STRUCTURE.md": file2_content,
    "03_END_TO_END_WORKFLOW_AND_ARCHITECTURE.md": file3_content,
    "04_DATABASE_SCHEMA_AND_MODELS.md": file4_content,
    "05_AI_ENGINE_AND_ALGORITHMS.md": file5_content,
    "06_PRESENTATION_SLIDE_DECK_OUTLINE.md": file6_content,
    "07_Q_AND_A_DEFENSE_GUIDE.md": file7_content,
}

for fname, content in files_to_write.items():
    filepath = os.path.join(presentation_dir, fname)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {filepath}")

# Create Zip Archive in workspace root
zip_path = r"e:\Mini project 2\MonitorAI_Project_Presentation_Package.zip"
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for fname in files_to_write.keys():
        filepath = os.path.join(presentation_dir, fname)
        zipf.write(filepath, arcname=os.path.join("presentation_package", fname))

print(f"\nSuccessfully packaged zip archive at: {zip_path}")
