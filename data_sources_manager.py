import requests
import json
import time
from datetime import datetime
from rdflib import Graph, Namespace, RDF, Literal

try:
    from github_config import GITHUB_TOKEN
except ImportError:
    GITHUB_TOKEN = None
    print("⚠️ GitHub token не найден. Создайте github_config.py с GITHUB_TOKEN")

class DataSourcesManager:
    def __init__(self, ontology_manager):
        self.om = ontology_manager
        self.NS = ontology_manager.NS
        self.session = requests.Session()
        
        # Настройки API
        self.github_token = GITHUB_TOKEN
        if self.github_token:
            print("✅ GitHub token загружен")
        else:
            print("⚠️ GitHub token отсутствует - будут использоваться демо-данные")
        self.stackoverflow_key = None
        
        # Настройки запросов
        self.request_timeout = 15
        self.retry_attempts = 2
        
    def update_all_sources(self, use_extended_sources=True):
        """Обновление данных из всех источников - ТОЛЬКО 6 языков"""
        print("🚀 ОБНОВЛЕНИЕ ДАННЫХ ИЗ ВСЕХ ИСТОЧНИКОВ")
        print("=" * 60)
        
        # Сначала получаем TIOBE данные
        print("\n🏆 Получение TIOBE данных...")
        from tiobe_importer import TIOBEImporter
        tiobe_importer = TIOBEImporter(self.om)
        tiobe_data = tiobe_importer.scrape_tiobe_ranking(use_demo_fallback=True)
        
        # Фильтруем TIOBE данные - оставляем только наши 6 языков
        if tiobe_data:
            filtered_tiobe = []
            target_languages = ['Python', 'Java', 'JavaScript', 'C', 'CPlusPlus', 'CSharp']
            for lang_data in tiobe_data:
                if lang_data['name'] in target_languages:
                    filtered_tiobe.append(lang_data)
            tiobe_data = filtered_tiobe
            print(f"📋 Фильтр TIOBE: оставлено {len(filtered_tiobe)} из 6 языков")
        
        results = {}
        
        # 1. GitHub данные с улучшенной обработкой
        print("\n🔮 GitHub данные...")
        github_data = self.get_github_stats_improved()
        results['github'] = github_data
        
        # 2. Stack Overflow данные с исправлением C#
        print("\n📚 Stack Overflow данные...")
        stackoverflow_data = self.get_stackoverflow_stats_improved()
        results['stackoverflow'] = stackoverflow_data
        
        # 3. TIOBE данные
        results['tiobe'] = tiobe_data or []
        
        # 4. Расширенные источники (опционально)
        if use_extended_sources:
            try:
                print("\n📊 Расширенные источники данных...")
                from extended_data_sources import ExtendedDataSources
                extended_fetcher = ExtendedDataSources()
                
                # Получаем данные из PYPL, RedMonk, IEEE Spectrum
                pypl_data = extended_fetcher.get_pypl_data()
                if pypl_data:
                    results['pypl'] = pypl_data
                    print(f"   ✅ PYPL: {len(pypl_data)} рейтингов")
                
                redmonk_data = extended_fetcher.get_redmonk_data()
                if redmonk_data:
                    results['redmonk'] = redmonk_data
                    print(f"   ✅ RedMonk: {len(redmonk_data)} рейтингов")
                
                ieee_data = extended_fetcher.get_ieee_spectrum_data()
                if ieee_data:
                    results['ieee_spectrum'] = ieee_data
                    print(f"   ✅ IEEE Spectrum: {len(ieee_data)} рейтингов")
                
            except ImportError:
                print("   ⚠️ Расширенные источники не доступны")
            except Exception as e:
                print(f"   ⚠️ Ошибка расширенных источников: {e}")
        
        # Обновляем онтологию
        updated_count = self._update_ontology_with_all_data(results)
        
        print(f"\n📊 ИТОГО: Обновлено {updated_count} записей из {len(results)} источников")
        return results

    def get_github_stats_improved(self):
        """Получение статистики с GitHub - улучшенная версия с использованием ImprovedDataFetcher"""
        languages_data = {}
        
        try:
            # ТОЛЬКО 6 основных языков
            language_map = {
                'python': 'Python',
                'java': 'Java',
                'javascript': 'JavaScript',
                'c': 'C',
                'cpp': 'CPlusPlus',
                'csharp': 'CSharp'
            }
            
            # Пробуем использовать улучшенный фетчер
            try:
                from improved_data_fetcher import ImprovedDataFetcher
                fetcher = ImprovedDataFetcher()
                
                for lang_key, lang_name in language_map.items():
                    print(f"   📦 GitHub: {lang_name}...")
                    github_data = fetcher.get_github_data_real(lang_name)
                    
                    if github_data:
                        languages_data[lang_key] = github_data
                        print(f"      ✅ {lang_name}: {github_data['total_repositories']} repos")
                    else:
                        # Fallback на старый метод
                        languages_data[lang_key] = self._get_github_data_old_method(lang_key)
                        
                    time.sleep(1)  # Пауза между запросами
                
                return languages_data
            except ImportError:
                print("   ⚠️ ImprovedDataFetcher не найден, используем старый метод")
            
            # Старый метод (fallback)
            for lang in language_map.keys():
                languages_data[lang] = self._get_github_data_old_method(lang)
                time.sleep(1)
                    
        except Exception as e:
            print(f"❌ Общая ошибка GitHub API: {e}")
            # Возвращаем демо-данные при ошибке
            for lang in language_map.keys():
                if lang not in languages_data:
                    languages_data[lang] = self._get_github_demo_data(lang)
        
        return languages_data
    
    def _get_github_data_old_method(self, lang):
        """Старый метод получения данных GitHub (fallback)"""
        try:
            url = f"https://api.github.com/search/repositories?q=language:{lang}&sort=stars&order=desc&per_page=3"
            
            headers = {
                'User-Agent': 'ProgrammingLanguageOntology/1.0',
                'Accept': 'application/vnd.github.v3+json'
            }
            if self.github_token:
                headers['Authorization'] = f'token {self.github_token}'
            
            response = self.session.get(url, headers=headers, timeout=self.request_timeout)
            
            if response.status_code == 200:
                data = response.json()
                total_repos = data['total_count']
                top_repos = data['items'][:3] if data['items'] else []
                total_stars = sum(repo['stargazers_count'] for repo in top_repos)
                avg_stars = total_stars / len(top_repos) if top_repos else 0
                
                return {
                    'total_repositories': total_repos,
                    'total_stars': total_stars,
                    'average_stars': round(avg_stars, 1),
                    'top_repositories': [repo['name'] for repo in top_repos],
                    'last_updated': datetime.now().isoformat(),
                    'source': 'github_api'
                }
            else:
                return self._get_github_demo_data(lang)
        except:
            return self._get_github_demo_data(lang)

    def get_stackoverflow_stats_improved(self):
        """Получение статистики с Stack Overflow - улучшенная версия с использованием ImprovedDataFetcher"""
        languages_data = {}
    
        try:
            language_map = {
                'python': 'Python',
                'java': 'Java',
                'javascript': 'JavaScript',
                'c': 'C',
                'cpp': 'CPlusPlus',
                'csharp': 'CSharp'
            }
            
            # Пробуем использовать улучшенный фетчер
            try:
                from improved_data_fetcher import ImprovedDataFetcher
                fetcher = ImprovedDataFetcher()
                
                for lang_key, lang_name in language_map.items():
                    print(f"   💬 Stack Overflow: {lang_name}...")
                    so_data = fetcher.get_stackoverflow_data_real(lang_name)
                    
                    if so_data:
                        languages_data[lang_key] = so_data
                        print(f"      ✅ {lang_name}: {so_data['total_questions']} вопросов")
                    else:
                        # Fallback на старый метод
                        languages_data[lang_key] = self._get_stackoverflow_data_old_method(lang_key)
                    
                    time.sleep(1.5)  # Уважаем rate limit
                
                return languages_data
            except ImportError:
                print("   ⚠️ ImprovedDataFetcher не найден, используем старый метод")
            
            # Старый метод (fallback)
            for lang_key in language_map.keys():
                languages_data[lang_key] = self._get_stackoverflow_data_old_method(lang_key)
                time.sleep(1.5)
            
        except Exception as e:
            print(f"❌ Общая ошибка Stack Overflow: {e}")
            for lang in language_map.keys():
                if lang not in languages_data:
                    languages_data[lang] = self._get_stackoverflow_demo_data(lang)
    
        return languages_data
    
    def _get_stackoverflow_data_old_method(self, lang_key):
        """Старый метод получения данных Stack Overflow (fallback)"""
        language_tags = {
            'python': 'python',
            'java': 'java',
            'javascript': 'javascript', 
            'c': 'c',
            'cpp': 'c++',
            'csharp': 'c%23'
        }
        
        tag = language_tags.get(lang_key, lang_key)
        
        try:
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
        except:
            pass
        
        return self._get_stackoverflow_demo_data(lang_key)
    
    def _update_ontology_with_all_data(self, all_data):
        """Обновление онтологии данными из всех источников - ТОЛЬКО 6 языков"""
        updated_count = 0
        
        # Маппинг названий языков - ТОЛЬКО 6 языков
        name_mapping = {
            'python': 'Python',
            'java': 'Java',
            'javascript': 'JavaScript',
            'c': 'C',
            'cpp': 'CPlusPlus',
            'cplusplus': 'CPlusPlus',
            'csharp': 'CSharp'
        }
        
        for source_name, source_data in all_data.items():
            print(f"\n📝 Обновление из {source_name}...")
            
            # Обрабатываем разные форматы данных
            if source_name == 'tiobe':
                # TIOBE данные - список словарей
                updated_count += self._process_tiobe_data(source_data)
            elif source_name == 'github':
                # GitHub данные - словарь
                updated_count += self._process_github_data(source_data, name_mapping)
            elif source_name == 'stackoverflow':
                # Stack Overflow данные - словарь
                updated_count += self._process_stackoverflow_data(source_data, name_mapping)
        
        return updated_count

    def _process_tiobe_data(self, tiobe_data):
        """Обработка TIOBE данных (список) - ТОЛЬКО 6 языков"""
        updated_count = 0
        
        for lang_data in tiobe_data:
            lang_name = lang_data['name']
            
            # Проверяем существует ли язык в онтологии
            if not self.om.language_exists(lang_name):
                print(f"   ⚠️ Язык {lang_name} не найден в онтологии")
                continue
            
            # Обновляем TIOBE данные
            success = self.om.update_language_ranking(
                lang_name, 
                lang_data['rank'], 
                lang_data['rating']
            )
            
            if success:
                updated_count += 1
                print(f"   ✅ TIOBE: {lang_name} - #{lang_data['rank']} ({lang_data['rating']})")
        
        return updated_count

    def _process_github_data(self, github_data, name_mapping):
        """Обработка GitHub данных (словарь) - ТОЛЬКО 6 языков"""
        updated_count = 0
        
        for lang_key, lang_data in github_data.items():
            # Получаем нормализованное имя языка
            normalized_name = name_mapping.get(lang_key)
            if not normalized_name:
                continue
            
            # Проверяем существует ли язык в онтологии
            if not self.om.language_exists(normalized_name):
                print(f"   ⚠️ Язык {normalized_name} не найден в онтологии")
                continue
            
            # Обновляем GitHub данные
            success = self._update_github_data(normalized_name, lang_data)
            if success:
                updated_count += 1
        
        return updated_count

    def _process_stackoverflow_data(self, stackoverflow_data, name_mapping):
        """Обработка Stack Overflow данных (словарь) - ТОЛЬКО 6 языков"""
        updated_count = 0
        
        for lang_key, lang_data in stackoverflow_data.items():
            # Получаем нормализованное имя языка
            normalized_name = name_mapping.get(lang_key)
            if not normalized_name:
                continue
            
            # Проверяем существует ли язык в онтологии
            if not self.om.language_exists(normalized_name):
                print(f"   ⚠️ Язык {normalized_name} не найден в онтологии")
                continue
            
            # Обновляем Stack Overflow данные
            success = self._update_stackoverflow_data(normalized_name, lang_data)
            if success:
                updated_count += 1
        
        return updated_count

    def _get_github_demo_data(self, language):
        """Демо-данные GitHub - ТОЛЬКО 6 языков"""
        demo_data = {
            'python': {'total_repositories': 4500000, 'total_stars': 850000, 'average_stars': 245.5},
            'java': {'total_repositories': 1200000, 'total_stars': 320000, 'average_stars': 156.2},
            'javascript': {'total_repositories': 3800000, 'total_stars': 720000, 'average_stars': 189.3},
            'c': {'total_repositories': 850000, 'total_stars': 180000, 'average_stars': 98.7},
            'cpp': {'total_repositories': 950000, 'total_stars': 210000, 'average_stars': 112.4},
            'csharp': {'total_repositories': 1100000, 'total_stars': 280000, 'average_stars': 134.8}
        }
        
        data = demo_data.get(language, {'total_repositories': 100000, 'total_stars': 50000, 'average_stars': 100.0})
        data['top_repositories'] = [f"awesome-{language}", f"{language}-project", f"{language}-framework"]
        data['last_updated'] = datetime.now().isoformat()
        data['source'] = 'github_demo'
        
        return data

    def _get_stackoverflow_demo_data(self, language):
        """Демо-данные Stack Overflow - ТОЛЬКО 6 языков"""
        demo_data = {
            'python': {'total_questions': 2150000},
            'java': {'total_questions': 1850000},
            'javascript': {'total_questions': 2450000},
            'c': {'total_questions': 850000},
            'cpp': {'total_questions': 920000},
            'csharp': {'total_questions': 1650000}
        }
        
        data = demo_data.get(language, {'total_questions': 100000})
        data['is_required'] = False
        data['is_moderator_only'] = False
        data['last_updated'] = datetime.now().isoformat()
        data['source'] = 'stackoverflow_demo'
        
        return data

    def _update_github_data(self, language_name, github_data):
        """Обновление GitHub данных в онтологии"""
        try:
            lang_uri = self.NS[language_name]
            
            # Удаляем старые GitHub данные
            self.om.g.remove((lang_uri, self.NS.githubRepositories, None))
            self.om.g.remove((lang_uri, self.NS.githubStars, None))
            self.om.g.remove((lang_uri, self.NS.githubAvgStars, None))
            self.om.g.remove((lang_uri, self.NS.githubLastUpdated, None))
            
            # Добавляем новые данные
            self.om.g.add((lang_uri, self.NS.githubRepositories, Literal(github_data['total_repositories'])))
            self.om.g.add((lang_uri, self.NS.githubStars, Literal(github_data['total_stars'])))
            self.om.g.add((lang_uri, self.NS.githubAvgStars, Literal(github_data['average_stars'])))
            self.om.g.add((lang_uri, self.NS.githubLastUpdated, Literal(github_data['last_updated'])))
            
            source_type = github_data.get('source', 'unknown')
            print(f"   ✅ GitHub: {language_name} - {github_data['total_repositories']} repos ({source_type})")
            return True
            
        except Exception as e:
            print(f"   ❌ Ошибка обновления GitHub для {language_name}: {e}")
            return False

    def _update_stackoverflow_data(self, language_name, stackoverflow_data):
        """Обновление Stack Overflow данных в онтологии"""
        try:
            lang_uri = self.NS[language_name]
            
            # Удаляем старые Stack Overflow данные
            self.om.g.remove((lang_uri, self.NS.stackOverflowQuestions, None))
            self.om.g.remove((lang_uri, self.NS.stackOverflowLastUpdated, None))
            
            # Добавляем новые данные
            self.om.g.add((lang_uri, self.NS.stackOverflowQuestions, Literal(stackoverflow_data['total_questions'])))
            self.om.g.add((lang_uri, self.NS.stackOverflowLastUpdated, Literal(stackoverflow_data['last_updated'])))
            
            source_type = stackoverflow_data.get('source', 'unknown')
            print(f"   ✅ Stack Overflow: {language_name} - {stackoverflow_data['total_questions']} вопросов ({source_type})")
            return True
            
        except Exception as e:
            print(f"   ❌ Ошибка обновления Stack Overflow для {language_name}: {e}")
            return False

