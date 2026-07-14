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
set /p SERVER_URL="Enter Server URL (e.g. https://mini-project-phi-green.vercel.app or http://172.16.53.70:5000): "
set /p USERNAME="Enter your Username: "
set /p PASSWORD="Enter your Password: "
echo.
echo [*] Connecting to %SERVER_URL%...
py client_agent.py %SERVER_URL% %USERNAME% %PASSWORD%
echo.
echo [ERROR] Agent terminated. Please verify connection credentials and URL.
pause
