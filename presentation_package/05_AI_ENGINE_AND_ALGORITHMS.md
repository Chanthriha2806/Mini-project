# AI Recommendation Engine & Diagnostic Algorithms

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
