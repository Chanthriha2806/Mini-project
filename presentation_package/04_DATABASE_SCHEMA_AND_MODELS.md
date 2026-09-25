# Database Schema & Entity Relationship

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
