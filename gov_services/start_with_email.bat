@echo off
chcp 65001 >nul
title Run Site with Email Settings
echo ============================================
echo    Starting Site with Email Settings
echo ============================================
echo.
echo Email: Project.test85@outlook.com
echo.

set EMAIL_HOST_USER=Project.test85@outlook.com
set EMAIL_HOST_PASSWORD=hamad26650

cd /d "%~dp0"
echo Starting server...
echo.
"..\gov_services_env\Scripts\python.exe" manage.py runserver

pause
