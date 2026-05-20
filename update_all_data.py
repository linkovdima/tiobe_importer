"""
Скрипт для полного обновления всех данных проекта
"""
import sys
from pathlib import Path

def update_all_data():
    """Обновление всех данных проекта"""
    print("🔄 ПОЛНОЕ ОБНОВЛЕНИЕ ДАННЫХ ПРОЕКТА")
    print("=" * 60)
    
    # 1. Обновление TIOBE данных
    print("\n1️⃣ Обновление TIOBE данных...")
    try:
        from main import TIOBEUpdater
        updater = TIOBEUpdater()
        success = updater.run_update(use_demo_fallback=True)
        if success:
            print("✅ TIOBE данные обновлены")
        else:
            print("⚠️ Не удалось обновить TIOBE данные")
    except Exception as e:
        print(f"❌ Ошибка обновления TIOBE: {e}")
    
    # 2. Обновление данных из всех источников
    print("\n2️⃣ Обновление данных из всех источников...")
    try:
        from ontology_manager import OntologyManager
        from data_sources_manager import DataSourcesManager
        
        om = OntologyManager()
        dsm = DataSourcesManager(om)
        dsm.update_all_sources(use_extended_sources=True)
        om.save_ontology()
        print("✅ Данные из всех источников обновлены")
    except Exception as e:
        print(f"❌ Ошибка обновления данных: {e}")
        import traceback
        traceback.print_exc()
    
    # 3. Добавление источников
    print("\n3️⃣ Добавление источников...")
    try:
        from add_russian_sources import add_russian_sources
        add_russian_sources()
        print("✅ Источники добавлены")
    except Exception as e:
        print(f"❌ Ошибка добавления источников: {e}")
        import traceback
        traceback.print_exc()
    
    # 4. Проверка результатов
    print("\n4️⃣ Проверка результатов...")
    try:
        from check_sources import check_all_sources
        check_all_sources()
    except Exception as e:
        print(f"⚠️ Не удалось проверить результаты: {e}")
    
    print("\n" + "=" * 60)
    print("✅ ОБНОВЛЕНИЕ ЗАВЕРШЕНО")
    print("=" * 60)

if __name__ == "__main__":
    update_all_data()

