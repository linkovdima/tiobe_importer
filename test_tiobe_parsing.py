"""
Тестовый скрипт для проверки парсинга TIOBE
Помогает понять структуру таблицы и отладить парсер
"""
import requests
from bs4 import BeautifulSoup
import re

def test_tiobe_parsing():
    """Тестирование парсинга TIOBE с подробным выводом"""
    print("🧪 ТЕСТИРОВАНИЕ ПАРСИНГА TIOBE")
    print("=" * 60)
    
    try:
        url = "https://www.tiobe.com/tiobe-index/"
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        print(f"🌐 Загрузка: {url}")
        response = session.get(url, timeout=15)
        
        if response.status_code != 200:
            print(f"❌ Ошибка HTTP: {response.status_code}")
            return
        
        print("✅ Страница загружена")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Ищем все таблицы
        tables = soup.find_all('table')
        print(f"\n📊 Найдено таблиц: {len(tables)}")
        
        for table_idx, table in enumerate(tables, 1):
            print(f"\n{'='*60}")
            print(f"ТАБЛИЦА {table_idx}")
            print(f"{'='*60}")
            
            rows = table.find_all('tr')
            print(f"Строк в таблице: {len(rows)}")
            
            # Показываем заголовок
            if rows:
                header_row = rows[0]
                header_cells = header_row.find_all(['td', 'th'])
                header_texts = [cell.get_text(strip=True) for cell in header_cells]
                print(f"Заголовок: {header_texts}")
            
            # Показываем первые 5 строк данных
            print(f"\nПервые 5 строк данных:")
            for i, row in enumerate(rows[1:6], 1):
                cols = row.find_all(['td', 'th'])
                cell_texts = [col.get_text(strip=True) for col in cols]
                print(f"  Строка {i}: {cell_texts}")
                
                # Пробуем определить структуру
                if len(cell_texts) >= 3:
                    print(f"    → Колонка 0: '{cell_texts[0]}' (ранг?)")
                    print(f"    → Колонка 1: '{cell_texts[1]}' (название?)")
                    print(f"    → Колонка 2: '{cell_texts[2]}' (рейтинг?)")
            
            # Пробуем извлечь данные
            print(f"\nПопытка извлечения данных:")
            rankings = []
            for i, row in enumerate(rows[1:21], 1):
                cols = row.find_all(['td', 'th'])
                if len(cols) >= 2:
                    cell_texts = [col.get_text(strip=True) for col in cols]
                    
                    # Анализируем ячейки
                    rank = None
                    name = None
                    rating = None
                    
                    for j, text in enumerate(cell_texts):
                        # Ранг - только число
                        if text.isdigit() and int(text) <= 50 and rank is None:
                            rank = int(text)
                        # Рейтинг - содержит %
                        elif '%' in text and rating is None:
                            rating = text
                        # Название - не число, не рейтинг, не пустое
                        elif (text and 
                              not text.isdigit() and 
                              '%' not in text and
                              len(text) > 1 and
                              text.lower() not in ['rank', 'programming language', 'ratings', 'change', ''] and
                              name is None):
                            name = text
                    
                    if rank and name:
                        rankings.append({
                            'rank': rank,
                            'name': name,
                            'rating': rating or 'N/A'
                        })
                        print(f"  ✅ #{rank} {name} ({rating or 'N/A'})")
                    elif len(cell_texts) > 0:
                        print(f"  ⚠️ Не распознано: {cell_texts}")
            
            if len(rankings) >= 5:
                print(f"\n✅ Успешно извлечено {len(rankings)} рейтингов из таблицы {table_idx}")
                return rankings
            else:
                print(f"\n⚠️ Недостаточно данных из таблицы {table_idx} ({len(rankings)} рейтингов)")
        
        print("\n❌ Не удалось извлечь данные ни из одной таблицы")
        return None
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_tiobe_parsing()

