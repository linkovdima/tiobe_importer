"""
Скрипт для добавления русских и английских источников в онтологию
Все книги доступны бесплатно онлайн
"""
from publication_manager import PublicationManager

def add_russian_sources():
    """Добавление русских и английских источников для всех языков"""
    pm = PublicationManager()
    
    print("📚 ДОБАВЛЕНИЕ ИСТОЧНИКОВ")
    print("=" * 60)
    
    # Источники по языкам (бесплатные книги и ресурсы)
    sources = {
        'Python': {
            'books': [
                {
                    'title': 'Automate the Boring Stuff with Python',
                    'author': 'Al Sweigart',
                    'keywords': 'python, автоматизация, бесплатно, английский, начальный',
                    'url': 'https://automatetheboringstuff.com/'
                },
                {
                    'title': 'Python для начинающих',
                    'author': 'Эл Свейгарт',
                    'keywords': 'python, обучение, русский, бесплатно, начальный',
                    'url': 'https://automatetheboringstuff.com/2e/chapter0/'
                },
                {
                    'title': 'Think Python: How to Think Like a Computer Scientist',
                    'author': 'Allen B. Downey',
                    'keywords': 'python, обучение, бесплатно, английский, начальный',
                    'url': 'https://greenteapress.com/wp/think-python-2e/'
                },
                {
                    'title': 'Python Crash Course',
                    'author': 'Eric Matthes',
                    'keywords': 'python, обучение, бесплатно, английский, начальный',
                    'url': 'https://ehmatthes.github.io/pcc/'
                },
                {
                    'title': 'Dive Into Python 3',
                    'author': 'Mark Pilgrim',
                    'keywords': 'python, продвинутый, бесплатно, английский, продвинутый',
                    'url': 'https://diveintopython3.net/'
                },
                {
                    'title': 'Real Python',
                    'author': 'Real Python Team',
                    'keywords': 'python, обучение, бесплатно, английский, средний',
                    'url': 'https://realpython.com/'
                },
                {
                    'title': 'Python 3 Patterns, Recipes and Idioms',
                    'author': 'Bruce Eckel',
                    'keywords': 'python, паттерны, бесплатно, английский, продвинутый',
                    'url': 'https://python-3-patterns-idioms-test.readthedocs.io/'
                },
                {
                    'title': 'Fluent Python',
                    'author': 'Luciano Ramalho',
                    'keywords': 'python, продвинутый, бесплатно, английский, продвинутый',
                    'url': 'https://www.oreilly.com/library/view/fluent-python/9781491946237/'
                },
                {
                    'title': 'Effective Python',
                    'author': 'Brett Slatkin',
                    'keywords': 'python, лучшие практики, бесплатно, английский, продвинутый',
                    'url': 'https://effectivepython.com/'
                },
                {
                    'title': 'Python Tricks',
                    'author': 'Dan Bader',
                    'keywords': 'python, трюки, советы, бесплатно, английский, средний',
                    'url': 'https://realpython.com/python-tricks/'
                },
                {
                    'title': 'Python Cookbook',
                    'author': 'David Beazley',
                    'keywords': 'python, рецепты, бесплатно, английский, продвинутый',
                    'url': 'https://dabeaz.com/cookbook.html'
                },
                {
                    'title': 'Изучаем Python',
                    'author': 'Марк Лутц',
                    'keywords': 'python, обучение, русский, бесплатно, средний',
                    'url': 'https://pythonworld.ru/knigi/izuchaem-python.html'
                },
            ],
            'documentation': [
                {
                    'title': 'Python 3 Official Documentation',
                    'url': 'https://docs.python.org/3/',
                    'description': 'Официальная документация Python 3'
                },
                {
                    'title': 'Python на русском',
                    'url': 'https://pythonworld.ru/',
                    'description': 'Русскоязычная документация и туториалы по Python'
                },
                {
                    'title': 'Pydocs - Документация Python',
                    'url': 'https://pydocs.ru/',
                    'description': 'Русскоязычная документация Python'
                },
                {
                    'title': 'Python 3 для начинающих',
                    'url': 'https://pythonworld.ru/osnovy/',
                    'description': 'Основы Python 3 на русском языке'
                },
                {
                    'title': 'Python Standard Library',
                    'url': 'https://docs.python.org/3/library/',
                    'description': 'Документация стандартной библиотеки Python'
                },
                {
                    'title': 'Python PEP Index',
                    'url': 'https://peps.python.org/',
                    'description': 'Python Enhancement Proposals'
                },
            ],
            'articles': [
                {
                    'title': 'Python для начинающих',
                    'url': 'https://pythonworld.ru/osnovy/',
                    'keywords': 'python, основы, обучение, русский, начальный'
                },
                {
                    'title': 'Уроки Python',
                    'url': 'https://pythonworld.ru/tutorials/',
                    'keywords': 'python, уроки, туториалы, русский, начальный'
                },
                {
                    'title': 'Python Tips and Tricks',
                    'url': 'https://realpython.com/python-tricks/',
                    'keywords': 'python, советы, трюки, английский, средний'
                },
                {
                    'title': 'Python Best Practices',
                    'url': 'https://docs.python-guide.org/',
                    'keywords': 'python, лучшие практики, английский, средний'
                },
                {
                    'title': 'Python Performance Tips',
                    'url': 'https://wiki.python.org/moin/PythonSpeed/PerformanceTips',
                    'keywords': 'python, производительность, английский, продвинутый'
                },
                {
                    'title': 'Python Design Patterns',
                    'url': 'https://python-patterns.guide/',
                    'keywords': 'python, паттерны проектирования, английский, продвинутый'
                },
            ],
            'tutorials': [
                {
                    'title': 'Python Tutor - Интерактивный туториал',
                    'url': 'https://pythontutor.ru/',
                    'keywords': 'python, интерактивный, обучение, русский, начальный'
                },
                {
                    'title': 'Stepik - Курс Python',
                    'url': 'https://stepik.org/course/67/',
                    'keywords': 'python, курс, stepik, русский, начальный'
                },
                {
                    'title': 'Hexlet - Курс Python',
                    'url': 'https://ru.hexlet.io/courses/python-basics',
                    'keywords': 'python, курс, hexlet, русский, начальный'
                },
                {
                    'title': 'Codecademy Python Course',
                    'url': 'https://www.codecademy.com/learn/learn-python-3',
                    'keywords': 'python, курс, codecademy, английский, начальный'
                },
                {
                    'title': 'FreeCodeCamp Python',
                    'url': 'https://www.freecodecamp.org/learn/scientific-computing-with-python/',
                    'keywords': 'python, курс, freecodecamp, английский, начальный'
                },
                {
                    'title': 'Python для всех',
                    'url': 'https://www.py4e.com/',
                    'keywords': 'python, курс, английский, начальный'
                },
                {
                    'title': 'Interactive Python',
                    'url': 'https://runestone.academy/runestone/books/published/pythonds/index.html',
                    'keywords': 'python, интерактивный, английский, средний'
                },
            ]
        },
        'Java': {
            'books': [
                {
                    'title': 'Think Java: How to Think Like a Computer Scientist',
                    'author': 'Allen B. Downey',
                    'keywords': 'java, обучение, бесплатно, английский',
                    'url': 'https://greenteapress.com/wp/think-java/'
                },
                {
                    'title': 'Java для начинающих',
                    'author': 'Герберт Шилдт',
                    'keywords': 'java, обучение, русский, бесплатно',
                    'url': 'https://metanit.com/java/tutorial/'
                },
                {
                    'title': 'Java Programming Notes',
                    'author': 'Fred Swartz',
                    'keywords': 'java, обучение, бесплатно, английский',
                    'url': 'https://www.cs.armstrong.edu/liang/intro10e/'
                },
                {
                    'title': 'Introduction to Programming Using Java',
                    'author': 'David J. Eck',
                    'keywords': 'java, обучение, бесплатно, английский',
                    'url': 'https://math.hws.edu/javanotes/'
                },
                {
                    'title': 'Java для начинающих - Учебник',
                    'author': 'Metanit',
                    'keywords': 'java, обучение, русский, бесплатно',
                    'url': 'https://metanit.com/java/tutorial/'
                }
            ],
            'documentation': [
                {
                    'title': 'Java Documentation',
                    'url': 'https://docs.oracle.com/java/',
                    'description': 'Официальная документация Java'
                },
                {
                    'title': 'Java на русском',
                    'url': 'https://javarush.ru/',
                    'description': 'Русскоязычные материалы по Java'
                },
                {
                    'title': 'Java документация на русском',
                    'url': 'https://metanit.com/java/',
                    'description': 'Учебник Java на русском языке'
                },
                {
                    'title': 'Java SE Documentation',
                    'url': 'https://docs.oracle.com/javase/',
                    'description': 'Документация Java SE'
                }
            ],
            'tutorials': [
                {
                    'title': 'JavaRush - Интерактивный курс',
                    'url': 'https://javarush.ru/',
                    'keywords': 'java, курс, обучение, русский'
                },
                {
                    'title': 'Metanit - Учебник Java',
                    'url': 'https://metanit.com/java/',
                    'keywords': 'java, учебник, русский'
                },
                {
                    'title': 'Stepik - Курс Java',
                    'url': 'https://stepik.org/course/187/',
                    'keywords': 'java, курс, stepik, русский'
                },
                {
                    'title': 'Oracle Java Tutorials',
                    'url': 'https://docs.oracle.com/javase/tutorial/',
                    'keywords': 'java, туториал, oracle, английский'
                }
            ]
        },
        'JavaScript': {
            'books': [
                {
                    'title': 'Eloquent JavaScript',
                    'author': 'Marijn Haverbeke',
                    'keywords': 'javascript, обучение, бесплатно, английский',
                    'url': 'https://eloquentjavascript.net/'
                },
                {
                    'title': 'JavaScript для чайников',
                    'author': 'Marijn Haverbeke',
                    'keywords': 'javascript, обучение, русский, бесплатно',
                    'url': 'https://eloquentjavascript.net/Eloquent_JavaScript.pdf'
                },
                {
                    'title': 'You Don\'t Know JS',
                    'author': 'Kyle Simpson',
                    'keywords': 'javascript, продвинутый, бесплатно, английский',
                    'url': 'https://github.com/getify/You-Dont-Know-JS'
                },
                {
                    'title': 'JavaScript: The Definitive Guide',
                    'author': 'David Flanagan',
                    'keywords': 'javascript, справочник, бесплатно, английский',
                    'url': 'https://github.com/davidflanagan/javascript-definitive-guide'
                },
                {
                    'title': 'Modern JavaScript Tutorial',
                    'author': 'Ilya Kantor',
                    'keywords': 'javascript, современный, бесплатно, английский',
                    'url': 'https://javascript.info/'
                }
            ],
            'documentation': [
                {
                    'title': 'MDN JavaScript Guide',
                    'url': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript',
                    'description': 'Официальная документация JavaScript от Mozilla'
                },
                {
                    'title': 'JavaScript на русском',
                    'url': 'https://learn.javascript.ru/',
                    'description': 'Современный учебник JavaScript на русском'
                },
                {
                    'title': 'JavaScript Reference',
                    'url': 'https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference',
                    'description': 'Справочник JavaScript на русском'
                }
            ],
            'tutorials': [
                {
                    'title': 'Learn JavaScript - Русский учебник',
                    'url': 'https://learn.javascript.ru/',
                    'keywords': 'javascript, учебник, русский'
                },
                {
                    'title': 'FreeCodeCamp JavaScript',
                    'url': 'https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/',
                    'keywords': 'javascript, курс, freecodecamp, английский'
                },
                {
                    'title': 'Codecademy JavaScript',
                    'url': 'https://www.codecademy.com/learn/introduction-to-javascript',
                    'keywords': 'javascript, курс, codecademy, английский'
                }
            ]
        },
        'C': {
            'books': [
                {
                    'title': 'The C Programming Language',
                    'author': 'Brian Kernighan, Dennis Ritchie',
                    'keywords': 'c, классика, бесплатно, английский',
                    'url': 'https://www.pdfdrive.com/the-c-programming-language-e187620908.html'
                },
                {
                    'title': 'Modern C',
                    'author': 'Jens Gustedt',
                    'keywords': 'c, современный, бесплатно, английский',
                    'url': 'https://hal.inria.fr/hal-02383654/document'
                },
                {
                    'title': 'C Programming Notes',
                    'author': 'Steve Summit',
                    'keywords': 'c, обучение, бесплатно, английский',
                    'url': 'https://www.eskimo.com/~scs/cclass/notes/top.html'
                },
                {
                    'title': 'C для начинающих',
                    'author': 'Metanit',
                    'keywords': 'c, обучение, русский, бесплатно',
                    'url': 'https://metanit.com/c/tutorial/'
                }
            ],
            'documentation': [
                {
                    'title': 'C Reference',
                    'url': 'https://en.cppreference.com/w/c',
                    'description': 'Справочник по C'
                },
                {
                    'title': 'C на русском',
                    'url': 'https://ru.cppreference.com/w/c',
                    'description': 'Справочник по C на русском'
                },
                {
                    'title': 'GNU C Manual',
                    'url': 'https://www.gnu.org/software/gnu-c-manual/',
                    'description': 'Руководство по GNU C'
                }
            ],
            'tutorials': [
                {
                    'title': 'C Tutorial - TutorialsPoint',
                    'url': 'https://www.tutorialspoint.com/cprogramming/index.htm',
                    'keywords': 'c, туториал, английский'
                },
                {
                    'title': 'C Programming Tutorial',
                    'url': 'https://www.programiz.com/c-programming',
                    'keywords': 'c, туториал, английский'
                }
            ]
        },
        'CPlusPlus': {
            'books': [
                {
                    'title': 'The C++ Programming Language',
                    'author': 'Bjarne Stroustrup',
                    'keywords': 'c++, классика, бесплатно, английский',
                    'url': 'https://www.stroustrup.com/4th.html'
                },
                {
                    'title': 'C++ для начинающих',
                    'author': 'Metanit',
                    'keywords': 'c++, обучение, русский, бесплатно',
                    'url': 'https://metanit.com/cpp/tutorial/'
                },
                {
                    'title': 'C++ Core Guidelines',
                    'author': 'Bjarne Stroustrup',
                    'keywords': 'c++, руководство, бесплатно, английский',
                    'url': 'https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines'
                },
                {
                    'title': 'Learn C++',
                    'author': 'LearnCPP',
                    'keywords': 'c++, обучение, бесплатно, английский',
                    'url': 'https://www.learncpp.com/'
                }
            ],
            'documentation': [
                {
                    'title': 'C++ Reference',
                    'url': 'https://en.cppreference.com/w/cpp',
                    'description': 'Справочник по C++'
                },
                {
                    'title': 'C++ на русском',
                    'url': 'https://ru.cppreference.com/w/cpp',
                    'description': 'Справочник по C++ на русском'
                },
                {
                    'title': 'ISO C++',
                    'url': 'https://isocpp.org/',
                    'description': 'Официальный сайт C++'
                }
            ],
            'tutorials': [
                {
                    'title': 'C++ Tutorial - TutorialsPoint',
                    'url': 'https://www.tutorialspoint.com/cplusplus/index.htm',
                    'keywords': 'c++, туториал, английский'
                },
                {
                    'title': 'C++ для начинающих',
                    'url': 'https://metanit.com/cpp/tutorial/',
                    'keywords': 'c++, туториал, русский'
                }
            ]
        },
        'CSharp': {
            'books': [
                {
                    'title': 'C# для начинающих',
                    'author': 'Metanit',
                    'keywords': 'c#, обучение, русский, бесплатно',
                    'url': 'https://metanit.com/sharp/tutorial/'
                },
                {
                    'title': 'C# Yellow Book',
                    'author': 'Rob Miles',
                    'keywords': 'c#, обучение, бесплатно, английский',
                    'url': 'https://www.csharpcourse.com/'
                },
                {
                    'title': 'C# Programming Guide',
                    'author': 'Microsoft',
                    'keywords': 'c#, руководство, бесплатно, английский',
                    'url': 'https://docs.microsoft.com/dotnet/csharp/programming-guide/'
                },
                {
                    'title': 'C# in Depth',
                    'author': 'Jon Skeet',
                    'keywords': 'c#, продвинутый, бесплатно, английский',
                    'url': 'https://csharpindepth.com/'
                }
            ],
            'documentation': [
                {
                    'title': 'C# Documentation',
                    'url': 'https://docs.microsoft.com/dotnet/csharp/',
                    'description': 'Официальная документация C#'
                },
                {
                    'title': 'C# на русском',
                    'url': 'https://metanit.com/sharp/',
                    'description': 'Русскоязычная документация по C#'
                },
                {
                    'title': 'Learn C#',
                    'url': 'https://learn.microsoft.com/dotnet/csharp/',
                    'description': 'Официальный учебник C#'
                }
            ],
            'tutorials': [
                {
                    'title': 'Metanit - Учебник C#',
                    'url': 'https://metanit.com/sharp/',
                    'keywords': 'c#, учебник, русский'
                },
                {
                    'title': 'C# Tutorial - TutorialsPoint',
                    'url': 'https://www.tutorialspoint.com/csharp/index.htm',
                    'keywords': 'c#, туториал, английский'
                },
                {
                    'title': 'Microsoft C# Tutorials',
                    'url': 'https://docs.microsoft.com/dotnet/csharp/tutorials/',
                    'keywords': 'c#, туториал, microsoft, английский'
                }
            ]
        }
    }
    
    total_added = 0
    
    for language, source_list in sources.items():
        print(f"\n📚 Добавление источников для {language}...")
        
        # Книги
        for book in source_list.get('books', []):
            success = pm.add_book(
                title=book['title'],
                language=language,
                author=book.get('author'),
                url=book.get('url'),
                keywords=book.get('keywords', 'бесплатно')
            )
            if success:
                total_added += 1
        
        # Документация
        for doc in source_list.get('documentation', []):
            success = pm.add_documentation(
                title=doc['title'],
                language=language,
                url=doc['url'],
                description=doc.get('description', 'Документация')
            )
            if success:
                total_added += 1
        
        # Статьи
        for article in source_list.get('articles', []):
            success = pm.add_article(
                title=article['title'],
                language=language,
                url=article['url'],
                keywords=article.get('keywords', '')
            )
            if success:
                total_added += 1
        
        # Туториалы
        for tutorial in source_list.get('tutorials', []):
            success = pm.add_tutorial(
                title=tutorial['title'],
                language=language,
                url=tutorial['url'],
                keywords=tutorial.get('keywords', '')
            )
            if success:
                total_added += 1
    
    # Сохраняем
    if total_added > 0:
        pm.save_ontology()
        print(f"\n✅ Добавлено {total_added} источников")
    else:
        print("\n⚠️ Не было добавлено новых источников (возможно, они уже существуют)")

if __name__ == "__main__":
    add_russian_sources()
