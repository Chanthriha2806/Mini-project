@echo off
title MonitorAI Public Cloud Tunnel Launcher
echo ====================================================
echo         MonitorAI Live Public Server Launcher
echo ====================================================
echo.
echo [1/2] Starting Flask Application Server on port 5000...
start /b py run.py > server.log 2>&1
timeout /t 3 /nobreak > nul

echo.
echo [2/2] Connecting to Public Gateway Tunnel...
echo.
echo ===================================================================
echo  SHARE THE PUBLIC HTTPS LINK BELOW WITH YOUR FRIEND / CLIENTS:
echo ===================================================================
echo.
ssh -o StrictHostKeyChecking=no -R 80:localhost:5000 nokey@localhost.run
pause
