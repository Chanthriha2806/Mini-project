# Viva & Project Review Q&A Defense Guide

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
