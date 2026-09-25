# Presentation Slide Deck Outline (10-Slide Blueprint)

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