def test_data_sources():
    """Тестирование системы сбора данных - ТОЛЬКО 6 языков"""
    from ontology_manager import OntologyManager
    
    print("🧪 ТЕСТИРОВАНИЕ СИСТЕМЫ СБОРА ДАННЫХ (6 ЯЗЫКОВ)")
    print("=" * 60)
    
    # Загружаем онтологию
    om = OntologyManager(r"D:\OneDrive\Рабочий стол\tiobe_importer\data\programming_languages.ttl")
    
    # Создаем менеджер источников данных
    data_manager = DataSourcesManager(om)
    
    # Обновляем данные из всех источников
    results = data_manager.update_all_sources()
    
    # Сохраняем онтологию
    if om.save_ontology():
        print(f"\n💾 Онтология сохранена с данными из {len(results)} источников!")
        
        # Анализируем источники данных
        print("\n📊 АНАЛИЗ ИСТОЧНИКОВ ДАННЫХ:")
        for source, data in results.items():
            if source == 'tiobe':
                print(f"   • {source}: {len(data)} языков")
            else:
                real_count = sum(1 for lang_data in data.values() 
                               if lang_data.get('source', '').endswith('_api'))
                demo_count = len(data) - real_count
                print(f"   • {source}: {len(data)} языков ({real_count} реальных, {demo_count} демо)")
    
    return results

if __name__ == "__main__":
    test_data_sources()