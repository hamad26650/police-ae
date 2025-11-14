@echo off
title تشغيل موقع الخدمات الحكومية
echo ============================================
echo       تشغيل موقع الخدمات الحكومية
echo ============================================
echo.
cd /d "%~dp0"
"..\gov_services_env\Scripts\python.exe" manage.py runserver
pause


