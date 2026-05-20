"""
Скрипт для добавления источников в онтологию
Можно использовать автоматический сбор или ручное добавление
"""
from publication_manager import PublicationManager
from source_collector import SourceCollector
import json

def add_sources_automatically(language: str, pm=None, save: bool = True):
    """
    Автоматическое добавление источников для языка
    
    Args:
        language: Язык программирования
        pm: Экземпляр PublicationManager (если None, создается новый)
        save: Сохранять ли онтологию после добавления
    """
    print(f"🚀 АВТОМАТИЧЕСКОЕ ДОБАВЛЕНИЕ ИСТОЧНИКОВ ДЛЯ {language}")
    print("=" * 60)
    
    if pm is None:
        pm = PublicationManager()
    collector = SourceCollector()
    
    # Собираем источники
    sources = collector.collect_all_sources(language)
    
    added_count = 0
    
    # Добавляем книги
    print(f"\n📚 Добавление книг ({len(sources['books'])}):")
    for book in sources['books']:
        success = pm.add_book(
            title=book['title'],
            language=language,
            author=book.get('author'),
            isbn=book.get('isbn'),
            keywords=book.get('keywords', 'programming, reference')
        )
        if success:
            added_count += 1
    
    # Добавляем документацию
    print(f"\n📖 Добавление документации ({len(sources['documentation'])}):")
    for doc in sources['documentation']:
        success = pm.add_documentation(
            title=doc['title'],
            language=language,
            url=doc['url'],
            description=doc.get('description', f"Official documentation for {language}")
        )
        if success:
            added_count += 1
    
    # Добавляем статьи
    print(f"\n📄 Добавление статей ({len(sources['articles'])}):")
    for article in sources['articles'][:10]:  # Ограничиваем 10 статьями
        success = pm.add_article(
            title=article['title'],
            language=language,
            url=article['url'],
            keywords=article.get('keywords', '')
        )
        if success:
            added_count += 1
    
    # Добавляем туториалы
    print(f"\n🎓 Добавление туториалов ({len(sources['tutorials'])}):")
    for tutorial in sources['tutorials'][:10]:  # Ограничиваем 10 туториалами
        success = pm.add_tutorial(
            title=tutorial['title'],
            language=language,
            url=tutorial['url'],
            keywords=tutorial.get('keywords', 'tutorial, learning')
        )
        if success:
            added_count += 1
    
    # Сохраняем
    if save and added_count > 0:
        pm.save_ontology()
        print(f"\n✅ Добавлено {added_count} источников для {language}")
    else:
        print(f"\n⚠️ Не было добавлено новых источников")
    
    return added_count

def add_source_manually():
    """Интерактивное добавление источника"""
    pm = PublicationManager()
    
    print("📝 РУЧНОЕ ДОБАВЛЕНИЕ ИСТОЧНИКА")
    print("=" * 60)
    
    print("\nВыберите тип источника:")
    print("1. Книга")
    print("2. Статья")
    print("3. Документация")
    print("4. Туториал")
    
    choice = input("\nВведите номер (1-4): ").strip()
    
    language = input("Язык программирования (Python, Java, JavaScript, C, CPlusPlus, CSharp): ").strip()
    title = input("Название: ").strip()
    
    if choice == "1":
        author = input("Автор (опционально): ").strip() or None
        isbn = input("ISBN (опционально): ").strip() or None
        url = input("URL (опционально): ").strip() or None
        keywords = input("Ключевые слова (опционально): ").strip() or None
        
        pm.add_book(
            title=title,
            language=language,
            author=author,
            isbn=isbn,
            url=url,
            keywords=keywords
        )
    
    elif choice == "2":
        url = input("URL: ").strip()
        author = input("Автор (опционально): ").strip() or None
        keywords = input("Ключевые слова (опционально): ").strip() or None
        
        pm.add_article(
            title=title,
            language=language,
            url=url,
            author=author,
            keywords=keywords
        )
    
    elif choice == "3":
        url = input("URL: ").strip()
        description = input("Описание (опционально): ").strip() or None
        
        pm.add_documentation(
            title=title,
            language=language,
            url=url,
            description=description
        )
    
    elif choice == "4":
        url = input("URL: ").strip()
        difficulty = input("Уровень сложности (Beginner/Intermediate/Advanced, опционально): ").strip() or None
        keywords = input("Ключевые слова (опционально): ").strip() or None
        
        pm.add_tutorial(
            title=title,
            language=language,
            url=url,
            difficulty=difficulty,
            keywords=keywords
        )
    
    # Сохраняем
    save = input("\nСохранить изменения? (y/n): ").strip().lower()
    if save == 'y':
        pm.save_ontology()
        print("✅ Изменения сохранены")

def main():
    """Главная функция"""
    print("📚 ДОБАВЛЕНИЕ ИСТОЧНИКОВ В ОНТОЛОГИЮ")
    print("=" * 60)
    print("\nВыберите режим:")
    print("1. Автоматическое добавление для языка")
    print("2. Ручное добавление источника")
    print("3. Добавить источники для всех языков")
    
    choice = input("\nВведите номер (1-3): ").strip()
    
    if choice == "1":
        language = input("Язык программирования: ").strip()
        add_sources_automatically(language)
    
    elif choice == "2":
        add_source_manually()
    
    elif choice == "3":
        languages = ['Python', 'Java', 'JavaScript', 'C', 'CPlusPlus', 'CSharp']
        total_added = 0
        
        # Используем один экземпляр PublicationManager для всех языков
        pm = PublicationManager()
        
        for lang in languages:
            added = add_sources_automatically(lang, pm=pm, save=False)
            total_added += added
        
        # Сохраняем один раз в конце
        if total_added > 0:
            pm.save_ontology()
            print(f"\n✅ Всего добавлено {total_added} источников для всех языков")
        else:
            print(f"\n⚠️ Не было добавлено новых источников")
    
    else:
        print("❌ Неверный выбор")

if __name__ == "__main__":
    main()

