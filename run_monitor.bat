@echo off
title MonitorAI Startup Launcher
echo ====================================================
echo           MonitorAI Auto-Launcher
echo ====================================================
echo.
echo [1/3] Starting Dashboard Web Server...
start "MonitorAI Web Server" py run.py

echo.
echo [2/3] Waiting for boot-up...
timeout /t 3 /nobreak >nul

echo.
echo [3/3] Launching Local Telemetry Agent...
start "MonitorAI Client Agent" py client_agent.py

echo.
echo ====================================================
echo [SUCCESS] MonitorAI is running!
echo Dashboard: http://127.0.0.1:5000
echo Credentials:
echo   - Admin Role:  admin / admin123
echo   - Client Role: client / client123
echo ====================================================
echo.
echo (Press any key to close this launcher. The dashboard and agent will continue to run in the background).
pause >nul
