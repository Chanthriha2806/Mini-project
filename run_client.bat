@echo off
title MonitorAI Client Launcher
echo ====================================================
echo         MonitorAI Client Telemetry Launcher
echo ====================================================
echo.
echo [1/2] Installing required python libraries (psutil, requests)...
py -m pip install -r requirements.txt
echo.
echo [2/2] Connecting to Dashboard Web Server...
set /p SERVER_IP="Enter Server IP (e.g. 172.16.53.70): "
set /p USERNAME="Enter your Username: "
set /p PASSWORD="Enter your Password: "
echo.
echo [*] Connecting to http://%SERVER_IP%:5000...
py client_agent.py http://%SERVER_IP%:5000 %USERNAME% %PASSWORD%
echo.
echo [ERROR] Agent terminated. Please verify connection credentials and IP address.
pause
