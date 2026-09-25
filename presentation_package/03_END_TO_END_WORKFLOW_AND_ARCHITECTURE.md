# End-to-End System Workflow & Architecture

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
