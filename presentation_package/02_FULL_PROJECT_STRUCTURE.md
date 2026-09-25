# Comprehensive Project Directory Structure

```text
E:\MINI PROJECT 2├── app/                                  # Core Application Package (MVC Architecture)
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
