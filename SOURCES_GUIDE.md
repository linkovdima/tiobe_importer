# Руководство по добавлению источников в онтологию

## Обзор

Система позволяет добавлять различные источники информации о языках программирования:
- 📚 **Книги** - учебники, справочники, руководства
- 📄 **Статьи** - блог-посты, научные статьи, обзоры
- 📖 **Документация** - официальная документация, справочники
- 🎓 **Туториалы** - обучающие материалы, курсы

## Способы добавления источников

### 1. Автоматический сбор (рекомендуется)

Система автоматически находит источники из различных мест:

```bash
python add_sources.py
```

Выберите:
1. Автоматическое добавление для языка
2. Ручное добавление источника
3. Добавить источники для всех языков

**Что ищет система:**
- Популярные книги по языку
- Официальную документацию
- Источники из Wikipedia
- Awesome списки на GitHub
- Статьи и туториалы

### 2. Ручное добавление через скрипт

```bash
python add_sources.py
```

Выберите режим "2. Ручное добавление источника" и следуйте инструкциям.

### 3. Программное добавление

```python
from publication_manager import PublicationManager

pm = PublicationManager()

# Добавить книгу
pm.add_book(
    title="Fluent Python",
    language="Python",
    author="Luciano Ramalho",
    isbn="978-1491946008",
    keywords="advanced, pythonic, best practices",
    url="https://www.oreilly.com/library/view/fluent-python/9781491946237/",
    year=2015,
    difficulty="Advanced"
)

# Добавить статью
pm.add_article(
    title="Python Type Hints",
    language="Python",
    url="https://docs.python.org/3/library/typing.html",
    keywords="type hints, typing"
)

# Сохранить
pm.save_ontology()
```

### 4. Веб-интерфейс (в разработке)

Откройте http://localhost:5000/sources после запуска веб-сервера.

## Структура источников в онтологии

### Книга (Book)
- `title` - название книги
- `aboutLanguage` - язык программирования
- `writtenBy` - автор
- `isbn` - ISBN
- `keywords` - ключевые слова
- `description` - описание
- `url` - ссылка на книгу
- `yearCreated` - год издания
- `hasDifficulty` - уровень сложности

### Статья (Article)
- `title` - название статьи
- `aboutLanguage` - язык программирования
- `url` - URL статьи
- `writtenBy` - автор
- `keywords` - ключевые слова
- `description` - описание
- `doi` - DOI статьи
- `publicationDate` - дата публикации

### Документация (Documentation)
- `title` - название документации
- `aboutLanguage` - язык программирования
- `url` - URL документации
- `description` - описание

### Туториал (Tutorial)
- `title` - название туториала
- `aboutLanguage` - язык программирования
- `url` - URL туториала
- `hasDifficulty` - уровень сложности
- `keywords` - ключевые слова

## Примеры использования

### Добавление книги для Python

```python
from publication_manager import PublicationManager

pm = PublicationManager()
pm.add_book(
    title="Python Tricks: The Book",
    language="Python",
    author="Dan Bader",
    isbn="978-1775093305",
    keywords="python tricks, best practices, advanced",
    url="https://realpython.com/products/python-tricks-book/",
    year=2017,
    difficulty="Intermediate"
)
pm.save_ontology()
```

### Добавление официальной документации

```python
pm.add_documentation(
    title="Python 3 Official Documentation",
    language="Python",
    url="https://docs.python.org/3/",
    description="Complete Python 3 documentation"
)
pm.save_ontology()
```

### Массовое добавление для всех языков

```bash
python add_sources.py
# Выберите вариант 3
```

## Автоматический сбор источников

Система ищет источники в:

1. **Популярные книги** - предопределенный список известных книг
2. **Официальная документация** - известные официальные сайты
3. **Wikipedia** - секции "Further reading" и "References"
4. **GitHub Awesome списки** - популярные списки ресурсов
5. **Официальные сайты** - ссылки из инфобоксов Wikipedia

## Проверка добавленных источников

```python
from publication_manager import PublicationManager

pm = PublicationManager()
publications = pm.get_publications_for_language("Python")

for pub in publications:
    print(f"[{pub['type']}] {pub['title']}")
    if pub['url']:
        print(f"  URL: {pub['url']}")
```

## Рекомендации

1. **Начните с автоматического сбора** - это быстро заполнит онтологию базовыми источниками
2. **Добавляйте качественные источники** - проверяйте актуальность и авторитетность
3. **Используйте ключевые слова** - это улучшит поиск
4. **Указывайте уровень сложности** - помогает пользователям найти подходящие материалы
5. **Регулярно обновляйте** - добавляйте новые источники по мере их появления

## Формат данных

### Книга
```json
{
  "type": "book",
  "title": "Fluent Python",
  "language": "Python",
  "author": "Luciano Ramalho",
  "isbn": "978-1491946008",
  "keywords": "advanced, pythonic",
  "url": "https://...",
  "year": 2015,
  "difficulty": "Advanced"
}
```

### Статья
```json
{
  "type": "article",
  "title": "Python Type Hints",
  "language": "Python",
  "url": "https://docs.python.org/3/library/typing.html",
  "keywords": "type hints, typing"
}
```

## API Endpoints

### Получить источники для языка
```
GET /api/sources/language/<name>
```

### Добавить источник
```
POST /api/sources/add
Content-Type: application/json

{
  "type": "book",
  "title": "...",
  "language": "Python",
  ...
}
```

### Автоматический сбор
```
GET /api/sources/collect/<language>
```

## Примечания

- Все источники автоматически связываются с языками программирования
- Дубликаты проверяются по названию
- Авторы создаются автоматически, если их еще нет
- Онтология сохраняется после каждого добавления (если указано)

