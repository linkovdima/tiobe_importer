"""
Скрипт для обновления всех источников
Добавляет расширенные источники из extended_sources.py
"""
from extended_sources import add_extended_sources
from add_russian_sources import add_russian_sources

if __name__ == "__main__":
    print("=" * 60)
    print("ОБНОВЛЕНИЕ ВСЕХ ИСТОЧНИКОВ")
    print("=" * 60)
    print()
    
    # Добавляем расширенные источники
    print("📚 Добавление расширенных источников...")
    extended_count = add_extended_sources()
    
    # Добавляем русские источники (они проверят дубликаты)
    print("\n📚 Добавление русских источников...")
    add_russian_sources()
    
    print("\n" + "=" * 60)
    print("✅ ОБНОВЛЕНИЕ ЗАВЕРШЕНО")
    print("=" * 60)
