"""Тестовый скрипт для проверки генератора библиографии"""
import sys
import io

# Перенаправляем вывод
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

try:
    from bibliography_generator import BibliographyGenerator
    
    print("=" * 60)
    print("📚 ГЕНЕРАТОР СПИСКА ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ")
    print("=" * 60)
    
    generator = BibliographyGenerator()
    
    # Генерируем HTML
    success = generator.generate_html("bibliography.html")
    
    if success:
        print("\n✅ Готово! Откройте файл bibliography.html в браузере")
    else:
        print("\n❌ Ошибка генерации списка источников")
        
except Exception as e:
    print(f"\n❌ Критическая ошибка: {e}")
    import traceback
    traceback.print_exc()









