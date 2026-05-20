"""
Скрипт для добавления всех источников
"""
import sys
import os

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from extended_sources import add_extended_sources
    print("=" * 60)
    print("ДОБАВЛЕНИЕ РАСШИРЕННЫХ ИСТОЧНИКОВ")
    print("=" * 60)
    extended_count = add_extended_sources()
    print(f"\n✅ Добавлено {extended_count} расширенных источников")
except Exception as e:
    print(f"Ошибка при добавлении расширенных источников: {e}")
    import traceback
    traceback.print_exc()

try:
    from add_russian_sources import add_russian_sources
    print("\n" + "=" * 60)
    print("ДОБАВЛЕНИЕ РУССКИХ ИСТОЧНИКОВ")
    print("=" * 60)
    add_russian_sources()
except Exception as e:
    print(f"Ошибка при добавлении русских источников: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("✅ ВСЕ ИСТОЧНИКИ ДОБАВЛЕНЫ")
print("=" * 60)

