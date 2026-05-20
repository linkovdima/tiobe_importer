# 🔄 Инструкция по обновлению проекта

## Быстрое обновление всех данных

Запустите один скрипт для обновления всех данных:

```bash
python update_all_data.py
```

Этот скрипт выполнит:
1. ✅ Обновление TIOBE данных
2. ✅ Обновление данных из GitHub, Stack Overflow и других источников
3. ✅ Добавление новых источников (книги, документация, туториалы)
4. ✅ Проверку результатов

## Пошаговое обновление

### 1. Обновление TIOBE данных

```bash
python main.py update
```

Или напрямую:

```bash
python -c "from main import TIOBEUpdater; TIOBEUpdater().run_update()"
```

### 2. Обновление данных из всех источников

```bash
python -c "from ontology_manager import OntologyManager; from data_sources_manager import DataSourcesManager; om = OntologyManager(); dsm = DataSourcesManager(om); dsm.update_all_sources(); om.save_ontology()"
```

### 3. Добавление источников

```bash
python add_russian_sources.py
```

### 4. Проверка результатов

```bash
python check_sources.py
```

## Исправление проблем

### График TIOBE не отображается

1. Проверьте, что данные TIOBE есть в онтологии:
   ```bash
   python check_sources.py
   ```

2. Если данных нет, обновите их:
   ```bash
   python main.py update
   ```

3. Перезапустите веб-сервер:
   ```bash
   python web_dashboard.py
   ```

### Поиск не находит результаты

1. Убедитесь, что источники добавлены:
   ```bash
   python add_russian_sources.py
   ```

2. Проверьте количество источников:
   ```bash
   python check_sources.py
   ```

### Данные не обновляются

1. Проверьте подключение к интернету
2. Проверьте наличие токена GitHub (опционально, но рекомендуется):
   - Создайте токен на https://github.com/settings/tokens
   - Добавьте в `github_config.py`:
     ```python
     GITHUB_TOKEN = "ваш_токен"
     ```

## Рекомендуемая частота обновления

- **TIOBE данные**: раз в месяц (они обновляются ежемесячно)
- **GitHub/Stack Overflow**: раз в неделю
- **Источники (книги, документация)**: по мере необходимости

## Автоматическое обновление

Для автоматического обновления используйте:

```bash
python main.py
```

Это запустит сервис с автоматическим обновлением по расписанию (настраивается в `config.py`).

