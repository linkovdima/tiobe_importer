"""
Расширенный модуль получения данных из множества реальных источников
Включает: PYPL, RedMonk, IEEE Spectrum, GitHub Octoverse, npm/pypi, Google Trends и др.
"""
import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
import re
import csv
from io import StringIO

class ExtendedDataSources:
    """Класс для получения данных из расширенного набора источников"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    # ========== PYPL (PopularitY of Programming Language) ==========
    
    def get_pypl_data(self) -> Optional[List[Dict]]:
        """
        Получение данных PYPL - рейтинг популярности языков программирования
        Основан на анализе поисковых запросов в Google для учебных материалов
        
        Источник: https://pypl.github.io/PYPL.html
        """
        print("📊 Получение данных PYPL...")
        
        try:
            url = "https://pypl.github.io/PYPL.html"
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Ищем таблицу с рейтингами
                tables = soup.find_all('table')
                
                for table in tables:
                    rows = table.find_all('tr')[1:21]  # Первые 20 строк
                    rankings = []
                    
                    for i, row in enumerate(rows, 1):
                        cols = row.find_all('td')
                        if len(cols) >= 2:
                            try:
                                name_text = cols[0].get_text(strip=True)
                                share_text = cols[1].get_text(strip=True) if len(cols) > 1 else ""
                                
                                if name_text:
                                    normalized = self._normalize_language_name(name_text)
                                    rankings.append({
                                        'rank': i,
                                        'name': normalized,
                                        'share': share_text,
                                        'original_name': name_text,
                                        'source': 'pypl'
                                    })
                            except:
                                continue
                    
                    if len(rankings) >= 5:
                        print(f"✅ Получено {len(rankings)} рейтингов с PYPL")
                        return rankings
        except Exception as e:
            print(f"⚠️ Ошибка получения PYPL: {e}")
        
        return None
    
    # ========== RedMonk Rankings ==========
    
    def get_redmonk_data(self) -> Optional[List[Dict]]:
        """
        Получение данных RedMonk Rankings
        Комбинирует данные GitHub и Stack Overflow
        
        Источник: https://redmonk.com/sogrady/category/programming-languages/
        """
        print("📊 Получение данных RedMonk...")
        
        try:
            # RedMonk публикует рейтинги в виде статей/блогов
            # Пробуем найти последний рейтинг
            url = "https://redmonk.com/sogrady/category/programming-languages/"
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Ищем ссылки на статьи с рейтингами
                articles = soup.find_all('article') or soup.find_all('div', class_='post')
                
                for article in articles[:3]:  # Проверяем первые 3 статьи
                    title_elem = article.find('h2') or article.find('h1') or article.find('a')
                    if title_elem and 'rankings' in title_elem.get_text().lower():
                        link = title_elem.find('a') if title_elem.find('a') else article.find('a')
                        if link and link.get('href'):
                            article_url = link['href']
                            if not article_url.startswith('http'):
                                article_url = f"https://redmonk.com{article_url}"
                            
                            # Парсим статью с рейтингом
                            rankings = self._parse_redmonk_article(article_url)
                            if rankings:
                                return rankings
        except Exception as e:
            print(f"⚠️ Ошибка получения RedMonk: {e}")
        
        return None
    
    def _parse_redmonk_article(self, url: str) -> Optional[List[Dict]]:
        """Парсинг статьи RedMonk с рейтингом"""
        try:
            response = self.session.get(url, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Ищем таблицы или списки с рейтингами
                tables = soup.find_all('table')
                for table in tables:
                    rows = table.find_all('tr')[1:]
                    rankings = []
                    
                    for i, row in enumerate(rows, 1):
                        cols = row.find_all(['td', 'th'])
                        if len(cols) >= 2:
                            try:
                                rank_text = cols[0].get_text(strip=True)
                                name_text = cols[1].get_text(strip=True)
                                
                                if name_text and name_text[0].isdigit():
                                    # Может быть формат "1. Python"
                                    parts = name_text.split('.', 1)
                                    if len(parts) == 2:
                                        rank = int(parts[0])
                                        name = parts[1].strip()
                                    else:
                                        rank = i
                                        name = name_text
                                else:
                                    rank = i
                                    name = name_text
                                
                                normalized = self._normalize_language_name(name)
                                rankings.append({
                                    'rank': rank,
                                    'name': normalized,
                                    'original_name': name,
                                    'source': 'redmonk'
                                })
                            except:
                                continue
                    
                    if len(rankings) >= 5:
                        print(f"✅ Получено {len(rankings)} рейтингов с RedMonk")
                        return rankings
        except Exception as e:
            print(f"⚠️ Ошибка парсинга статьи RedMonk: {e}")
        
        return None
    
    # ========== IEEE Spectrum Rankings ==========
    
    def get_ieee_spectrum_data(self) -> Optional[List[Dict]]:
        """
        Получение данных IEEE Spectrum Top Programming Languages
        Комплексный рейтинг на основе множества метрик
        
        Источник: https://spectrum.ieee.org/top-programming-languages/
        """
        print("📊 Получение данных IEEE Spectrum...")
        
        try:
            url = "https://spectrum.ieee.org/top-programming-languages/"
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Ищем таблицу или список языков
                tables = soup.find_all('table')
                lists = soup.find_all(['ol', 'ul'])
                
                # Пробуем таблицы
                for table in tables:
                    rankings = self._parse_ranking_table(table)
                    if rankings:
                        print(f"✅ Получено {len(rankings)} рейтингов с IEEE Spectrum")
                        return rankings
                
                # Пробуем списки
                for list_elem in lists:
                    items = list_elem.find_all('li')
                    if len(items) >= 5:
                        rankings = []
                        for i, item in enumerate(items[:20], 1):
                            text = item.get_text(strip=True)
                            # Формат может быть "1. Python" или просто "Python"
                            match = re.match(r'(\d+)\.?\s*(.+)', text)
                            if match:
                                rank = int(match.group(1))
                                name = match.group(2).strip()
                            else:
                                rank = i
                                name = text
                            
                            normalized = self._normalize_language_name(name)
                            rankings.append({
                                'rank': rank,
                                'name': normalized,
                                'original_name': name,
                                'source': 'ieee_spectrum'
                            })
                        
                        if len(rankings) >= 5:
                            print(f"✅ Получено {len(rankings)} рейтингов с IEEE Spectrum")
                            return rankings
        except Exception as e:
            print(f"⚠️ Ошибка получения IEEE Spectrum: {e}")
        
        return None
    
    # ========== Package Managers Statistics ==========
    
    def get_npm_stats(self, language: str = "JavaScript") -> Optional[Dict]:
        """
        Получение статистики npm пакетов для JavaScript/TypeScript
        
        Источник: npm API и npmjs.com
        """
        if language not in ["JavaScript", "TypeScript"]:
            return None
        
        print(f"📦 Получение статистики npm для {language}...")
        
        try:
            # Используем npm registry API
            url = "https://registry.npmjs.org/-/v1/search"
            params = {
                'text': 'keywords:javascript',
                'size': 1
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                total_packages = data.get('total', 0)
                
                return {
                    'total_packages': total_packages,
                    'source': 'npm_registry',
                    'last_updated': datetime.now().isoformat()
                }
        except Exception as e:
            print(f"⚠️ Ошибка получения npm статистики: {e}")
        
        return None
    
    def get_pypi_stats(self, language: str = "Python") -> Optional[Dict]:
        """
        Получение статистики PyPI пакетов для Python
        
        Источник: PyPI API (pypi.org)
        """
        if language != "Python":
            return None
        
        print(f"📦 Получение статистики PyPI для {language}...")
        
        try:
            # PyPI JSON API
            url = "https://pypi.org/pypi"
            response = self.session.get(url, timeout=10)
            
            # Альтернативно: используем статистику из HTML
            url_stats = "https://pypi.org/stats/"
            response = self.session.get(url_stats, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Ищем статистику пакетов
                stats_text = soup.get_text()
                
                # Ищем числа в тексте (например "Total packages: 500000")
                package_match = re.search(r'(\d+[\d,]*)\s*(?:total\s*)?packages?', stats_text, re.I)
                if package_match:
                    total_packages = int(package_match.group(1).replace(',', ''))
                    
                    return {
                        'total_packages': total_packages,
                        'source': 'pypi_stats',
                        'last_updated': datetime.now().isoformat()
                    }
        except Exception as e:
            print(f"⚠️ Ошибка получения PyPI статистики: {e}")
        
        return None
    
    # ========== GitHub Trending ==========
    
    def get_github_trending(self, language: str, timeframe: str = "daily") -> Optional[List[Dict]]:
        """
        Получение трендовых репозиториев GitHub для языка
        
        Источник: GitHub Trending (парсинг HTML)
        timeframe: daily, weekly, monthly
        """
        print(f"🔥 Получение GitHub Trending для {language}...")
        
        try:
            github_lang_map = {
                'Python': 'python',
                'Java': 'java',
                'JavaScript': 'javascript',
                'C': 'c',
                'CPlusPlus': 'cpp',
                'CSharp': 'csharp'
            }
            
            github_lang = github_lang_map.get(language, language.lower())
            
            url = f"https://github.com/trending/{github_lang}?since={timeframe}"
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                repos = []
                repo_elements = soup.find_all('article', class_='Box-row') or soup.find_all('div', class_='Box-row')
                
                for repo_elem in repo_elements[:10]:  # Топ 10
                    try:
                        # Название репозитория
                        title_elem = repo_elem.find('h2') or repo_elem.find('h1')
                        if title_elem:
                            link = title_elem.find('a')
                            if link:
                                repo_name = link.get_text(strip=True)
                                repo_url = f"https://github.com{link.get('href', '')}"
                                
                                # Звезды
                                stars_elem = repo_elem.find(string=re.compile(r'stars?', re.I))
                                stars = 0
                                if stars_elem:
                                    stars_text = stars_elem.find_parent().get_text() if hasattr(stars_elem, 'find_parent') else str(stars_elem)
                                    stars_match = re.search(r'(\d+[\d,]*)\s*stars?', stars_text, re.I)
                                    if stars_match:
                                        stars = int(stars_match.group(1).replace(',', ''))
                                
                                repos.append({
                                    'name': repo_name,
                                    'url': repo_url,
                                    'stars': stars,
                                    'language': language
                                })
                    except:
                        continue
                
                if repos:
                    print(f"✅ Получено {len(repos)} трендовых репозиториев")
                    return repos
        except Exception as e:
            print(f"⚠️ Ошибка получения GitHub Trending: {e}")
        
        return None
    
    # ========== Rosetta Code ==========
    
    def get_rosetta_code_stats(self, language: str) -> Optional[Dict]:
        """
        Получение статистики примеров кода из Rosetta Code
        
        Источник: rosettacode.org
        """
        print(f"📚 Получение статистики Rosetta Code для {language}...")
        
        try:
            lang_map = {
                'Python': 'Python',
                'Java': 'Java',
                'JavaScript': 'JavaScript',
                'C': 'C',
                'CPlusPlus': 'C%2B%2B',
                'CSharp': 'C_sharp'
            }
            
            rosetta_lang = lang_map.get(language, language.replace('+', '%2B').replace('#', '_'))
            
            url = f"https://rosettacode.org/wiki/Category:{rosetta_lang}"
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Ищем количество задач/примеров
                # Обычно это указано в тексте страницы
                page_text = soup.get_text()
                
                # Ищем паттерны типа "X tasks" или "X programming examples"
                tasks_match = re.search(r'(\d+)\s*(?:tasks?|programming\s*examples?)', page_text, re.I)
                if tasks_match:
                    tasks_count = int(tasks_match.group(1))
                    
                    return {
                        'tasks_count': tasks_count,
                        'source': 'rosetta_code',
                        'last_updated': datetime.now().isoformat()
                    }
        except Exception as e:
            print(f"⚠️ Ошибка получения Rosetta Code статистики: {e}")
        
        return None
    
    # ========== Google Trends (упрощенный) ==========
    
    def get_google_trends_info(self, language: str) -> Optional[Dict]:
        """
        Получение информации о популярности поисковых запросов
        
        Примечание: Полный API Google Trends требует специальных библиотек
        Здесь используется упрощенный подход через публичные данные
        """
        print(f"📈 Получение Google Trends данных для {language}...")
        
        try:
            # Google Trends не предоставляет прямой API
            # Можно использовать альтернативные сервисы или парсинг
            # Для демонстрации возвращаем структуру данных
            
            lang_map = {
                'Python': 'python programming',
                'Java': 'java programming',
                'JavaScript': 'javascript programming',
                'C': 'c programming',
                'CPlusPlus': 'c++ programming',
                'CSharp': 'c# programming'
            }
            
            search_term = lang_map.get(language, f"{language} programming")
            
            # Здесь можно интегрировать библиотеку pytrends или использовать альтернативные API
            # Для примера возвращаем структуру
            
            return {
                'search_term': search_term,
                'note': 'Для полной интеграции требуется библиотека pytrends',
                'source': 'google_trends',
                'last_updated': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"⚠️ Ошибка получения Google Trends: {e}")
        
        return None
    
    # ========== Вспомогательные методы ==========
    
    def _parse_ranking_table(self, table) -> Optional[List[Dict]]:
        """Парсинг таблицы с рейтингами"""
        rankings = []
        rows = table.find_all('tr')[1:]  # Пропускаем заголовок
        
        for i, row in enumerate(rows, 1):
            cols = row.find_all(['td', 'th'])
            if len(cols) >= 2:
                try:
                    rank_text = cols[0].get_text(strip=True)
                    name_text = cols[1].get_text(strip=True)
                    
                    # Извлекаем ранг
                    rank_match = re.search(r'(\d+)', rank_text)
                    rank = int(rank_match.group(1)) if rank_match else i
                    
                    if name_text:
                        normalized = self._normalize_language_name(name_text)
                        rankings.append({
                            'rank': rank,
                            'name': normalized,
                            'original_name': name_text,
                            'source': 'table_parse'
                        })
                except:
                    continue
        
        return rankings if len(rankings) >= 5 else None
    
    def _normalize_language_name(self, name: str) -> str:
        """Нормализация названия языка"""
        name_mapping = {
            'Python': 'Python',
            'C': 'C',
            'C++': 'CPlusPlus',
            'C#': 'CSharp',
            'Java': 'Java',
            'JavaScript': 'JavaScript',
            'TypeScript': 'TypeScript',
            'Go': 'Go',
            'Rust': 'Rust',
            'Swift': 'Swift',
            'Kotlin': 'Kotlin',
            'PHP': 'PHP',
            'Ruby': 'Ruby',
            'R': 'R',
            'Scala': 'Scala',
            'Perl': 'Perl'
        }
        
        clean_name = re.sub(r'[^\w\s#+]', '', name).strip()
        return name_mapping.get(clean_name, clean_name.replace(' ', '').replace('#', 'Sharp').replace('++', 'PlusPlus'))
    
    def get_all_sources_data(self, language: str) -> Dict:
        """
        Получение данных из всех доступных источников для конкретного языка
        
        Returns:
            Словарь с данными из всех источников
        """
        all_data = {
            'language': language,
            'sources': {}
        }
        
        # PYPL
        pypl_data = self.get_pypl_data()
        if pypl_data:
            lang_data = next((item for item in pypl_data if item['name'] == language), None)
            if lang_data:
                all_data['sources']['pypl'] = lang_data
        
        # RedMonk
        redmonk_data = self.get_redmonk_data()
        if redmonk_data:
            lang_data = next((item for item in redmonk_data if item['name'] == language), None)
            if lang_data:
                all_data['sources']['redmonk'] = lang_data
        
        # IEEE Spectrum
        ieee_data = self.get_ieee_spectrum_data()
        if ieee_data:
            lang_data = next((item for item in ieee_data if item['name'] == language), None)
            if lang_data:
                all_data['sources']['ieee_spectrum'] = lang_data
        
        # Package managers
        if language == "Python":
            pypi_data = self.get_pypi_stats(language)
            if pypi_data:
                all_data['sources']['pypi'] = pypi_data
        
        if language in ["JavaScript", "TypeScript"]:
            npm_data = self.get_npm_stats(language)
            if npm_data:
                all_data['sources']['npm'] = npm_data
        
        # GitHub Trending
        trending_data = self.get_github_trending(language)
        if trending_data:
            all_data['sources']['github_trending'] = trending_data
        
        # Rosetta Code
        rosetta_data = self.get_rosetta_code_stats(language)
        if rosetta_data:
            all_data['sources']['rosetta_code'] = rosetta_data
        
        # Google Trends
        trends_data = self.get_google_trends_info(language)
        if trends_data:
            all_data['sources']['google_trends'] = trends_data
        
        return all_data

def test_extended_sources():
    """Тестирование расширенных источников данных"""
    fetcher = ExtendedDataSources()
    
    print("🧪 ТЕСТИРОВАНИЕ РАСШИРЕННЫХ ИСТОЧНИКОВ ДАННЫХ")
    print("=" * 60)
    
    # Тест PYPL
    print("\n1. Тест PYPL...")
    pypl_data = fetcher.get_pypl_data()
    if pypl_data:
        print(f"   ✅ Получено {len(pypl_data)} рейтингов")
        for lang in pypl_data[:5]:
            print(f"      #{lang['rank']} {lang['name']}")
    
    # Тест RedMonk
    print("\n2. Тест RedMonk...")
    redmonk_data = fetcher.get_redmonk_data()
    if redmonk_data:
        print(f"   ✅ Получено {len(redmonk_data)} рейтингов")
        for lang in redmonk_data[:5]:
            print(f"      #{lang['rank']} {lang['name']}")
    
    # Тест IEEE Spectrum
    print("\n3. Тест IEEE Spectrum...")
    ieee_data = fetcher.get_ieee_spectrum_data()
    if ieee_data:
        print(f"   ✅ Получено {len(ieee_data)} рейтингов")
        for lang in ieee_data[:5]:
            print(f"      #{lang['rank']} {lang['name']}")
    
    # Тест PyPI
    print("\n4. Тест PyPI для Python...")
    pypi_data = fetcher.get_pypi_stats("Python")
    if pypi_data:
        print(f"   ✅ Пакетов: {pypi_data.get('total_packages', 'N/A')}")
    
    # Тест GitHub Trending
    print("\n5. Тест GitHub Trending для Python...")
    trending_data = fetcher.get_github_trending("Python")
    if trending_data:
        print(f"   ✅ Трендовых репозиториев: {len(trending_data)}")
        for repo in trending_data[:3]:
            print(f"      • {repo['name']} ({repo['stars']} stars)")
    
    # Тест всех источников для Python
    print("\n6. Тест всех источников для Python...")
    all_data = fetcher.get_all_sources_data("Python")
    print(f"   ✅ Источников данных: {len(all_data['sources'])}")
    for source_name, source_data in all_data['sources'].items():
        print(f"      • {source_name}: {type(source_data).__name__}")

if __name__ == "__main__":
    test_extended_sources()

