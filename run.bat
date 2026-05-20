@echo off
echo ========================================
echo   TIOBE IMPORTER - Запуск системы
echo ========================================
echo.

:menu
echo Выберите действие:
echo 1. Обновить данные из источников
echo 2. Запустить веб-интерфейс
echo 3. Тестовый режим (демо-данные)
echo 4. Запустить по расписанию
echo 5. Тест поиска
echo 6. Тест источников данных
echo 7. Добавить все источники (расширенные + русские)
echo 8. Выход
echo.

set /p choice="Введите номер (1-8): "

if "%choice%"=="1" goto update
if "%choice%"=="2" goto web
if "%choice%"=="3" goto test
if "%choice%"=="4" goto schedule
if "%choice%"=="5" goto test_search
if "%choice%"=="6" goto test_sources
if "%choice%"=="7" goto add_sources
if "%choice%"=="8" goto end

echo Неверный выбор!
goto menu

:update
echo.
echo Обновление данных...
python main.py update
pause
goto menu

:web
echo.
echo Запуск веб-интерфейса...
echo Откройте http://localhost:5000 в браузере
python web_dashboard.py
pause
goto menu

:test
echo.
echo Тестовый режим...
python main.py test
pause
goto menu

:schedule
echo.
echo Запуск по расписанию...
python main.py schedule
pause
goto menu

:test_search
echo.
echo Тест поиска...
python ontology_search.py
pause
goto menu

:test_sources
echo.
echo Тест источников данных...
python extended_data_sources.py
pause
goto menu

:add_sources
echo.
echo Добавление всех источников...
python add_all_sources.py
pause
goto menu

:end
echo Выход...
exit

