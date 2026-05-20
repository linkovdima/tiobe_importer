# Как добавить источники в онтологию

## Быстрый старт

### Вариант 1: Автоматический сбор (самый простой)

```bash
python add_sources.py
```

Выберите:
1. Автоматическое добавление для языка
2. Ручное добавление источника  
3. Добавить источники для всех языков

**Рекомендуется:** Выберите вариант 3 для автоматического заполнения всех языков.

### Вариант 2: Для конкретного языка

```bash
python add_sources.py
# Выберите 1
# Введите язык: Python
```

## Что добавляется автоматически

### Для каждого языка система находит:

1. **📚 Популярные книги** (3-5 книг)
   - Известные учебники и справочники
   - С ISBN и авторами

2. **📖 Официальная документация** (2-3 ссылки)
   - Официальные сайты документации
   - Справочники API

3. **📄 Статьи из Wikipedia** (до 10)
   - Источники из секции "Further reading"
   - Внешние ссылки

4. **⭐ GitHub Awesome списки** (до 10)
   - Популярные списки ресурсов
   - Ссылки из README файлов

## Ручное добавление

### Через скрипт

```bash
python add_sources.py
# Выберите 2
```

Следуйте инструкциям для ввода данных.

### Через Python код

```python
from publication_manager import PublicationManager

pm = PublicationManager()

# Книга
pm.add_book(
    title="Название книги",
    language="Python",
    author="Автор",
    isbn="978-...",
    url="https://...",
    keywords="ключевые, слова",
    year=2024,
    difficulty="Advanced"
)

# Статья
pm.add_article(
    title="Название статьи",
    language="Python",
    url="https://...",
    keywords="ключевые слова"
)

# Документация
pm.add_documentation(
    title="Официальная документация",
    language="Python",
    url="https://docs.python.org/"
)

# Туториал
pm.add_tutorial(
    title="Название туториала",
    language="Python",
    url="https://...",
    difficulty="Beginner"
)

# Сохранить
pm.save_ontology()
```

## Проверка добавленных источников

```python
from publication_manager import PublicationManager

pm = PublicationManager()
publications = pm.get_publications_for_language("Python")

print(f"Найдено {len(publications)} источников:")
for pub in publications:
    print(f"  [{pub['type']}] {pub['title']}")
    if pub['url']:
        print(f"    URL: {pub['url']}")
```

## Примеры реальных источников

### Python

**Книги:**
- Fluent Python (Luciano Ramalho)
- Python Tricks (Dan Bader)
- Effective Python (Brett Slatkin)

**Документация:**
- https://docs.python.org/3/
- https://www.python.org/about/gettingstarted/

**Статьи:**
- MDN Python Guide
- Real Python articles

### Java

**Книги:**
- Effective Java (Joshua Bloch)
- Java: The Complete Reference

**Документация:**
- https://docs.oracle.com/javase/
- https://docs.oracle.com/java/

### JavaScript

**Книги:**
- You Don't Know JS (Kyle Simpson)
- Eloquent JavaScript

**Документация:**
- https://developer.mozilla.org/en-US/docs/Web/JavaScript
- https://javascript.info/

## Рекомендации

1. **Начните с автоматического сбора** - это быстро заполнит базу
2. **Добавляйте качественные источники** - проверяйте актуальность
3. **Используйте ключевые слова** - улучшает поиск
4. **Указывайте уровень сложности** - Beginner/Intermediate/Advanced
5. **Регулярно обновляйте** - добавляйте новые источники

## Структура данных

Каждый источник связан с языком через свойство `aboutLanguage` и может иметь:
- Название (title)
- URL (url)
- Автора (writtenBy)
- Ключевые слова (keywords)
- Описание (description)
- Уровень сложности (hasDifficulty)

## После добавления

Источники автоматически становятся доступными:
- В поиске по онтологии
- В результатах поиска по ключевым словам
- При запросе информации о языке

## Дополнительная информация

См. `SOURCES_GUIDE.md` для полного руководства.

