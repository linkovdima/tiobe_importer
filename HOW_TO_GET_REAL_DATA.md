# Как получить реальные данные из источников

## Быстрый старт

### 1. Обновление данных из всех источников

```bash
python main.py update
```

Это обновит данные из:
- ✅ TIOBE Index
- ✅ GitHub API
- ✅ Stack Overflow API
- ✅ PYPL (если доступно)
- ✅ RedMonk (если доступно)
- ✅ IEEE Spectrum (если доступно)

### 2. Тестирование расширенных источников

```bash
python extended_data_sources.py
```

Это протестирует все доступные источники данных.

## Настройка источников данных

### GitHub API (рекомендуется)

1. Создайте токен на https://github.com/settings/tokens
2. Добавьте в `github_config.py`:
   ```python
   GITHUB_TOKEN = "ваш_токен_здесь"
   ```

**Преимущества с токеном:**
- 5000 запросов/час вместо 60
- Доступ к приватным репозиториям (если нужно)
- Более стабильная работа

### Stack Overflow API

**Не требует настройки** - публичный API, но есть лимиты:
- 300 запросов/день
- 30 запросов/секунду

## Источники данных и их доступность

### ✅ Всегда доступны (API)

| Источник | Тип | Требования | Лимиты |
|----------|-----|------------|--------|
| GitHub API | REST API | Токен (опционально) | 60-5000/час |
| Stack Overflow API | REST API | Нет | 300/день |
| npm Registry | REST API | Нет | Нет |

### ⚠️ Могут требовать обновления парсеров (HTML парсинг)

| Источник | Тип | Стабильность | Примечания |
|----------|-----|--------------|------------|
| TIOBE Index | HTML парсинг | Средняя | Структура может меняться |
| PYPL | HTML парсинг | Высокая | Стабильная структура |
| RedMonk | HTML парсинг | Средняя | Блог формат |
| IEEE Spectrum | HTML парсинг | Средняя | Может меняться |
| GitHub Trending | HTML парсинг | Высокая | Стабильная структура |
| PyPI Stats | HTML парсинг | Средняя | Может меняться |
| Rosetta Code | HTML парсинг | Высокая | Стабильная структура |

## Использование в коде

### Базовый пример

```python
from extended_data_sources import ExtendedDataSources

fetcher = ExtendedDataSources()

# Получить все данные для Python
all_data = fetcher.get_all_sources_data("Python")
print(all_data)
```

### Получение конкретных данных

```python
# PYPL рейтинг
pypl = fetcher.get_pypl_data()
print(f"Топ-5 языков PYPL: {pypl[:5]}")

# GitHub Trending
trending = fetcher.get_github_trending("Python", timeframe="weekly")
print(f"Трендовые репозитории: {trending}")

# Статистика пакетов
pypi_stats = fetcher.get_pypi_stats("Python")
print(f"Всего пакетов PyPI: {pypi_stats['total_packages']}")
```

### Интеграция с системой обновления

```python
from data_sources_manager import DataSourcesManager
from ontology_manager import OntologyManager

om = OntologyManager()
dsm = DataSourcesManager(om)

# Обновить с расширенными источниками
results = dsm.update_all_sources(use_extended_sources=True)

# Обновить только основные источники
results = dsm.update_all_sources(use_extended_sources=False)
```

## Решение проблем

### Проблема: Rate limit превышен

**Решение:**
- Для GitHub: добавьте токен в `github_config.py`
- Для Stack Overflow: увеличьте паузы между запросами
- Используйте кэширование результатов

### Проблема: Парсинг не работает

**Причины:**
- Структура HTML изменилась
- Сайт недоступен
- Блокировка по IP

**Решение:**
- Проверьте доступность сайта вручную
- Обновите селекторы в парсере
- Используйте fallback на демо-данные

### Проблема: Данные не обновляются

**Проверьте:**
1. Интернет соединение
2. Доступность источников
3. Логи ошибок в консоли
4. Правильность путей к файлам

## Рекомендации

1. **Регулярное обновление**: Обновляйте данные еженедельно или ежемесячно
2. **Мониторинг**: Следите за логами обновлений
3. **Резервные копии**: Сохраняйте предыдущие версии онтологии
4. **Тестирование**: Тестируйте источники перед массовым обновлением
5. **Кэширование**: Кэшируйте результаты для уменьшения запросов

## Альтернативные подходы

### Использование готовых датасетов

Если парсинг не работает, можно использовать готовые датасеты:
- Kaggle datasets по языкам программирования
- GitHub Awesome списки
- Open Data порталы

### Создание собственных скриптов

Для специфических источников создайте собственные скрипты:
```python
# custom_source.py
def get_custom_data():
    # Ваш код получения данных
    pass
```

## Дополнительные ресурсы

- [GitHub API Documentation](https://docs.github.com/en/rest)
- [Stack Overflow API Documentation](https://api.stackoverflow.com/docs)
- [TIOBE Index](https://www.tiobe.com/tiobe-index/)
- [PYPL](https://pypl.github.io/PYPL.html)
- [RedMonk](https://redmonk.com)

## Поддержка

Если источник данных перестал работать:
1. Проверьте доступность сайта
2. Обновите парсер под новую структуру
3. Используйте альтернативные источники
4. Создайте issue в репозитории проекта

