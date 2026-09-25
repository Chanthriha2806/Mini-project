# 🎯 MASTER CLAUDE PROMPT FOR REVIEW II PPT GENERATION

Copy and paste the prompt below directly into **Claude**:

---

```text
Act as a Senior Computer Science Academic Reviewer and Presentation Designer. I have an upcoming Mini Project Review II presentation tomorrow for my MCA program at KGiSL Institute of Information Management (Department of Computer Science).

I am uploading my Review 1 presentation template file ("REVIEW 1 - AI INFRASTRUCTURE MONITORING DASHBOARD .pptx"). 

Please generate a complete 13-slide PowerPoint presentation (or python-pptx / SVG slide deck) for Review II that uses my exact template theme, headers, footers ("AI INFRASTRUCTURE MONITORING DASHBOARD"), font styles, and color scheme.

---

### STUDENT & PROJECT DETAILS:
- Project Title: AI-Enabled IT Infrastructure Monitoring Dashboard
- Student Name: CHANTHRIHA J
- Register No: 2538M0070
- Guide Name: Mrs. R. GOMATHI
- Institution: KGiSL Institute of Information Management (KGiSL-IIM), Coimbatore
- Department: Department of Computer Science (ODD Semester 2026-2027)

---

### MANDATORY REVIEW II COMPONENTS TO INCLUDE (SLIDE-BY-SLIDE):

SLIDE 1: TITLE SLIDE
- Header: KGiSL INSTITUTE OF INFORMATION MANAGEMENT | DEPARTMENT OF COMPUTER SCIENCE
- Title: AI-ENABLED IT INFRASTRUCTURE MONITORING DASHBOARD
- Subtitle: MINI PROJECT REVIEW II PRESENTATION
- Student Info: CHANTHRIHA J (Reg No: 2538M0070)
- Guide Info: Under the Guidance of Mrs. R. GOMATHI

SLIDE 2: AGENDA / CONTENT
- 1. Module Description
- 2. Data Flow Diagram (DFD Level 0 Context Diagram)
- 3. Data Flow Diagram (DFD Level 1 Macro Flow)
- 4. Data Flow Diagram (DFD Level 2 Sub-Processes)
- 5. Table Design (Relational Database Schemas)
- 6. Input Design (Forms & Control Interfaces)
- 7. Output Design (Dashboards, Alerts & Reports)
- 8. System Requirements & Conclusion

SLIDE 3: COMPONENT 1 - MODULE DESCRIPTION
Break down into 5 clean structured boxes:
1. User Authentication Module (auth_controller.py): Registration, login, PBKDF2-SHA256 hashing, Flask-Login session management.
2. Telemetry Acquisition Module (system_monitor.py & client_agent.py): psutil local sensor & remote client JSON agent reporting.
3. Threshold Audit & Alert Module (dashboard_controller.py & mail_helper.py): Threshold comparison, ACTIVE alert logging, async SMTP emails.
4. AI Recommendation Module (ai_engine.py): Rule-based expert decision system for hardware troubleshooting recommendations.
5. Reporting & Process Control Module (reports_controller.py & report_generator.py): Admin PID process killing, PDF ReportLab & Excel openpyxl exports.

SLIDE 4: COMPONENT 2 - DATA FLOW DIAGRAM (DFD LEVEL 0 CONTEXT DIAGRAM)
Draw a clean, neat visual box diagram:
- External Entities (Rectangles): [USER / ADMIN], [REMOTE CLIENT AGENT], [HOST HARDWARE], [ADMIN DASHBOARD], [SMTP MAIL GATEWAY], [MYSQL DB].
- Central Process (Circle/Rounded Box): (0.0 AI-ENABLED IT INFRASTRUCTURE MONITORING SYSTEM)
- Directional Arrows & Data Flow Labels:
  - User -> Process: "Login Credentials / Queries"
  - Process -> User: "Session State / Telemetry Response"
  - Client Agent -> Process: "JSON Telemetry Payload (HTTP POST)"
  - Host Hardware -> Process: "Raw Metrics (psutil API)"
  - Process -> Admin Dashboard: "Live Charts & Alert Feeds"
  - Process -> SMTP Gateway: "Threshold Breach Email Alerts"
  - Process <-> MySQL DB: "SQL Logs & Time-Series History"

SLIDE 5: COMPONENT 2 - DATA FLOW DIAGRAM (DFD LEVEL 1 MACRO PROCESS FLOW)
Draw a neat visual flow diagram connecting 5 processes with Data Stores:
- Process 1.0 (User Authentication) <---> Data Store [D1: users]
- Process 2.0 (Metric Collection & Ingestion) <---> Data Store [D2: monitoring_history]
- Process 3.0 (Threshold Auditing & Alerting) <---> Data Stores [D3: settings] & [D4: alerts] ---> External Entity [SMTP Mail]
- Process 4.0 (AI Diagnostics Engine) ---> Evaluates Rule Matrix
- Process 5.0 (Visualization & Process Control) ---> [Chart.js Dashboard] & [PDF/Excel Reports]

SLIDE 6: COMPONENT 2 - DATA FLOW DIAGRAM (DFD LEVEL 2 SUB-PROCESSES)
Draw 2 distinct sub-process flow columns:
- Column A (Process 3.0 Threshold Auditing):
  3.1 Read Thresholds (D3: settings) -> 3.2 Compare Metric Values -> 3.3 Create ACTIVE Alert (D4: alerts) -> 3.4 Dispatch SMTP Email.
- Column B (Process 4.0 AI Recommendation Engine):
  4.1 Multi-Variable Rule Audit -> 4.2 Identify Root Causes (Memory leak, CPU saturation, Storage depletion) -> 4.3 Formulate Action Steps -> 4.4 Render AI Advice Banners.

SLIDE 7: COMPONENT 3 - TABLE DESIGN (DATABASE SCHEMAS - PART 1)
Structured schema boxes for:
1. `users`: id (INT, PK, AI), username (VARCHAR 50, UNQ), email (VARCHAR 120, UNQ), password_hash (VARCHAR 255), is_admin (BOOL), created_at (TIMESTAMP).
2. `settings`: id (INT, PK, AI), user_id (INT, FK -> users.id, UNQ), cpu_threshold (FLOAT), ram_threshold (FLOAT), disk_threshold (FLOAT), refresh_interval (INT), email_address (VARCHAR 120).

SLIDE 8: COMPONENT 3 - TABLE DESIGN (DATABASE SCHEMAS - PART 2)
Structured schema boxes for:
3. `monitoring_history`: id (INT, PK), user_id (INT, FK), hostname (VARCHAR 100), cpu_usage (FLOAT), ram_usage (FLOAT), disk_usage (FLOAT), upload_speed (FLOAT), download_speed (FLOAT), created_at (TIMESTAMP).
4. `alerts`: id (INT, PK), metric_type (VARCHAR 20), message (VARCHAR 255), value (FLOAT), threshold (FLOAT), status (VARCHAR 20), created_at (TIMESTAMP).
5. `reports`: id (INT, PK), report_type (VARCHAR 20), file_path (VARCHAR 255), created_at (TIMESTAMP).

SLIDE 9: COMPONENT 4 - INPUT DESIGN (FORMS & CONTROLS)
Clean bulleted card blocks:
- Auth Forms (login.html): Textbox (Username/Email), Password field, client-side required validation, server-side PBKDF2 hash check.
- Settings Form (settings.html): HTML5 Range Sliders (1-100% CPU/RAM/Disk), Refresh rate input, Alert Email box.
- Remote Client Agent Payload (POST /api/metrics/report): HTTP REST API JSON schema for CPU, Memory, Disk, Network speeds.
- AI Assistant Chat Input: Natural-language query text input box with sanitization.
- Process Termination Action: PID integer input button with system process protection.

SLIDE 10: COMPONENT 5 - OUTPUT DESIGN (DASHBOARDS & ALERTS)
Visual output cards:
- Real-Time Metric Cards & Gauges: Circular progress rings & percentage badges (5s live refresh).
- Interactive Chart.js Graphs: Multi-line time-series graphs for CPU %, RAM %, Disk % trend lines.
- Active Alert Feed Panel: Color-coded red/warning warning banners triggered on threshold breach.

SLIDE 11: COMPONENT 5 - OUTPUT DESIGN (AI DIAGNOSTICS & REPORTS)
Visual output cards:
- AI Diagnostic Banners: Root cause diagnostics & step-by-step corrective action steps.
- Top Processes Table: Sortable PID list with single-click "Kill Process" action button.
- Exported Audit Reports: Downloadable PDF diagnostic summaries (ReportLab) & Excel spreadsheets (openpyxl).

SLIDE 12: SYSTEM REQUIREMENTS
Hardware: Intel i3/i5 Processor, 4GB/8GB RAM, 10GB Storage, 64-bit OS.
Software: Windows 10/11, HTML5/CSS3/Bootstrap 5/JavaScript/Chart.js, Python 3.12 Flask, MySQL/SQLite database, psutil sensor.

SLIDE 13: CONCLUSION & REVIEW II VERIFICATION
Summary of Review II completion, supervisor approval readiness, and future ML/mobile roadmap.

---

Please output the complete presentation code or python-pptx script that updates my uploaded PPTX template directly, creating clean visual DFD boxes and arrows.
```
