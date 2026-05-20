import os
from rdflib import Graph

def find_ontology_files():
    """Поиск файлов онтологии"""
    print("🔍 ПОИСК ФАЙЛОВ ОНТОЛОГИИ")
    print("=" * 50)
    
    # Проверяем разные возможные пути
    possible_paths = [
        r"D:\OneDrive\Документы\protege_test\my_ontology.ttl",
        r"D:\OneDrive\Документы\protege_test\my_ontology.owl",
        r"D:\OneDrive\Рабочий стол\tiobe_importer\data\programming_languages.ttl",
        r"D:\OneDrive\Рабочий стол\tiobe_importer\programming_languages.ttl",
        "my_ontology.ttl",
        "programming_languages.ttl"
    ]
    
    found_files = []
    
    for path in possible_paths:
        if os.path.exists(path):
            # Проверяем размер файла
            file_size = os.path.getsize(path)
            print(f"✅ Найден: {path} ({file_size} байт)")
            found_files.append(path)
            
            # Пробуем загрузить
            try:
                g = Graph()
                g.parse(path, format="turtle")
                print(f"   📊 Загружено триплов: {len(g)}")
            except Exception as e:
                print(f"   ❌ Ошибка загрузки: {e}")
        else:
            print(f"❌ Не найден: {path}")
    
    return found_files

if __name__ == "__main__":
    found = find_ontology_files()
    if found:
        print(f"\n🎯 Найдено файлов: {len(found)}")
        print("Скопируйте правильный путь в config.py")
    else:
        print("\n❌ Файлы онтологии не найдены!")