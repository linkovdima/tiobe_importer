import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urljoin
import json

class AdvancedTIOBEParser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def get_tiobe_data(self):
        """Основной метод получения данных TIOBE"""
        print("🎯 ЗАПУСК УЛУЧШЕННОГО ПАРСЕРА TIOBE")
        print("=" * 60)
        
        strategies = [
            self._try_direct_parsing,
            self._try_alternative_sources,
            self._try_archive_org,
            self._try_api_endpoints,
        ]
        
        for strategy in strategies:
            print(f"\n🔄 Попытка стратегии: {strategy.__name__}")
            result = strategy()
            if result:
                print(f"✅ Успех! Найдено {len(result)} языков")
                return result
            time.sleep(1)  # Пауза между запросами
        
        print("❌ Все стратегии не сработали")
        return None
    
    def _try_direct_parsing(self):
        """Прямой парсинг TIOBE сайта"""
        try:
            url = "https://www.tiobe.com/tiobe-index/"
            print(f"🌐 Загрузка: {url}")
            
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Стратегия 1: Ищем по классам таблицы
            rankings = self._parse_by_table_classes(soup)
            if rankings:
                return rankings
            
            # Стратегия 2: Ищем по текстовым паттернам
            rankings = self._parse_by_text_patterns(soup)
            if rankings:
                return rankings
                
            # Стратегия 3: Ищем в script тегах
            rankings = self._parse_script_tags(soup)
            if rankings:
                return rankings
                
        except Exception as e:
            print(f"❌ Ошибка прямого парсинга: {e}")
        
        return None
    
    def _parse_by_table_classes(self, soup):
        """Парсинг по CSS классам таблиц"""
        print("🔍 Поиск таблиц по CSS классам...")
        
        # Известные классы таблиц TIOBE
        table_selectors = [
            'table.table.table-striped',
            'table.table',
            '.table-responsive table',
            '#top20',
            'table#top20',
            '.tiobe-table',
            'table[class*="table"]',
            'table',
        ]
        
        for selector in table_selectors:
            tables = soup.select(selector)
            print(f"   Проверка селектора '{selector}': найдено {len(tables)} таблиц")
            
            for i, table in enumerate(tables):
                rankings = self._extract_from_html_table(table)
                if rankings:
                    print(f"✅ Успех с селектором '{selector}': {len(rankings)} языков")
                    return rankings
        
        return None
    
    def _parse_by_text_patterns(self, soup):
        """Парсинг по текстовым паттернам TIOBE"""
        print("🔍 Поиск по текстовым паттернам...")
        
        # Ищем характерные для TIOBE тексты
        tiobe_indicators = [
            'TIOBE Programming Community Index',
            'TIOBE Index',
            'Top 20 Programming Languages',
            'Long term history',
            'Programming Language'
        ]
        
        for indicator in tiobe_indicators:
            elements = soup.find_all(string=re.compile(re.escape(indicator), re.I))
            if elements:
                print(f"✅ Найден индикатор: {indicator}")
                # Ищем таблицу рядом с индикатором
                for element in elements:
                    # Ищем в родительских элементах
                    current = element.parent
                    for depth in range(10):  # Проверяем несколько уровней вверх
                        if current:
                            # Ищем таблицы в этом элементе
                            tables = current.find_all('table')
                            for table in tables:
                                rankings = self._extract_from_html_table(table)
                                if rankings:
                                    return rankings
                            
                            # Переходим к родителю
                            current = current.parent
        
        return None
    
    def _parse_script_tags(self, soup):
        """Парсинг script тегов"""
        print("🔍 Поиск в script тегах...")
        
        scripts = soup.find_all('script')
        
        for i, script in enumerate(scripts):
            if script.string:
                # Ищем данные в тексте script
                text = script.string
                
                # Ищем JSON данные
                if '{' in text and '}' in text:
                    try:
                        # Пробуем извлечь JSON
                        json_match = re.search(r'\{.*\}', text, re.DOTALL)
                        if json_match:
                            data = json.loads(json_match.group())
                            rankings = self._extract_from_json(data)
                            if rankings:
                                return rankings
                    except:
                        pass
                
                # Ищем массивы данных
                if 'Python' in text and 'Java' in text:
                    print(f"   Найден script с данными о языках")
                    # Здесь можно добавить специфичный парсинг
        
        return None
    
    def _try_alternative_sources(self):
        """Альтернативные источники данных"""
        print("🔍 Поиск альтернативных источников...")
        
        alternative_urls = [
            "https://pypl.github.io/PYPL.html",
        ]
        
        for url in alternative_urls:
            try:
                print(f"🌐 Проверка: {url}")
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    # Парсинг PYPL (другой рейтинг)
                    tables = soup.find_all('table')
                    for table in tables:
                        rankings = self._extract_from_html_table(table)
                        if rankings:
                            # Добавляем источник
                            for rank in rankings:
                                rank['source'] = 'PYPL'
                            return rankings
            except Exception as e:
                print(f"   Ошибка: {e}")
                continue
        
        return None
    
    def _try_archive_org(self):
        """Использование Archive.org"""
        try:
            # Пробуем разные даты
            dates = ['20241001', '20240701', '20240401']
            
            for date in dates:
                url = f"https://web.archive.org/web/{date}/https://www.tiobe.com/tiobe-index/"
                print(f"📚 Проверка Archive.org: {date}")
                
                response = self.session.get(url, timeout=15)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    rankings = self._parse_by_table_classes(soup)
                    if rankings:
                        for rank in rankings:
                            rank['source'] = f'Archive_{date}'
                        return rankings
                    time.sleep(1)
                    
        except Exception as e:
            print(f"❌ Ошибка Archive.org: {e}")
        
        return None
    
    def _try_api_endpoints(self):
        """Поиск API endpoints"""
        print("🔍 Поиск API endpoints...")
        
        # Возможные API endpoints (если есть)
        api_urls = [
            "https://www.tiobe.com/wp-json/wp/v2/posts",
            "https://www.tiobe.com/api/tiobe-index",
        ]
        
        for url in api_urls:
            try:
                print(f"🌐 Проверка API: {url}")
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    # Здесь можно добавить парсинг API ответа
                    print(f"   API доступен, но формат неизвестен")
            except:
                continue
        
        return None
    
    def _extract_from_html_table(self, table):
        """Извлечение данных из HTML таблицы"""
        rankings = []
        
        rows = table.find_all('tr')
        print(f"   Анализ таблицы: {len(rows)} строк")
        
        for i, row in enumerate(rows):
            # Пропускаем пустые строки и заголовки
            if i == 0:  # Первая строка может быть заголовком
                header_cells = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
                print(f"   Заголовок: {header_cells}")
                continue
            
            cols = row.find_all(['td', 'th'])
            if len(cols) >= 2:  # Нужен как минимум ранг и название
                try:
                    # Получаем текст из всех ячеек
                    cells = [col.get_text(strip=True) for col in cols]
                    
                    # Анализируем ячейки для поиска паттерна TIOBE
                    rank, name, rating = self._analyze_cells(cells)
                    
                    # Проверяем, что name не является числом
                    if rank and name and not name.isdigit() and len(name) > 1:
                        # Пропускаем служебные тексты
                        if name.lower() not in ['rank', 'programming language', 'ratings', 'change', '']:
                            normalized_name = self._normalize_language_name(name)
                            
                            rankings.append({
                                'rank': rank,
                                'name': normalized_name,
                                'rating': rating or 'N/A',
                                'original_name': name,
                                'source': 'html_table'
                            })
                            print(f"     ✅ Строка {i}: {name} -> {normalized_name} (#{rank})")
                        
                except Exception as e:
                    continue
        
        # Возвращаем только если нашли достаточно данных
        return rankings if len(rankings) >= 3 else None
    
    def _analyze_cells(self, cells):
        """Анализ ячеек для идентификации ранга, имени и рейтинга"""
        rank = None
        name = None
        rating = None
        
        # Сначала ищем рейтинг (содержит %)
        for cell in cells:
            cell = cell.strip()
            if '%' in cell and not rating:
                rating = cell
                break
        
        # Затем ищем ранг (только число, обычно первое или второе)
        for i, cell in enumerate(cells[:3]):  # Проверяем первые 3 ячейки
            cell = cell.strip()
            if re.match(r'^\d+$', cell) and not rank:
                # Проверяем, что это не часть названия языка
                if int(cell) <= 50:  # Разумный предел для ранга
                    rank = int(cell)
                    break
        
        # Наконец ищем имя языка (не число, не рейтинг, не служебный текст)
        for cell in cells:
            cell = cell.strip()
            if (cell and 
                not cell.isdigit() and 
                not re.match(r'^[\d\.%\-+\s]+$', cell) and  # Не только числа и символы
                cell.lower() not in ['rank', 'programming language', 'ratings', 'change', ''] and
                len(cell) > 1 and 
                '%' not in cell and  # Не рейтинг
                not name):
                name = cell
                break
        
        return rank, name, rating
    
    def _normalize_language_name(self, name):
        """Нормализация названий языков"""
        name_mapping = {
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
            'TypeScript': 'TypeScript',
            'MATLAB': 'MATLAB',
            'Assembly language': 'Assembly',
            'Ruby': 'Ruby',
            'Perl': 'Perl',
            'Objective-C': 'ObjectiveC',
            'Visual Basic .NET': 'VisualBasic',
            'Delphi/Object Pascal': 'Delphi',
            'Classic Visual Basic': 'VisualBasic',
        }
        
        # Очистка названия
        clean_name = re.sub(r'[^\w\s#+\.]', '', name).strip()
        
        return name_mapping.get(clean_name, clean_name.replace(' ', '').replace('#', 'Sharp').replace('.', ''))
    
    def _extract_from_json(self, data):
        """Извлечение данных из JSON"""
        # Простой поиск в JSON структуре
        if isinstance(data, dict):
            # Ищем массивы с данными
            for key, value in data.items():
                if isinstance(value, list) and len(value) > 0:
                    if isinstance(value[0], dict) and any('name' in item or 'rank' in item for item in value):
                        print(f"   Найден потенциальный массив данных в ключе: {key}")
        return None

def test_advanced_parser():
    """Тестирование улучшенного парсера"""
    parser = AdvancedTIOBEParser()
    
    print("🧪 ТЕСТИРОВАНИЕ УЛУЧШЕННОГО ПАРСЕРА")
    print("=" * 60)
    
    start_time = time.time()
    rankings = parser.get_tiobe_data()
    end_time = time.time()
    
    if rankings:
        print(f"\n🎉 УСПЕХ! Получено данных за {end_time - start_time:.2f} секунд")
        print("\n🏆 ТОП-10 ЯЗЫКОВ:")
        for i, lang in enumerate(rankings[:10], 1):
            print(f"   {lang['rank']:2d}. {lang['name']:15} - {lang['rating']:8} ({lang['source']})")
        
        print(f"\n📊 Всего языков: {len(rankings)}")
        return rankings
    else:
        print("\n❌ Не удалось получить реальные данные")
        print("💡 Рекомендации:")
        print("   • TIOBE может блокировать автоматические запросы")
        print("   • Структура сайта могла измениться")
        print("   • Используйте демо-данные как fallback")
        return None

if __name__ == "__main__":
    test_advanced_parser()