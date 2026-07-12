-- MySQL Schema Script for AI-Enabled IT Infrastructure Monitoring Dashboard
-- Database: `it_monitor_db`

CREATE DATABASE IF NOT EXISTS `it_monitor_db`;
USE `it_monitor_db`;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `email` VARCHAR(120) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Settings Table
CREATE TABLE IF NOT EXISTS `settings` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT UNIQUE NOT NULL,
    `cpu_threshold` FLOAT NOT NULL DEFAULT 90.0,
    `ram_threshold` FLOAT NOT NULL DEFAULT 90.0,
    `disk_threshold` FLOAT NOT NULL DEFAULT 95.0,
    `refresh_interval` INT NOT NULL DEFAULT 5,
    `email_address` VARCHAR(120),
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Alerts Table
CREATE TABLE IF NOT EXISTS `alerts` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `metric_type` VARCHAR(20) NOT NULL, -- 'CPU', 'RAM', 'DISK'
    `message` VARCHAR(255) NOT NULL,
    `value` FLOAT NOT NULL,
    `threshold` FLOAT NOT NULL,
    `status` VARCHAR(20) NOT NULL DEFAULT 'ACTIVE', -- 'ACTIVE', 'RESOLVED'
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Monitoring History Table (Time-Series Metric Logs)
CREATE TABLE IF NOT EXISTS `monitoring_history` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `cpu_usage` FLOAT NOT NULL,
    `ram_usage` FLOAT NOT NULL,
    `disk_usage` FLOAT NOT NULL,
    `upload_speed` FLOAT NOT NULL,
    `download_speed` FLOAT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Reports Table
CREATE TABLE IF NOT EXISTS `reports` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `report_type` VARCHAR(20) NOT NULL, -- 'DAILY', 'WEEKLY', 'MONTHLY'
    `file_path` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
