# Semantic programming library (TIOBE importer)

Веб-приложение семантической электронной библиотеки по языкам программирования: RDF-онтология, семантический поиск, личный кабинет, дашборд с метриками TIOBE / GitHub / Stack Overflow.

## Возможности

- Каталог языков и публикаций на основе онтологии (`data/programming_languages.ttl`)
- Семантический поиск по ключевым словам (SPARQL + ранжирование)
- Сохранение внешних источников и фактов в RDF
- Личный кабинет (папки, закладки, экспорт BibTeX)
- Аналитический дашборд (диаграммы TIOBE и GitHub)
- Импорт рейтингов TIOBE и обновление метрик из внешних API

## Требования

- Python 3.9+
- Зависимости из `requirements.txt`

## Установка

```bash
git clone https://github.com/linkovdima/tiobe_importer.git
cd tiobe_importer
pip install -r requirements.txt
```

### GitHub API (опционально)

Для обновления метрик GitHub задайте токен одним из способов:

```bash
# Windows PowerShell
$env:GITHUB_TOKEN = "ghp_..."

# или скопируйте пример
copy github_config.example.py github_config.py
# и впишите токен в github_config.py (файл в .gitignore)
```

## Запуск

**Веб-интерфейс** (основной режим):

```bash
python web_dashboard.py
```

Откройте в браузере: http://127.0.0.1:5000

Путь к онтологии по умолчанию: `data/programming_languages.ttl`. Переопределение:

```bash
set ONTOLOGY_PATH=C:\path\to\programming_languages.ttl
```

**Меню Windows** (`run.bat`): обновление данных, веб, тесты.

**Обновление данных из источников:**

```bash
python main.py update
```

## Тесты

```bash
python -m pytest tests/ -v
```

Smoke-тесты проверяют основные HTTP-маршруты и JSON API.

## Структура проекта

```
tiobe_importer/
├── web_dashboard.py      # Flask-приложение и REST API
├── ontology_search.py    # Семантический поиск
├── ontology_manager.py   # Загрузка/сохранение RDF (скрипты)
├── publication_manager.py
├── cabinet_storage.py    # SQLite — личный кабинет
├── data/
│   └── programming_languages.ttl
├── templates/            # HTML-шаблоны
├── tests/
└── scripts/              # Вспомогательные скрипты (замеры и т.п.)
```

## Основные маршруты

| Маршрут | Назначение |
|---------|------------|
| `/` | Главная |
| `/languages` | Список языков |
| `/search` | Семантический поиск |
| `/dashboard` | Дашборд |
| `/cabinet` | Личный кабинет |
| `GET /api/languages` | JSON — языки |
| `POST /api/search` | JSON — поиск (`keywords` в теле) |

## Лицензия

Учебный / дипломный проект. Используйте и дорабатывайте по согласованию с автором.

## Автор

[linkovdima](https://github.com/linkovdima)
