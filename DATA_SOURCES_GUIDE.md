# Руководство по источникам данных

## Обзор источников данных

Система поддерживает получение данных из множества реальных источников для языков программирования.

## Основные источники рейтингов

### 1. TIOBE Index
- **URL**: https://www.tiobe.com/tiobe-index/
- **Тип**: Парсинг HTML
- **Данные**: Рейтинг популярности языков (1-20)
- **Обновление**: Ежемесячно
- **Метод**: `get_tiobe_data_real()` в `improved_data_fetcher.py`

### 2. PYPL (PopularitY of Programming Language)
- **URL**: https://pypl.github.io/PYPL.html
- **Тип**: Парсинг HTML
- **Данные**: Рейтинг на основе поисковых запросов учебных материалов
- **Обновление**: Регулярно
- **Метод**: `get_pypl_data()` в `extended_data_sources.py`

### 3. RedMonk Rankings
- **URL**: https://redmonk.com/sogrady/category/programming-languages/
- **Тип**: Парсинг HTML блога
- **Данные**: Комбинированный рейтинг GitHub + Stack Overflow
- **Обновление**: Дважды в год
- **Метод**: `get_redmonk_data()` в `extended_data_sources.py`

### 4. IEEE Spectrum Top Programming Languages
- **URL**: https://spectrum.ieee.org/top-programming-languages/
- **Тип**: Парсинг HTML
- **Данные**: Комплексный рейтинг на основе множества метрик
- **Обновление**: Ежегодно
- **Метод**: `get_ieee_spectrum_data()` в `extended_data_sources.py`

## API источники

### 5. GitHub API
- **URL**: https://api.github.com
- **Тип**: REST API
- **Данные**: 
  - Количество репозиториев
  - Количество звезд
  - Топ репозитории
- **Требования**: Токен (опционально, увеличивает лимит)
- **Метод**: `get_github_data_real()` в `improved_data_fetcher.py`
- **Лимиты**: 
  - Без токена: 60 запросов/час
  - С токеном: 5000 запросов/час

### 6. Stack Overflow API
- **URL**: https://api.stackexchange.com
- **Тип**: REST API
- **Данные**: 
  - Количество вопросов по тегам
  - Статистика использования
- **Требования**: Нет (публичный API)
- **Метод**: `get_stackoverflow_data_real()` в `improved_data_fetcher.py`
- **Лимиты**: 300 запросов/день

### 7. GitHub Trending
- **URL**: https://github.com/trending
- **Тип**: Парсинг HTML
- **Данные**: Трендовые репозитории по языкам
- **Обновление**: Ежедневно/еженедельно/ежемесячно
- **Метод**: `get_github_trending()` в `extended_data_sources.py`

## Статистика пакетных менеджеров

### 8. npm (Node Package Manager)
- **URL**: https://registry.npmjs.org
- **Тип**: REST API
- **Данные**: Количество пакетов для JavaScript/TypeScript
- **Метод**: `get_npm_stats()` в `extended_data_sources.py`

### 9. PyPI (Python Package Index)
- **URL**: https://pypi.org
- **Тип**: Парсинг HTML статистики
- **Данные**: Количество пакетов для Python
- **Метод**: `get_pypi_stats()` в `extended_data_sources.py`

## Дополнительные источники

### 10. Rosetta Code
- **URL**: https://rosettacode.org
- **Тип**: Парсинг HTML
- **Данные**: Количество примеров кода/задач
- **Метод**: `get_rosetta_code_stats()` в `extended_data_sources.py`

### 11. Google Trends
- **URL**: https://trends.google.com
- **Тип**: API (требует библиотеку pytrends)
- **Данные**: Популярность поисковых запросов
- **Статус**: Частично реализовано (требует доработки)
- **Метод**: `get_google_trends_info()` в `extended_data_sources.py`

### 12. Wikipedia
- **URL**: https://en.wikipedia.org
- **Тип**: Парсинг HTML
- **Данные**: Общая информация о языках
- **Метод**: `get_wikipedia_data()` в `improved_data_fetcher.py`

## Использование

### Базовое использование

```python
from extended_data_sources import ExtendedDataSources

fetcher = ExtendedDataSources()

# Получить данные из всех источников для языка
all_data = fetcher.get_all_sources_data("Python")
print(all_data)
```

### Получение данных из конкретного источника

```python
# PYPL данные
pypl_data = fetcher.get_pypl_data()

# RedMonk данные
redmonk_data = fetcher.get_redmonk_data()

# IEEE Spectrum данные
ieee_data = fetcher.get_ieee_spectrum_data()

# GitHub Trending
trending = fetcher.get_github_trending("Python", timeframe="weekly")

# Статистика пакетов
pypi_stats = fetcher.get_pypi_stats("Python")
npm_stats = fetcher.get_npm_stats("JavaScript")
```

## Интеграция с онтологией

Данные из всех источников можно интегрировать в онтологию через `data_sources_manager.py`:

```python
from data_sources_manager import DataSourcesManager
from ontology_manager import OntologyManager

om = OntologyManager()
dsm = DataSourcesManager(om)

# Обновить данные из всех источников
results = dsm.update_all_sources()
```

## Рекомендации по использованию

1. **Rate Limits**: Уважайте лимиты API (особенно GitHub и Stack Overflow)
2. **Кэширование**: Кэшируйте результаты для уменьшения запросов
3. **Обработка ошибок**: Всегда используйте try/except и fallback на демо-данные
4. **Паузы**: Делайте паузы между запросами (особенно для парсинга)
5. **User-Agent**: Используйте корректный User-Agent для парсинга

## Расширение источников

Для добавления нового источника:

1. Создайте метод в `ExtendedDataSources` или `ImprovedDataFetcher`
2. Реализуйте парсинг/API запросы
3. Нормализуйте данные к стандартному формату
4. Добавьте обработку ошибок
5. Интегрируйте в `get_all_sources_data()`

## Потенциальные дополнительные источники

- **JetBrains Developer Ecosystem Survey** - опросы разработчиков
- **Stack Overflow Developer Survey** - ежегодный опрос
- **GitHub Octoverse** - ежегодный отчет GitHub
- **Indeed/LinkedIn** - статистика вакансий
- **HackerRank** - статистика по языкам
- **Codeforces/LeetCode** - статистика использования языков в соревнованиях

## Примечания

- Некоторые источники могут изменять структуру HTML, что требует обновления парсеров
- API могут изменять форматы ответов
- Рекомендуется регулярно проверять работоспособность источников
- Для production использования рассмотрите использование официальных API где возможно

