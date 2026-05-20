# Быстрый старт

## 🚀 Быстрый запуск (3 шага)

### Шаг 1: Установка зависимостей
```bash
pip install -r requirements.txt
```

### Шаг 2: Обновление данных (первый раз)
```bash
python main.py update
```

### Шаг 3: Запуск веб-интерфейса
```bash
python web_dashboard.py
```

Откройте в браузере: **http://localhost:5000/search**

## 📋 Альтернативный запуск (Windows)

Используйте файл `run.bat` для интерактивного меню:
```bash
run.bat
```

## 📋 Альтернативный запуск (Linux/Mac)

Сделайте файл исполняемым и запустите:
```bash
chmod +x run.sh
./run.sh
```

## 🌐 Веб-интерфейс

После запуска `python web_dashboard.py` доступны:
- Главная страница: http://localhost:5000
- Поиск: http://localhost:5000/search
- Дашборд: http://localhost:5000/dashboard
- Список языков: http://localhost:5000/languages

## 🔄 Обновление данных

### Однократное обновление
```bash
python main.py update
```

### Обновление по расписанию
```bash
python main.py schedule
```

### Тестовый режим (демо-данные)
```bash
python main.py test
```

## Тестирование поиска

```bash
python ontology_search.py
```

## Тестирование получения данных

```bash
python improved_data_fetcher.py
```

## Структура проекта

- `ontology_search.py` - модуль поиска по онтологии
- `improved_data_fetcher.py` - получение реальных данных
- `web_dashboard.py` - веб-интерфейс и API
- `main.py` - основной модуль обновления данных
- `data/programming_languages.ttl` - онтология

## Настройка GitHub токена

Создайте файл `github_config.py`:
```python
GITHUB_TOKEN = "ваш_токен_здесь"
```

Токен можно получить на: https://github.com/settings/tokens

