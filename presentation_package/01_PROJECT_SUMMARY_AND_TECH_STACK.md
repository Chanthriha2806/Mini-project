# Executive Summary & Technology Stack

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
