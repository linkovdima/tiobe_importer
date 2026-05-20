@echo off
chcp 65001 >nul
echo ========================================
echo   ОБНОВЛЕНИЕ ИСТОЧНИКОВ
echo ========================================
echo.
python extended_sources.py
echo.
python add_russian_sources.py
echo.
echo ========================================
echo   ОБНОВЛЕНИЕ ЗАВЕРШЕНО
echo ========================================
pause

