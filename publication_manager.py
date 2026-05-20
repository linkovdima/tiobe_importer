"""
Модуль для управления публикациями и источниками в онтологии
Позволяет добавлять книги, статьи, ссылки, документацию
"""
from rdflib import Graph, Namespace, RDF, RDFS, Literal, URIRef
from rdflib.namespace import XSD, OWL
from typing import Dict, List, Optional
from datetime import datetime
import re
from config import ONTOLOGY_PATH

class PublicationManager:
    """Класс для управления публикациями в онтологии"""
    
    def __init__(self, ontology_path=None):
        self.g = Graph()
        self.ontology_path = ontology_path or ONTOLOGY_PATH
        self.NS = Namespace("http://www.semanticweb.org/дмитрий/ontologies/2025/10/untitled-ontology-7/")
        self.OWL = Namespace("http://www.w3.org/2002/07/owl#")
        self.load_ontology()
    
    def load_ontology(self):
        """Загрузка онтологии"""
        try:
            self.g.parse(str(self.ontology_path), format="turtle")
            print(f"✅ Онтология загружена: {len(self.g)} триплов")
            return True
        except Exception as e:
            print(f"❌ Ошибка загрузки онтологии: {e}")
            return False
    
    def add_book(self, title: str, language: str, author: Optional[str] = None, 
                 isbn: Optional[str] = None, keywords: Optional[str] = None,
                 description: Optional[str] = None, url: Optional[str] = None,
                 year: Optional[int] = None, difficulty: Optional[str] = None) -> bool:
        """
        Добавление книги в онтологию
        
        Args:
            title: Название книги
            language: Язык программирования (Python, Java, etc.)
            author: Автор (имя или URI существующего автора)
            isbn: ISBN книги
            keywords: Ключевые слова через запятую
            description: Описание книги
            url: URL книги (официальный сайт, Amazon, etc.)
            year: Год издания
            difficulty: Уровень сложности (Beginner, Intermediate, Advanced)
        
        Returns:
            True если успешно добавлено
        """
        try:
            # Создаем URI для книги
            book_name = self._normalize_name(title)
            book_uri = self.NS[book_name]
            
            # Проверяем, не существует ли уже
            if (book_uri, RDF.type, self.NS.Book) in self.g:
                print(f"⚠️ Книга '{title}' уже существует")
                return False
            
            # Получаем URI языка
            lang_uri = self.NS[language]
            if not (lang_uri, RDF.type, self.NS.ProgrammingLanguage) in self.g:
                print(f"⚠️ Язык '{language}' не найден в онтологии")
                return False
            
            # Добавляем книгу
            self.g.add((book_uri, RDF.type, self.NS.Book))
            self.g.add((book_uri, RDF.type, self.OWL.NamedIndividual))
            self.g.add((book_uri, self.NS.title, Literal(title)))
            self.g.add((book_uri, self.NS.aboutLanguage, lang_uri))
            
            # Опциональные свойства
            if author:
                author_uri = self._get_or_create_author(author)
                self.g.add((book_uri, self.NS.writtenBy, author_uri))
            
            if isbn:
                self.g.add((book_uri, self.NS.isbn, Literal(isbn)))
            
            if keywords:
                self.g.add((book_uri, self.NS.keywords, Literal(keywords)))
            
            if description:
                self.g.add((book_uri, self.NS.description, Literal(description)))
            
            if url:
                self.g.add((book_uri, self.NS.url, Literal(url, datatype=XSD.anyURI)))
            
            if year:
                self.g.add((book_uri, self.NS.yearCreated, Literal(year, datatype=XSD.integer)))
            
            if difficulty:
                difficulty_uri = self.NS[difficulty]
                self.g.add((book_uri, self.NS.hasDifficulty, difficulty_uri))
            
            print(f"✅ Книга '{title}' добавлена для языка {language}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка добавления книги: {e}")
            return False
    
    def add_article(self, title: str, language: str, url: str,
                   author: Optional[str] = None, keywords: Optional[str] = None,
                   description: Optional[str] = None, doi: Optional[str] = None,
                   publication_date: Optional[str] = None) -> bool:
        """
        Добавление статьи в онтологию
        
        Args:
            title: Название статьи
            language: Язык программирования
            url: URL статьи
            author: Автор
            keywords: Ключевые слова
            description: Описание
            doi: DOI статьи
            publication_date: Дата публикации (ISO format)
        
        Returns:
            True если успешно добавлено
        """
        try:
            article_name = self._normalize_name(title)
            article_uri = self.NS[article_name]
            
            if (article_uri, RDF.type, self.NS.Article) in self.g:
                print(f"⚠️ Статья '{title}' уже существует")
                return False
            
            lang_uri = self.NS[language]
            if not (lang_uri, RDF.type, self.NS.ProgrammingLanguage) in self.g:
                print(f"⚠️ Язык '{language}' не найден")
                return False
            
            self.g.add((article_uri, RDF.type, self.NS.Article))
            self.g.add((article_uri, RDF.type, self.OWL.NamedIndividual))
            self.g.add((article_uri, self.NS.title, Literal(title)))
            self.g.add((article_uri, self.NS.aboutLanguage, lang_uri))
            self.g.add((article_uri, self.NS.url, Literal(url, datatype=XSD.anyURI)))
            
            if author:
                author_uri = self._get_or_create_author(author)
                self.g.add((article_uri, self.NS.writtenBy, author_uri))
            
            if keywords:
                self.g.add((article_uri, self.NS.keywords, Literal(keywords)))
            
            if description:
                self.g.add((article_uri, self.NS.description, Literal(description)))
            
            if doi:
                self.g.add((article_uri, self.NS.doi, Literal(doi)))
            
            if publication_date:
                self.g.add((article_uri, self.NS.publicationDate, Literal(publication_date, datatype=XSD.dateTime)))
            
            print(f"✅ Статья '{title}' добавлена для языка {language}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка добавления статьи: {e}")
            return False
    
    def add_documentation(self, title: str, language: str, url: str,
                         description: Optional[str] = None) -> bool:
        """
        Добавление документации в онтологию
        
        Args:
            title: Название документации
            language: Язык программирования
            url: URL документации
            description: Описание
        
        Returns:
            True если успешно добавлено
        """
        try:
            doc_name = self._normalize_name(title)
            doc_uri = self.NS[doc_name]
            
            if (doc_uri, RDF.type, self.NS.Documentation) in self.g:
                print(f"⚠️ Документация '{title}' уже существует")
                return False
            
            lang_uri = self.NS[language]
            if not (lang_uri, RDF.type, self.NS.ProgrammingLanguage) in self.g:
                print(f"⚠️ Язык '{language}' не найден")
                return False
            
            self.g.add((doc_uri, RDF.type, self.NS.Documentation))
            self.g.add((doc_uri, RDF.type, self.OWL.NamedIndividual))
            self.g.add((doc_uri, self.NS.title, Literal(title)))
            self.g.add((doc_uri, self.NS.aboutLanguage, lang_uri))
            self.g.add((doc_uri, self.NS.url, Literal(url, datatype=XSD.anyURI)))
            
            if description:
                self.g.add((doc_uri, self.NS.description, Literal(description)))
            
            print(f"✅ Документация '{title}' добавлена для языка {language}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка добавления документации: {e}")
            return False
    
    def add_tutorial(self, title: str, language: str, url: str,
                    difficulty: Optional[str] = None, keywords: Optional[str] = None) -> bool:
        """
        Добавление туториала в онтологию
        
        Args:
            title: Название туториала
            language: Язык программирования
            url: URL туториала
            difficulty: Уровень сложности
            keywords: Ключевые слова
        
        Returns:
            True если успешно добавлено
        """
        try:
            tutorial_name = self._normalize_name(title)
            tutorial_uri = self.NS[tutorial_name]
            
            if (tutorial_uri, RDF.type, self.NS.Tutorial) in self.g:
                print(f"⚠️ Туториал '{title}' уже существует")
                return False
            
            lang_uri = self.NS[language]
            if not (lang_uri, RDF.type, self.NS.ProgrammingLanguage) in self.g:
                print(f"⚠️ Язык '{language}' не найден")
                return False
            
            self.g.add((tutorial_uri, RDF.type, self.NS.Tutorial))
            self.g.add((tutorial_uri, RDF.type, self.OWL.NamedIndividual))
            self.g.add((tutorial_uri, self.NS.title, Literal(title)))
            self.g.add((tutorial_uri, self.NS.aboutLanguage, lang_uri))
            self.g.add((tutorial_uri, self.NS.url, Literal(url, datatype=XSD.anyURI)))
            
            if difficulty:
                difficulty_uri = self.NS[difficulty]
                self.g.add((tutorial_uri, self.NS.hasDifficulty, difficulty_uri))
            
            if keywords:
                self.g.add((tutorial_uri, self.NS.keywords, Literal(keywords)))
            
            print(f"✅ Туториал '{title}' добавлен для языка {language}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка добавления туториала: {e}")
            return False
    
    def _get_or_create_author(self, author_name: str) -> URIRef:
        """Получение или создание автора"""
        author_normalized = self._normalize_name(author_name)
        author_uri = self.NS[author_normalized]
        
        if not (author_uri, RDF.type, self.NS.Author) in self.g:
            self.g.add((author_uri, RDF.type, self.NS.Author))
            self.g.add((author_uri, RDF.type, self.OWL.NamedIndividual))
        
        return author_uri
    
    def _normalize_name(self, name: str) -> str:
        """Нормализация имени для URI"""
        # Убираем специальные символы, заменяем пробелы
        normalized = re.sub(r'[^\w\s]', '', name)
        normalized = re.sub(r'\s+', '', normalized)
        # Ограничиваем длину
        if len(normalized) > 50:
            normalized = normalized[:50]
        return normalized
    
    def save_ontology(self):
        """Сохранение онтологии"""
        try:
            self.g.serialize(destination=str(self.ontology_path), format="turtle")
            print(f"💾 Онтология сохранена: {self.ontology_path}")
            return True
        except Exception as e:
            print(f"❌ Ошибка сохранения онтологии: {e}")
            return False
    
    def get_publications_for_language(self, language: str) -> List[Dict]:
        """Получение всех публикаций для языка"""
        lang_uri = self.NS[language]
        
        # Используем прямой доступ к графу для надежности
        publications = []
        
        # Получаем все публикации, связанные с языком
        all_pubs = list(self.g.subjects(self.NS.aboutLanguage, lang_uri))
        
        for pub_uri in all_pubs:
            # Определяем тип публикации
            pub_type = None
            if (pub_uri, RDF.type, self.NS.Book) in self.g:
                pub_type = 'Book'
            elif (pub_uri, RDF.type, self.NS.Article) in self.g:
                pub_type = 'Article'
            elif (pub_uri, RDF.type, self.NS.Documentation) in self.g:
                pub_type = 'Documentation'
            elif (pub_uri, RDF.type, self.NS.Tutorial) in self.g:
                pub_type = 'Tutorial'
            
            # Пропускаем если это не публикация
            if not pub_type:
                continue
            
            # Получаем свойства
            title = self.g.value(pub_uri, self.NS.title)
            url = self.g.value(pub_uri, self.NS.url)
            author_uri = self.g.value(pub_uri, self.NS.writtenBy)
            keywords = self.g.value(pub_uri, self.NS.keywords)
            
            # Преобразуем значения
            title_str = str(title) if title else ""
            url_str = str(url) if url else ""
            author_str = str(author_uri).split("/")[-1] if author_uri else None
            keywords_str = str(keywords) if keywords else ""
            
            publications.append({
                'uri': str(pub_uri),
                'type': pub_type,
                'title': title_str,
                'url': url_str,
                'author': author_str,
                'keywords': keywords_str
            })

        # Добавляем факты, сохраненные из браузера (KnowledgeFact),
        # чтобы они отображались на странице источников языка.
        for fact_uri in self.g.subjects(RDF.type, self.NS.KnowledgeFact):
            fact_lang = self.g.value(fact_uri, self.NS.aboutLanguage)
            if fact_lang != lang_uri:
                continue

            title = self.g.value(fact_uri, self.NS.title)
            fact_text = self.g.value(fact_uri, self.NS.factText)
            source_url = self.g.value(fact_uri, self.NS.hasSource)
            source_name = self.g.value(fact_uri, self.NS.sourceName)
            material_type = self.g.value(fact_uri, self.NS.materialType)
            query_text = self.g.value(fact_uri, self.NS.queryText)

            type_str = str(material_type) if material_type else "Article"
            title_str = str(title) if title else "Сохраненный факт"
            url_str = str(source_url) if source_url else ""
            author_str = str(source_name) if source_name else None

            keywords_parts = []
            if query_text:
                keywords_parts.append(f"запрос: {str(query_text)}")
            if fact_text:
                keywords_parts.append(str(fact_text))

            publications.append({
                'uri': str(fact_uri),
                'type': type_str,
                'title': title_str,
                'url': url_str,
                'author': author_str,
                'keywords': " | ".join(keywords_parts)
            })
        
        return publications

