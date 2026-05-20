import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re
from config import TIOBE_URL, LANGUAGE_MAPPING

class TIOBEImporter:
    def __init__(self, ontology_manager):
        self.om = ontology_manager
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_tiobe_ranking(self, use_demo_fallback=True):
        """Улучшенный парсинг TIOBE с использованием AdvancedTIOBEParser и ImprovedDataFetcher - ТОЛЬКО 6 языков"""
        print("🔍 Запуск улучшенного парсера TIOBE...")
    
        try:
            # Пробуем улучшенный фетчер реальных данных
            from improved_data_fetcher import ImprovedDataFetcher
            fetcher = ImprovedDataFetcher()
            rankings = fetcher.get_tiobe_data_real()
        
            if rankings:
                # Фиксим проблему с языком "C" и фильтруем ТОЛЬКО 6 языков
                fixed_rankings = self._fix_ranking_issues(rankings)
                if len(fixed_rankings) > 0:
                    print(f"✅ Улучшенный фетчер нашел {len(fixed_rankings)} из 6 языков")
                    return fixed_rankings
                else:
                    print("⚠️ Фетчер получил данные, но не смог распознать нужные языки")
            
            # Если не получилось, пробуем AdvancedTIOBEParser
            print("🔄 Пробуем альтернативный парсер...")
            from advanced_tiobe_parser import AdvancedTIOBEParser
            advanced_parser = AdvancedTIOBEParser()
            rankings = advanced_parser.get_tiobe_data()
        
            if rankings:
                # Фиксим проблему с языком "C" и фильтруем ТОЛЬКО 6 языков
                fixed_rankings = self._fix_ranking_issues(rankings)
                if len(fixed_rankings) > 0:
                    print(f"✅ Улучшенный парсер нашел {len(fixed_rankings)} из 6 языков")
                    return fixed_rankings
                else:
                    print("⚠️ Парсер получил данные, но не смог распознать нужные языки")
            
            # Если ничего не получилось, используем fallback
            if use_demo_fallback:
                print("🔄 Используем демо-данные для 6 языков...")
                return self._get_demo_data()
            else:
                print("❌ Парсеры не смогли получить данные")
                return []
            
        except Exception as e:
            print(f"❌ Ошибка парсеров: {e}")
            import traceback
            traceback.print_exc()
        
            if use_demo_fallback:
                print("🔄 Используем демо-данные для 6 языков...")
                return self._get_demo_data()
            else:
                return []

    def _fix_ranking_issues(self, rankings):
        """Исправление проблем с распознаванием данных - ТОЛЬКО 6 языков"""
        fixed_rankings = []
        
        # Маппинг различных вариантов названий на нормализованные
        language_mapping = {
            # Python
            'Python': 'Python',
            'python': 'Python',
            
            # Java
            'Java': 'Java',
            'java': 'Java',
            
            # JavaScript
            'JavaScript': 'JavaScript',
            'javascript': 'JavaScript',
            'JS': 'JavaScript',
            'js': 'JavaScript',
            
            # C
            'C': 'C',
            'c': 'C',
            '+091': 'C',
            '+0.91%': 'C',
            
            # C++
            'C++': 'CPlusPlus',
            'CPlusPlus': 'CPlusPlus',
            'Cpp': 'CPlusPlus',
            'cpp': 'CPlusPlus',
            'C Plus Plus': 'CPlusPlus',
            
            # C#
            'C#': 'CSharp',
            'CSharp': 'CSharp',
            'Csharp': 'CSharp',
            'C Sharp': 'CSharp',
            'csharp': 'CSharp',
        }
        
        target_languages = ['Python', 'Java', 'JavaScript', 'C', 'CPlusPlus', 'CSharp']
        
        print(f"🔍 Обработка {len(rankings)} рейтингов...")
        
        for lang in rankings:
            original_name = lang.get('original_name', lang.get('name', ''))
            current_name = lang.get('name', '')
            
            # Исправляем язык "C" (вместо "+0.91%")
            if current_name == '+091' or original_name == '+0.91%' or '+0.91%' in str(original_name):
                lang['name'] = 'C'
                lang['original_name'] = 'C'
                current_name = 'C'
            
            # Пробуем найти нормализованное имя
            normalized_name = None
            
            # Проверяем текущее имя
            if current_name in language_mapping:
                normalized_name = language_mapping[current_name]
            # Проверяем оригинальное имя
            elif original_name in language_mapping:
                normalized_name = language_mapping[original_name]
            # Пробуем найти по частичному совпадению
            else:
                for key, value in language_mapping.items():
                    if key.lower() in current_name.lower() or key.lower() in original_name.lower():
                        normalized_name = value
                        break
            
            # Если нашли нормализованное имя, обновляем
            if normalized_name:
                lang['name'] = normalized_name
                if normalized_name in target_languages:
                    fixed_rankings.append(lang)
                    print(f"   ✅ Найден: {original_name} -> {normalized_name}")
            else:
                # Выводим для отладки, что не распознано
                print(f"   ⚠️ Не распознано: {current_name} (оригинал: {original_name})")
        
        print(f"🎯 Фильтр: оставлено {len(fixed_rankings)} из 6 целевых языков")
        
        # Если ничего не найдено, выводим все полученные названия для отладки
        if len(fixed_rankings) == 0 and len(rankings) > 0:
            print(f"📋 Полученные языки из TIOBE:")
            for i, lang in enumerate(rankings[:10], 1):
                print(f"   {i}. '{lang.get('name', 'N/A')}' (оригинал: '{lang.get('original_name', 'N/A')}')")
        
        return fixed_rankings
    
    def _parse_tiobe_page(self, soup):
        """Парсинг страницы TIOBE - исправленная версия"""
        rankings = []
    
        print("🔍 Поиск таблицы TIOBE...")
    
        # Пробуем разные селекторы
        selectors = ['table', '.table', '#top20', '.tiobe-table']
    
        for selector in selectors:
            tables = soup.find_all(selector)
            for table in tables:
                rows = table.find_all('tr')[1:21]  # Первые 20 строк после заголовка
            
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 4:
                        try:
                            # Берем текст из ячеек
                            rank_text = cols[0].get_text(strip=True)
                            name_text = cols[1].get_text(strip=True)
                            rating_text = cols[2].get_text(strip=True)
                        
                            # Извлекаем числовой ранг
                            rank_match = re.search(r'(\d+)', rank_text)
                            if rank_match:
                                rank = int(rank_match.group(1))
                            
                                # Пропускаем если имя пустое или это число
                                if not name_text or name_text.isdigit():
                                    continue
                                
                                # Нормализуем имя языка
                                normalized_name = self._normalize_language_name(name_text)
                            
                                rankings.append({
                                    'rank': rank,
                                    'name': normalized_name,
                                    'rating': rating_text,
                                    'original_name': name_text
                                })
                                print(f"   ✅ Найден: {name_text} -> {normalized_name}")
                            
                        except Exception as e:
                         continue
            
                if rankings:
                    print(f"✅ Найдено {len(rankings)} языков с селектором '{selector}'")
                    return rankings
    
        print("❌ Не удалось найти данные в таблицах")
        return []
    
    def _normalize_language_name(self, original_name):
        """Нормализация названия языка - ТОЛЬКО 6 языков"""
        # Убираем лишние символы
        clean_name = re.sub(r'[^\w\s#+]', '', original_name).strip()
        
        # Используем маппинг из конфига
        normalized = LANGUAGE_MAPPING.get(clean_name)
        
        if normalized:
            return normalized
        
        # Автоматическая нормализация только для 6 языков
        name_map = {
            'C++': 'CPlusPlus',
            'C#': 'CSharp',
            'JavaScript': 'JavaScript'
        }
        
        return name_map.get(clean_name, clean_name.replace(' ', '').replace('#', 'Sharp'))
    
    def _get_demo_data(self):
        """Демо-данные для тестирования - ТОЛЬКО 6 языков"""
        return [
            {'rank': 1, 'name': 'Python', 'rating': '15.07%', 'original_name': 'Python'},
            {'rank': 2, 'name': 'C', 'rating': '11.95%', 'original_name': 'C'},
            {'rank': 3, 'name': 'CPlusPlus', 'rating': '10.36%', 'original_name': 'C++'},
            {'rank': 4, 'name': 'Java', 'rating': '9.08%', 'original_name': 'Java'},
            {'rank': 5, 'name': 'CSharp', 'rating': '7.62%', 'original_name': 'C#'},
            {'rank': 6, 'name': 'JavaScript', 'rating': '2.91%', 'original_name': 'JavaScript'}
        ]
    
    def update_ontology_with_rankings(self, rankings):
        """Обновление онтологии новыми рейтингами"""
        updated_count = 0
        failed_updates = []
        
        for lang_data in rankings:
            success = self.om.update_language_ranking(
                lang_data['name'], 
                lang_data['rank'], 
                lang_data['rating']
            )
            
            if success:
                updated_count += 1
            else:
                failed_updates.append(lang_data['name'])
        
        # Добавляем метаданные об обновлении
        if updated_count > 0:
            self._add_update_metadata()
        
        return {
            'updated_count': updated_count,
            'failed_updates': failed_updates,
            'total_rankings': len(rankings)
        }
    
    def _add_update_metadata(self):
        """Добавление метаданных об обновлении"""
        timestamp = datetime.now().isoformat()
        print(f"📅 Обновление TIOBE завершено: {timestamp}")

def test_tiobe_importer():
    """Тестирование TIOBE импортера - ТОЛЬКО 6 языков"""
    from ontology_manager import OntologyManager
    
    print("🧪 ТЕСТИРОВАНИЕ TIOBE ИМПОРТЕРА (6 ЯЗЫКОВ)")
    print("=" * 50)
    
    om = OntologyManager(r"D:\OneDrive\Рабочий стол\tiobe_importer\data\programming_languages.ttl")
    importer = TIOBEImporter(om)
    
    rankings = importer.scrape_tiobe_ranking(use_demo_fallback=True)
    
    if rankings:
        print(f"\n🏆 ТОП-6 ЯЗЫКОВ TIOBE:")
        for lang in rankings:
            print(f"   #{lang['rank']:2} {lang['name']:12} - {lang['rating']:8}")
        
        # Обновляем онтологию
        result = importer.update_ontology_with_rankings(rankings)
        print(f"\n📊 Обновлено: {result['updated_count']} языков")
        
        if om.save_ontology():
            print("💾 Онтология сохранена!")
    else:
        print("❌ Не удалось получить данные TIOBE")

if __name__ == "__main__":
    test_tiobe_importer()