"""
Модуль для автоматического сбора источников информации о языках программирования
Ищет книги, статьи, документацию в различных источниках
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import re
import time

class SourceCollector:
    """Класс для автоматического сбора источников"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def find_wikipedia_sources(self, language: str) -> List[Dict]:
        """
        Поиск источников на Wikipedia странице языка
        
        Returns:
            Список словарей с информацией о книгах и статьях
        """
        print(f"📚 Поиск источников на Wikipedia для {language}...")
        
        sources = []
        
        try:
            # Маппинг названий для Wikipedia
            wiki_map = {
                'Python': 'Python_(programming_language)',
                'Java': 'Java_(programming_language)',
                'JavaScript': 'JavaScript',
                'C': 'C_(programming_language)',
                'CPlusPlus': 'C%2B%2B',
                'CSharp': 'C_Sharp_(programming_language)'
            }
            
            wiki_name = wiki_map.get(language, language.replace('+', '%2B').replace('#', '_'))
            url = f"https://en.wikipedia.org/wiki/{wiki_name}"
            
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Ищем секцию "Further reading" или "References"
                sections = soup.find_all(['section', 'div'], class_=re.compile(r'references|further.*reading', re.I))
                
                for section in sections:
                    # Ищем ссылки на книги и статьи
                    links = section.find_all('a', href=True)
                    
                    for link in links:
                        href = link.get('href', '')
                        text = link.get_text(strip=True)
                        
                        # Фильтруем служебные тексты
                        skip_texts = ['archived', 'buy now', 'the original', 'retrieved', 'cite', 
                                     'edit', 'talk', 'main article', 'see also', 'external links']
                        
                        if (href.startswith('http') and text and 
                            len(text) > 3 and 
                            text.lower() not in skip_texts and
                            not text.isdigit()):
                            sources.append({
                                'title': text[:200],  # Ограничиваем длину
                                'url': href,
                                'type': 'article',
                                'source': 'wikipedia'
                            })
                
                # Ищем инфобокс с официальными ссылками
                infobox = soup.find('table', class_='infobox')
                if infobox:
                    official_links = infobox.find_all('a', href=True)
                    for link in official_links:
                        href = link.get('href', '')
                        if 'docs' in href.lower() or 'documentation' in href.lower():
                            sources.append({
                                'title': f"{language} Official Documentation",
                                'url': href,
                                'type': 'documentation',
                                'source': 'wikipedia'
                            })
            
        except Exception as e:
            print(f"⚠️ Ошибка поиска на Wikipedia: {e}")
        
        return sources
    
    def find_github_awesome_lists(self, language: str) -> List[Dict]:
        """
        Поиск в Awesome списках на GitHub
        
        Returns:
            Список ресурсов из Awesome списков
        """
        print(f"⭐ Поиск в Awesome списках для {language}...")
        
        sources = []
        
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
            
            # Ищем Awesome списки
            url = f"https://api.github.com/search/repositories?q=awesome+{github_lang}+language:{github_lang}&sort=stars&order=desc&per_page=5"
            
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                for repo in data.get('items', []):
                    repo_name = repo['name']
                    repo_url = repo['html_url']
                    
                    sources.append({
                        'title': f"Awesome {language} - {repo_name}",
                        'url': repo_url,
                        'type': 'tutorial',
                        'source': 'github_awesome'
                    })
                    
                    # Пробуем получить README с ссылками
                    readme_url = f"https://raw.githubusercontent.com/{repo['full_name']}/master/README.md"
                    try:
                        readme_response = self.session.get(readme_url, timeout=10)
                        if readme_response.status_code == 200:
                            # Парсим ссылки из README
                            readme_text = readme_response.text
                            # Ищем ссылки в формате Markdown
                            link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
                            matches = re.findall(link_pattern, readme_text)
                            
                            for match_text, match_url in matches[:20]:  # Берем первые 20
                                # Фильтруем служебные тексты
                                skip_texts = ['archived', 'buy now', 'the original', 'back to top', 
                                             'contribute', 'license', 'stars', 'fork']
                                
                                if (match_url.startswith('http') and 
                                    match_text and 
                                    len(match_text) > 3 and
                                    match_text.lower() not in skip_texts and
                                    not match_text.isdigit()):
                                    sources.append({
                                        'title': match_text[:200],  # Ограничиваем длину
                                        'url': match_url,
                                        'type': 'article',
                                        'source': f'github_awesome_{repo_name}'
                                    })
                    except:
                        pass
            
        except Exception as e:
            print(f"⚠️ Ошибка поиска в Awesome списках: {e}")
        
        return sources
    
    def find_official_documentation(self, language: str) -> List[Dict]:
        """
        Поиск официальной документации
        
        Returns:
            Список ссылок на официальную документацию
        """
        print(f"📖 Поиск официальной документации для {language}...")
        
        sources = []
        
        # Известные официальные сайты
        official_sites = {
            'Python': [
                {'url': 'https://docs.python.org/3/', 'title': 'Python 3 Official Documentation'},
                {'url': 'https://www.python.org/about/gettingstarted/', 'title': 'Python Getting Started'}
            ],
            'Java': [
                {'url': 'https://docs.oracle.com/javase/', 'title': 'Java SE Documentation'},
                {'url': 'https://docs.oracle.com/java/', 'title': 'Java Documentation'}
            ],
            'JavaScript': [
                {'url': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript', 'title': 'MDN JavaScript Guide'},
                {'url': 'https://javascript.info/', 'title': 'The Modern JavaScript Tutorial'}
            ],
            'C': [
                {'url': 'https://en.cppreference.com/w/c', 'title': 'C Reference'},
                {'url': 'https://www.gnu.org/software/gnu-c-manual/', 'title': 'GNU C Manual'}
            ],
            'CPlusPlus': [
                {'url': 'https://en.cppreference.com/w/cpp', 'title': 'C++ Reference'},
                {'url': 'https://isocpp.org/', 'title': 'ISO C++'}
            ],
            'CSharp': [
                {'url': 'https://docs.microsoft.com/dotnet/csharp/', 'title': 'C# Documentation'},
                {'url': 'https://learn.microsoft.com/dotnet/csharp/', 'title': 'Learn C#'}
            ]
        }
        
        if language in official_sites:
            for site in official_sites[language]:
                sources.append({
                    'title': site['title'],
                    'url': site['url'],
                    'type': 'documentation',
                    'source': 'official'
                })
        
        return sources
    
    def find_popular_books(self, language: str) -> List[Dict]:
        """
        Поиск популярных книг о языке
        
        Returns:
            Список книг с информацией
        """
        print(f"📚 Поиск популярных книг для {language}...")
        
        # Известные книги по языкам
        popular_books = {
            'Python': [
                {'title': 'Fluent Python', 'author': 'Luciano Ramalho', 'isbn': '978-1491946008'},
                {'title': 'Python Tricks', 'author': 'Dan Bader', 'isbn': '978-1775093305'},
                {'title': 'Effective Python', 'author': 'Brett Slatkin', 'isbn': '978-0134853987'},
                {'title': 'Automate the Boring Stuff with Python', 'author': 'Al Sweigart', 'isbn': '978-1593279929'}
            ],
            'Java': [
                {'title': 'Effective Java', 'author': 'Joshua Bloch', 'isbn': '978-0134685991'},
                {'title': 'Java: The Complete Reference', 'author': 'Herbert Schildt', 'isbn': '978-1260440232'},
                {'title': 'Head First Java', 'author': 'Kathy Sierra', 'isbn': '978-0596009205'}
            ],
            'JavaScript': [
                {'title': 'You Don\'t Know JS', 'author': 'Kyle Simpson', 'isbn': '978-1491924464'},
                {'title': 'Eloquent JavaScript', 'author': 'Marijn Haverbeke', 'isbn': '978-1593279509'},
                {'title': 'JavaScript: The Definitive Guide', 'author': 'David Flanagan', 'isbn': '978-1491952023'}
            ],
            'C': [
                {'title': 'The C Programming Language', 'author': 'Brian Kernighan, Dennis Ritchie', 'isbn': '978-0131103627'},
                {'title': 'C Programming: A Modern Approach', 'author': 'K. N. King', 'isbn': '978-0393979503'}
            ],
            'CPlusPlus': [
                {'title': 'The C++ Programming Language', 'author': 'Bjarne Stroustrup', 'isbn': '978-0321563842'},
                {'title': 'Effective Modern C++', 'author': 'Scott Meyers', 'isbn': '978-1491903993'},
                {'title': 'C++ Primer', 'author': 'Stanley Lippman', 'isbn': '978-0321714114'}
            ],
            'CSharp': [
                {'title': 'C# in Depth', 'author': 'Jon Skeet', 'isbn': '978-1617294532'},
                {'title': 'Pro C# 8 with .NET Core 3', 'author': 'Andrew Troelsen', 'isbn': '978-1484254279'}
            ]
        }
        
        books = []
        if language in popular_books:
            for book in popular_books[language]:
                books.append({
                    'title': book['title'],
                    'author': book['author'],
                    'isbn': book.get('isbn', ''),
                    'type': 'book',
                    'source': 'popular_books'
                })
        
        return books
    
    def collect_all_sources(self, language: str) -> Dict[str, List[Dict]]:
        """
        Сбор всех источников для языка
        
        Returns:
            Словарь с источниками по типам
        """
        print(f"\n🔍 СБОР ИСТОЧНИКОВ ДЛЯ {language}")
        print("=" * 60)
        
        all_sources = {
            'books': [],
            'articles': [],
            'documentation': [],
            'tutorials': []
        }
        
        # Книги
        books = self.find_popular_books(language)
        all_sources['books'].extend(books)
        
        # Официальная документация
        docs = self.find_official_documentation(language)
        all_sources['documentation'].extend(docs)
        
        # Wikipedia источники
        wiki_sources = self.find_wikipedia_sources(language)
        for source in wiki_sources:
            if source['type'] == 'documentation':
                all_sources['documentation'].append(source)
            else:
                all_sources['articles'].append(source)
        
        # Awesome списки
        awesome_sources = self.find_github_awesome_lists(language)
        all_sources['tutorials'].extend(awesome_sources)
        
        # Пауза между запросами
        time.sleep(2)
        
        return all_sources

def test_source_collector():
    """Тестирование сборщика источников"""
    collector = SourceCollector()
    
    print("🧪 ТЕСТИРОВАНИЕ СБОРЩИКА ИСТОЧНИКОВ")
    print("=" * 60)
    
    # Собираем источники для Python
    sources = collector.collect_all_sources("Python")
    
    print(f"\n📊 РЕЗУЛЬТАТЫ:")
    print(f"   Книг: {len(sources['books'])}")
    print(f"   Статей: {len(sources['articles'])}")
    print(f"   Документации: {len(sources['documentation'])}")
    print(f"   Туториалов: {len(sources['tutorials'])}")
    
    print(f"\n📚 КНИГИ:")
    for book in sources['books'][:3]:
        print(f"   • {book['title']} by {book['author']}")
    
    print(f"\n📖 ДОКУМЕНТАЦИЯ:")
    for doc in sources['documentation'][:3]:
        print(f"   • {doc['title']}: {doc['url']}")

if __name__ == "__main__":
    test_source_collector()

