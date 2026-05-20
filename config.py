# Конфигурация проекта
import os
from pathlib import Path

# Пути
BASE_DIR = Path(__file__).parent
ONTOLOGY_PATH = BASE_DIR / "data" / "programming_languages.ttl"
LOG_PATH = BASE_DIR / "logs" / "update_log.json"

# Настройки TIOBE
TIOBE_URL = "https://www.tiobe.com/tiobe-index/"

# Настройки обновления
UPDATE_SCHEDULE = {
    'daily': '09:00',      # Ежедневно в 9:00 (для тестирования)
    'monthly': '1 09:00'   # 1-го числа каждого месяца в 9:00
}

# Маппинг названий языков
LANGUAGE_MAPPING = {
    'Python': 'Python',
    'C': 'C',
    'C++': 'CPlusPlus', 
    'Java': 'Java',
    'C#': 'CSharp',
    'JavaScript': 'JavaScript',
    'Visual Basic': 'VisualBasic',
    'PHP': 'PHP',
    'SQL': 'SQL',
    'Go': 'Go',
    'R': 'R',
    'Swift': 'Swift',
    'Kotlin': 'Kotlin',
    'Rust': 'Rust',
    'TypeScript': 'TypeScript'
}