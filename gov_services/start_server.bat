@echo off
cd /d "%~dp0"
start "Django Server" /D "%~dp0" "..\gov_services_env\Scripts\python.exe" manage.py runserver
echo.
echo الموقع يعمل الآن على: http://127.0.0.1:8000/
echo تم فتح نافذة جديدة للخادم
echo.
timeout /t 3

