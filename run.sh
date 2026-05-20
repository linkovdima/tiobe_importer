#!/bin/bash

echo "========================================"
echo "  TIOBE IMPORTER - Запуск системы"
echo "========================================"
echo ""

show_menu() {
    echo "Выберите действие:"
    echo "1. Обновить данные из источников"
    echo "2. Запустить веб-интерфейс"
    echo "3. Тестовый режим (демо-данные)"
    echo "4. Запустить по расписанию"
    echo "5. Тест поиска"
    echo "6. Тест источников данных"
    echo "7. Выход"
    echo ""
}

while true; do
    show_menu
    read -p "Введите номер (1-7): " choice
    
    case $choice in
        1)
            echo ""
            echo "Обновление данных..."
            python main.py update
            read -p "Нажмите Enter для продолжения..."
            ;;
        2)
            echo ""
            echo "Запуск веб-интерфейса..."
            echo "Откройте http://localhost:5000 в браузере"
            python web_dashboard.py
            read -p "Нажмите Enter для продолжения..."
            ;;
        3)
            echo ""
            echo "Тестовый режим..."
            python main.py test
            read -p "Нажмите Enter для продолжения..."
            ;;
        4)
            echo ""
            echo "Запуск по расписанию..."
            python main.py schedule
            read -p "Нажмите Enter для продолжения..."
            ;;
        5)
            echo ""
            echo "Тест поиска..."
            python ontology_search.py
            read -p "Нажмите Enter для продолжения..."
            ;;
        6)
            echo ""
            echo "Тест источников данных..."
            python extended_data_sources.py
            read -p "Нажмите Enter для продолжения..."
            ;;
        7)
            echo "Выход..."
            exit 0
            ;;
        *)
            echo "Неверный выбор!"
            ;;
    esac
done

