"""
Улучшенный модуль получения реальных данных из различных источников
"""
import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
import re

class ImprovedDataFetcher:
    """Класс для получения реальных данных из различных источников"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_tiobe_data_real(self) -> List[Dict]:
        """
        Получение реальных данных TIOBE
        
        Источники:
        1. Прямой парсинг TIOBE сайта
        2. Альтернативные источники (PYPL, GitHub trends)
        3. Wikipedia страницы языков
        """
        print("🔍 Получение реальных данных TIOBE...")
        
        # Стратегия 1: Парсинг TIOBE сайта
        tiobe_data = self._parse_tiobe_site()
        if tiobe_data:
            return tiobe_data
        
        # Стратегия 2: Альтернативные источники
        alt_data = self._get_alternative_rankings()
        if alt_data:
            return alt_data
        
        return []
    
    def _parse_tiobe_site(self) -> Optional[List[Dict]]:
        """Парсинг официального сайта TIOBE"""
        try:
            url = "https://www.tiobe.com/tiobe-index/"
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Ищем таблицу с рейтингами
                tables = soup.find_all('table')
                
                for table in tables:
                    rows = table.find_all('tr')
                    if len(rows) < 2:
                        continue
                    
                    # Пропускаем заголовок, берем первые 20 строк данных
                    data_rows = rows[1:21]
                    rankings = []
                    
                    for row in data_rows:
                        cols = row.find_all(['td', 'th'])
                        if len(cols) < 2:
                            continue
                        
                        try:
                            # Пробуем разные варианты структуры таблицы
                            # Вариант 1: ранг, название, рейтинг, изменение
                            # Вариант 2: ранг, название, рейтинг
                            
                            # Извлекаем все тексты из ячеек
                            cell_texts = [col.get_text(strip=True) for col in cols]
                            
                            # Ищем ранг (обычно первая ячейка или содержит только число)
                            rank = None
                            name_text = None
                            rating_text = None
                            
                            for i, text in enumerate(cell_texts):
                                # Если текст - это только число, это может быть ранг
                                if text.isdigit() and rank is None:
                                    rank = int(text)
                                # Если текст содержит %, это рейтинг
                                elif '%' in text and rating_text is None:
                                    rating_text = text
                                # Если текст не число и не рейтинг, это название языка
                                elif not text.isdigit() and '%' not in text and len(text) > 1 and name_text is None:
                                    # Пропускаем служебные тексты
                                    if text.lower() not in ['rank', 'programming language', 'ratings', 'change', '']:
                                        name_text = text
                            
                            # Если не нашли ранг, используем индекс строки
                            if rank is None:
                                rank = len(rankings) + 1
                            
                            # Если нашли название языка
                            if name_text and name_text and not name_text.isdigit():
                                # Нормализуем имя
                                normalized = self._normalize_language_name(name_text)
                                
                                rankings.append({
                                    'rank': rank,
                                    'name': normalized,
                                    'rating': rating_text or 'N/A',
                                    'original_name': name_text,
                                    'source': 'tiobe_official'
                                })
                                
                        except Exception as e:
                            # Пропускаем проблемные строки
                            continue
                    
                    if len(rankings) >= 5:
                        print(f"✅ Получено {len(rankings)} рейтингов с TIOBE")
                        # Выводим первые несколько для отладки
                        for lang in rankings[:3]:
                            print(f"   Пример: #{lang['rank']} {lang['original_name']} -> {lang['name']}")
                        return rankings
        except Exception as e:
            print(f"⚠️ Ошибка парсинга TIOBE: {e}")
            import traceback
            traceback.print_exc()
        
        return None
    
    def _get_alternative_rankings(self) -> Optional[List[Dict]]:
        """Получение рейтингов из альтернативных источников"""
        # PYPL (PopularitY of Programming Language)
        try:
            url = "https://pypl.github.io/PYPL.html"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                tables = soup.find_all('table')
                
                for table in tables:
                    rows = table.find_all('tr')[1:21]
                    rankings = []
                    
                    for i, row in enumerate(rows, 1):
                        cols = row.find_all('td')
                        if len(cols) >= 2:
                            name_text = cols[0].get_text(strip=True)
                            share_text = cols[1].get_text(strip=True) if len(cols) > 1 else ""
                            
                            if name_text:
                                normalized = self._normalize_language_name(name_text)
                                rankings.append({
                                    'rank': i,
                                    'name': normalized,
                                    'rating': share_text,
                                    'original_name': name_text,
                                    'source': 'pypl'
                                })
                    
                    if len(rankings) >= 5:
                        print(f"✅ Получено {len(rankings)} рейтингов с PYPL")
                        return rankings
        except Exception as e:
            print(f"⚠️ Ошибка получения PYPL: {e}")
        
        return None
    
    def get_github_data_real(self, language: str) -> Optional[Dict]:
        """
        Получение реальных данных GitHub для языка
        
        Использует GitHub API для получения статистики
        """
        try:
            from github_config import GITHUB_TOKEN
            
            # Нормализуем имя языка для GitHub API
            github_lang_map = {
                'Python': 'python',
                'Java': 'java',
                'JavaScript': 'javascript',
                'C': 'c',
                'CPlusPlus': 'cpp',
                'CSharp': 'csharp'
            }
            
            github_lang = github_lang_map.get(language, language.lower())
            
            # Запрос к GitHub API
            url = f"https://api.github.com/search/repositories?q=language:{github_lang}&sort=stars&order=desc&per_page=10"
            
            headers = {
                'User-Agent': 'ProgrammingLanguageOntology/1.0',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            if GITHUB_TOKEN:
                headers['Authorization'] = f'token {GITHUB_TOKEN}'
            
            response = self.session.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                total_repos = data.get('total_count', 0)
                items = data.get('items', [])
                
                total_stars = sum(repo['stargazers_count'] for repo in items)
                avg_stars = total_stars / len(items) if items else 0
                
                return {
                    'total_repositories': total_repos,
                    'total_stars': total_stars,
                    'average_stars': round(avg_stars, 1),
                    'top_repositories': [repo['name'] for repo in items[:5]],
                    'last_updated': datetime.now().isoformat(),
                    'source': 'github_api'
                }
            elif response.status_code == 403:
                print(f"⚠️ Rate limit для GitHub API (язык: {language})")
                return None
            else:
                print(f"⚠️ Ошибка GitHub API: {response.status_code}")
                return None
                
        except ImportError:
            print("⚠️ GitHub token не найден")
            return None
        except Exception as e:
            print(f"⚠️ Ошибка получения данных GitHub: {e}")
            return None
    
    def get_stackoverflow_data_real(self, language: str) -> Optional[Dict]:
        """
        Получение реальных данных Stack Overflow для языка
        
        Использует Stack Overflow API
        """
        try:
            # Маппинг тегов для Stack Overflow API
            tag_map = {
                'Python': 'python',
                'Java': 'java',
                'JavaScript': 'javascript',
                'C': 'c',
                'CPlusPlus': 'c++',
                'CSharp': 'c%23'  # URL-encoded #
            }
            
            tag = tag_map.get(language, language.lower())
            
            # Запрос к Stack Overflow API
            url = f"https://api.stackexchange.com/2.3/tags/{tag}/info?site=stackoverflow&pagesize=1"
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'items' in data and data['items']:
                    tag_info = data['items'][0]
                    
                    return {
                        'total_questions': tag_info.get('count', 0),
                        'last_updated': datetime.now().isoformat(),
                        'source': 'stackoverflow_api'
                    }
            else:
                print(f"⚠️ Ошибка Stack Overflow API: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"⚠️ Ошибка получения данных Stack Overflow: {e}")
            return None
    
    def get_wikipedia_data(self, language: str) -> Optional[Dict]:
        """
        Получение дополнительной информации из Wikipedia
        
        Парсит основную информацию о языке программирования
        """
        try:
            # Маппинг названий для Wikipedia
            wiki_map = {
                'CPlusPlus': 'C%2B%2B',
                'CSharp': 'C_Sharp_(programming_language)',
                'JavaScript': 'JavaScript'
            }
            
            wiki_name = wiki_map.get(language, language)
            url = f"https://en.wikipedia.org/wiki/{wiki_name}"
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Ищем информационную таблицу
                infobox = soup.find('table', class_='infobox')
                
                if infobox:
                    data = {}
                    
                    # Извлекаем основные данные
                    rows = infobox.find_all('tr')
                    for row in rows:
                        th = row.find('th')
                        td = row.find('td')
                        
                        if th and td:
                            key = th.get_text(strip=True)
                            value = td.get_text(strip=True)
                            data[key] = value
                    
                    return {
                        'wikipedia_data': data,
                        'wikipedia_url': url,
                        'last_updated': datetime.now().isoformat(),
                        'source': 'wikipedia'
                    }
        except Exception as e:
            print(f"⚠️ Ошибка получения данных Wikipedia: {e}")
        
        return None
    
    def _normalize_language_name(self, name: str) -> str:
        """Нормализация названия языка"""
        # Сначала очищаем имя от лишних символов
        clean_name = re.sub(r'[^\w\s#+]', '', name).strip()
        
        # Маппинг различных вариантов названий
        name_mapping = {
            'Python': 'Python',
            'python': 'Python',
            'C': 'C',
            'c': 'C',
            'C++': 'CPlusPlus',
            'C Plus Plus': 'CPlusPlus',
            'Cpp': 'CPlusPlus',
            'cpp': 'CPlusPlus',
            'Java': 'Java',
            'java': 'Java',
            'C#': 'CSharp',
            'C Sharp': 'CSharp',
            'Csharp': 'CSharp',
            'csharp': 'CSharp',
            'JavaScript': 'JavaScript',
            'javascript': 'JavaScript',
            'JS': 'JavaScript',
            'js': 'JavaScript',
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
        
        # Проверяем точное совпадение
        if clean_name in name_mapping:
            return name_mapping[clean_name]
        
        # Проверяем частичное совпадение (без учета регистра)
        clean_lower = clean_name.lower()
        for key, value in name_mapping.items():
            if key.lower() == clean_lower or key.lower() in clean_lower or clean_lower in key.lower():
                return value
        
        # Если не нашли, применяем базовую нормализацию
        normalized = clean_name.replace(' ', '').replace('#', 'Sharp').replace('++', 'PlusPlus')
        return normalized

def test_improved_fetcher():
    """Тестирование улучшенного фетчера"""
    fetcher = ImprovedDataFetcher()
    
    print("🧪 ТЕСТИРОВАНИЕ УЛУЧШЕННОГО ФЕТЧЕРА")
    print("=" * 60)
    
    # Тест TIOBE
    print("\n1. Получение данных TIOBE...")
    tiobe_data = fetcher.get_tiobe_data_real()
    if tiobe_data:
        print(f"   ✅ Получено {len(tiobe_data)} рейтингов")
        for lang in tiobe_data[:5]:
            print(f"      #{lang['rank']} {lang['name']} - {lang['rating']} ({lang['source']})")
    else:
        print("   ❌ Не удалось получить данные")
    
    # Тест GitHub
    print("\n2. Получение данных GitHub для Python...")
    github_data = fetcher.get_github_data_real("Python")
    if github_data:
        print(f"   ✅ Репозиториев: {github_data['total_repositories']}")
        print(f"   ✅ Звезд: {github_data['total_stars']}")
    else:
        print("   ❌ Не удалось получить данные")
    
    # Тест Stack Overflow
    print("\n3. Получение данных Stack Overflow для Python...")
    so_data = fetcher.get_stackoverflow_data_real("Python")
    if so_data:
        print(f"   ✅ Вопросов: {so_data['total_questions']}")
    else:
        print("   ❌ Не удалось получить данные")
    
    time.sleep(2)  # Пауза между запросами

if __name__ == "__main__":
    test_improved_fetcher()

