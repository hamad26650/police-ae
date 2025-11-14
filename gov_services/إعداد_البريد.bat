@echo off
chcp 65001 >nul
title Email Setup
cd /d "%~dp0"
echo ============================================
echo    Email Configuration Setup
echo ============================================
echo.
"..\gov_services_env\Scripts\python.exe" إعداد_حقيقي.py
pause