def test_publication_manager():
    """Тестирование менеджера публикаций"""
    pm = PublicationManager()
    
    print("🧪 ТЕСТИРОВАНИЕ МЕНЕДЖЕРА ПУБЛИКАЦИЙ")
    print("=" * 60)
    
    # Добавляем книгу
    print("\n1. Добавление книги...")
    pm.add_book(
        title="Fluent Python",
        language="Python",
        author="Luciano Ramalho",
        isbn="978-1491946008",
        keywords="advanced, pythonic, best practices",
        url="https://www.oreilly.com/library/view/fluent-python/9781491946237/",
        year=2015,
        difficulty="Advanced"
    )
    
    # Добавляем статью
    print("\n2. Добавление статьи...")
    pm.add_article(
        title="Python Type Hints",
        language="Python",
        url="https://docs.python.org/3/library/typing.html",
        keywords="type hints, typing, annotations",
        description="Official Python type hints documentation"
    )
    
    # Добавляем документацию
    print("\n3. Добавление документации...")
    pm.add_documentation(
        title="Python Official Documentation",
        language="Python",
        url="https://docs.python.org/3/",
        description="Official Python 3 documentation"
    )
    
    # Сохраняем
    print("\n4. Сохранение онтологии...")
    pm.save_ontology()
    
    # Получаем публикации
    print("\n5. Получение публикаций для Python...")
    pubs = pm.get_publications_for_language("Python")
    print(f"   Найдено публикаций: {len(pubs)}")
    for pub in pubs:
        print(f"   • [{pub['type']}] {pub['title']}")

if __name__ == "__main__":
    test_publication_manager()

