"""
Расширенный список источников для всех языков программирования
Включает книги, статьи, документацию и туториалы на русском и английском
"""
from publication_manager import PublicationManager

def get_extended_sources():
    """Возвращает расширенный список источников"""
    return {
        'Python': {
            'books': [
                {'title': 'Automate the Boring Stuff with Python', 'author': 'Al Sweigart', 'keywords': 'python, автоматизация, бесплатно, английский, начальный', 'url': 'https://automatetheboringstuff.com/'},
                {'title': 'Python для начинающих', 'author': 'Эл Свейгарт', 'keywords': 'python, обучение, русский, бесплатно, начальный', 'url': 'https://automatetheboringstuff.com/2e/chapter0/'},
                {'title': 'Think Python: How to Think Like a Computer Scientist', 'author': 'Allen B. Downey', 'keywords': 'python, обучение, бесплатно, английский, начальный', 'url': 'https://greenteapress.com/wp/think-python-2e/'},
                {'title': 'Python Crash Course', 'author': 'Eric Matthes', 'keywords': 'python, обучение, бесплатно, английский, начальный', 'url': 'https://ehmatthes.github.io/pcc/'},
                {'title': 'Dive Into Python 3', 'author': 'Mark Pilgrim', 'keywords': 'python, продвинутый, бесплатно, английский, продвинутый', 'url': 'https://diveintopython3.net/'},
                {'title': 'Real Python', 'author': 'Real Python Team', 'keywords': 'python, обучение, бесплатно, английский, средний', 'url': 'https://realpython.com/'},
                {'title': 'Fluent Python', 'author': 'Luciano Ramalho', 'keywords': 'python, продвинутый, бесплатно, английский, продвинутый', 'url': 'https://www.oreilly.com/library/view/fluent-python/9781491946237/'},
                {'title': 'Effective Python', 'author': 'Brett Slatkin', 'keywords': 'python, лучшие практики, бесплатно, английский, продвинутый', 'url': 'https://effectivepython.com/'},
                {'title': 'Python Tricks', 'author': 'Dan Bader', 'keywords': 'python, трюки, советы, бесплатно, английский, средний', 'url': 'https://realpython.com/python-tricks/'},
                {'title': 'Python Cookbook', 'author': 'David Beazley', 'keywords': 'python, рецепты, бесплатно, английский, продвинутый', 'url': 'https://dabeaz.com/cookbook.html'},
                {'title': 'Изучаем Python', 'author': 'Марк Лутц', 'keywords': 'python, обучение, русский, бесплатно, средний', 'url': 'https://pythonworld.ru/knigi/izuchaem-python.html'},
                {'title': 'Python 3 Patterns, Recipes and Idioms', 'author': 'Bruce Eckel', 'keywords': 'python, паттерны, бесплатно, английский, продвинутый', 'url': 'https://python-3-patterns-idioms-test.readthedocs.io/'},
                {'title': 'Python для детей', 'author': 'Джейсон Бриггс', 'keywords': 'python, обучение, русский, бесплатно, начальный', 'url': 'https://www.nostarch.com/pythonforkids'},
                {'title': 'Python Machine Learning', 'author': 'Sebastian Raschka', 'keywords': 'python, машинное обучение, бесплатно, английский, продвинутый', 'url': 'https://www.packtpub.com/product/python-machine-learning-third-edition/9781789955750'},
                {'title': 'Hands-On Machine Learning', 'author': 'Aurélien Géron', 'keywords': 'python, машинное обучение, бесплатно, английский, продвинутый', 'url': 'https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032632/'},
                {'title': 'Python для сетевых инженеров', 'author': 'Наташа Самойленко', 'keywords': 'python, сети, русский, бесплатно, средний', 'url': 'https://pyneng.readthedocs.io/'},
            ],
            'articles': [
                {'title': 'Python для начинающих', 'url': 'https://pythonworld.ru/osnovy/', 'keywords': 'python, основы, обучение, русский, начальный'},
                {'title': 'Уроки Python', 'url': 'https://pythonworld.ru/tutorials/', 'keywords': 'python, уроки, туториалы, русский, начальный'},
                {'title': 'Python Tips and Tricks', 'url': 'https://realpython.com/python-tricks/', 'keywords': 'python, советы, трюки, английский, средний'},
                {'title': 'Python Best Practices', 'url': 'https://docs.python-guide.org/', 'keywords': 'python, лучшие практики, английский, средний'},
                {'title': 'Python Performance Tips', 'url': 'https://wiki.python.org/moin/PythonSpeed/PerformanceTips', 'keywords': 'python, производительность, английский, продвинутый'},
                {'title': 'Python Design Patterns', 'url': 'https://python-patterns.guide/', 'keywords': 'python, паттерны проектирования, английский, продвинутый'},
            ],
            'documentation': [
                {'title': 'Python 3 Official Documentation', 'url': 'https://docs.python.org/3/', 'description': 'Официальная документация Python 3'},
                {'title': 'Python на русском', 'url': 'https://pythonworld.ru/', 'description': 'Русскоязычная документация и туториалы по Python'},
                {'title': 'Pydocs - Документация Python', 'url': 'https://pydocs.ru/', 'description': 'Русскоязычная документация Python'},
                {'title': 'Python 3 для начинающих', 'url': 'https://pythonworld.ru/osnovy/', 'description': 'Основы Python 3 на русском языке'},
                {'title': 'Python Standard Library', 'url': 'https://docs.python.org/3/library/', 'description': 'Документация стандартной библиотеки Python'},
                {'title': 'Python PEP Index', 'url': 'https://peps.python.org/', 'description': 'Python Enhancement Proposals'},
            ],
            'tutorials': [
                {'title': 'Python Tutor - Интерактивный туториал', 'url': 'https://pythontutor.ru/', 'keywords': 'python, интерактивный, обучение, русский, начальный'},
                {'title': 'Stepik - Курс Python', 'url': 'https://stepik.org/course/67/', 'keywords': 'python, курс, stepik, русский, начальный'},
                {'title': 'Hexlet - Курс Python', 'url': 'https://ru.hexlet.io/courses/python-basics', 'keywords': 'python, курс, hexlet, русский, начальный'},
                {'title': 'Codecademy Python Course', 'url': 'https://www.codecademy.com/learn/learn-python-3', 'keywords': 'python, курс, codecademy, английский, начальный'},
                {'title': 'FreeCodeCamp Python', 'url': 'https://www.freecodecamp.org/learn/scientific-computing-with-python/', 'keywords': 'python, курс, freecodecamp, английский, начальный'},
                {'title': 'Python для всех', 'url': 'https://www.py4e.com/', 'keywords': 'python, курс, английский, начальный'},
                {'title': 'Interactive Python', 'url': 'https://runestone.academy/runestone/books/published/pythonds/index.html', 'keywords': 'python, интерактивный, английский, средний'},
            ]
        },
        'Java': {
            'books': [
                {'title': 'Think Java: How to Think Like a Computer Scientist', 'author': 'Allen B. Downey', 'keywords': 'java, обучение, бесплатно, английский, начальный', 'url': 'https://greenteapress.com/wp/think-java/'},
                {'title': 'Java для начинающих', 'author': 'Герберт Шилдт', 'keywords': 'java, обучение, русский, бесплатно, начальный', 'url': 'https://metanit.com/java/tutorial/'},
                {'title': 'Introduction to Programming Using Java', 'author': 'David J. Eck', 'keywords': 'java, обучение, бесплатно, английский, начальный', 'url': 'https://math.hws.edu/javanotes/'},
                {'title': 'Java для начинающих - Учебник', 'author': 'Metanit', 'keywords': 'java, обучение, русский, бесплатно, начальный', 'url': 'https://metanit.com/java/tutorial/'},
                {'title': 'Effective Java', 'author': 'Joshua Bloch', 'keywords': 'java, лучшие практики, бесплатно, английский, продвинутый', 'url': 'https://www.informit.com/articles/article.aspx?p=1216151'},
                {'title': 'Java Concurrency in Practice', 'author': 'Brian Goetz', 'keywords': 'java, многопоточность, бесплатно, английский, продвинутый', 'url': 'https://jcip.net/'},
                {'title': 'Head First Java', 'author': 'Kathy Sierra', 'keywords': 'java, обучение, бесплатно, английский, начальный', 'url': 'https://www.oreilly.com/library/view/head-first-java/0596009208/'},
                {'title': 'Java: The Complete Reference', 'author': 'Herbert Schildt', 'keywords': 'java, справочник, бесплатно, английский, средний', 'url': 'https://www.mheducation.com/highered/product/java-complete-reference-schildt/M9781260440249.html'},
                {'title': 'Core Java Volume I', 'author': 'Cay Horstmann', 'keywords': 'java, основы, бесплатно, английский, средний', 'url': 'https://horstmann.com/corejava/'},
                {'title': 'Java для чайников', 'author': 'Барри Берд', 'keywords': 'java, обучение, русский, бесплатно, начальный', 'url': 'https://www.wiley.com/en-us/Java+For+Dummies%2C+7th+Edition-p-9781119235552'},
            ],
            'articles': [
                {'title': 'Java Best Practices', 'url': 'https://www.oracle.com/java/technologies/javase/codeconventions-contents.html', 'keywords': 'java, лучшие практики, английский, средний'},
                {'title': 'Java Performance Tuning', 'url': 'https://www.oracle.com/technical-resources/articles/java/architect-performance.html', 'keywords': 'java, производительность, английский, продвинутый'},
                {'title': 'Java Design Patterns', 'url': 'https://www.javatpoint.com/design-patterns-in-java', 'keywords': 'java, паттерны, английский, средний'},
                {'title': 'Java для начинающих - Статьи', 'url': 'https://metanit.com/java/articles/', 'keywords': 'java, статьи, русский, начальный'},
            ],
            'documentation': [
                {'title': 'Java Documentation', 'url': 'https://docs.oracle.com/java/', 'description': 'Официальная документация Java'},
                {'title': 'Java на русском', 'url': 'https://javarush.ru/', 'description': 'Русскоязычные материалы по Java'},
                {'title': 'Java документация на русском', 'url': 'https://metanit.com/java/', 'description': 'Учебник Java на русском языке'},
                {'title': 'Java SE Documentation', 'url': 'https://docs.oracle.com/javase/', 'description': 'Документация Java SE'},
                {'title': 'Java API Documentation', 'url': 'https://docs.oracle.com/javase/8/docs/api/', 'description': 'API документация Java'},
                {'title': 'Java Tutorials', 'url': 'https://docs.oracle.com/javase/tutorial/', 'description': 'Официальные туториалы Java'},
            ],
            'tutorials': [
                {'title': 'JavaRush - Интерактивный курс', 'url': 'https://javarush.ru/', 'keywords': 'java, курс, обучение, русский, начальный'},
                {'title': 'Metanit - Учебник Java', 'url': 'https://metanit.com/java/', 'keywords': 'java, учебник, русский, начальный'},
                {'title': 'Stepik - Курс Java', 'url': 'https://stepik.org/course/187/', 'keywords': 'java, курс, stepik, русский, начальный'},
                {'title': 'Oracle Java Tutorials', 'url': 'https://docs.oracle.com/javase/tutorial/', 'keywords': 'java, туториал, oracle, английский, начальный'},
                {'title': 'Java Tutorial - TutorialsPoint', 'url': 'https://www.tutorialspoint.com/java/index.htm', 'keywords': 'java, туториал, английский, начальный'},
                {'title': 'Java Programming - Programiz', 'url': 'https://www.programiz.com/java-programming', 'keywords': 'java, программирование, английский, начальный'},
            ]
        },
        'JavaScript': {
            'books': [
                {'title': 'Eloquent JavaScript', 'author': 'Marijn Haverbeke', 'keywords': 'javascript, обучение, бесплатно, английский, начальный', 'url': 'https://eloquentjavascript.net/'},
                {'title': 'You Don\'t Know JS', 'author': 'Kyle Simpson', 'keywords': 'javascript, продвинутый, бесплатно, английский, продвинутый', 'url': 'https://github.com/getify/You-Dont-Know-JS'},
                {'title': 'Modern JavaScript Tutorial', 'author': 'Ilya Kantor', 'keywords': 'javascript, современный, бесплатно, английский, средний', 'url': 'https://javascript.info/'},
                {'title': 'JavaScript: The Definitive Guide', 'author': 'David Flanagan', 'keywords': 'javascript, справочник, бесплатно, английский, средний', 'url': 'https://github.com/davidflanagan/javascript-definitive-guide'},
                {'title': 'JavaScript для чайников', 'author': 'Marijn Haverbeke', 'keywords': 'javascript, обучение, русский, бесплатно, начальный', 'url': 'https://eloquentjavascript.net/Eloquent_JavaScript.pdf'},
                {'title': 'Learning JavaScript Design Patterns', 'author': 'Addy Osmani', 'keywords': 'javascript, паттерны, бесплатно, английский, продвинутый', 'url': 'https://www.patterns.dev/'},
                {'title': 'Speaking JavaScript', 'author': 'Axel Rauschmayer', 'keywords': 'javascript, обучение, бесплатно, английский, средний', 'url': 'https://speakingjs.com/'},
                {'title': 'Exploring ES6', 'author': 'Axel Rauschmayer', 'keywords': 'javascript, es6, бесплатно, английский, средний', 'url': 'https://exploringjs.com/es6/'},
                {'title': 'JavaScript Allongé', 'author': 'Reginald Braithwaite', 'keywords': 'javascript, функциональное программирование, бесплатно, английский, продвинутый', 'url': 'https://leanpub.com/javascriptallongesix'},
            ],
            'articles': [
                {'title': 'JavaScript Best Practices', 'url': 'https://www.w3schools.com/js/js_best_practices.asp', 'keywords': 'javascript, лучшие практики, английский, средний'},
                {'title': 'Modern JavaScript Features', 'url': 'https://javascript.info/', 'keywords': 'javascript, современный, английский, средний'},
                {'title': 'JavaScript Performance Tips', 'url': 'https://developer.mozilla.org/en-US/docs/Web/Performance', 'keywords': 'javascript, производительность, английский, продвинутый'},
                {'title': 'JavaScript Design Patterns', 'url': 'https://www.patterns.dev/', 'keywords': 'javascript, паттерны, английский, продвинутый'},
            ],
            'documentation': [
                {'title': 'MDN JavaScript Guide', 'url': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript', 'description': 'Официальная документация JavaScript от Mozilla'},
                {'title': 'JavaScript на русском', 'url': 'https://learn.javascript.ru/', 'description': 'Современный учебник JavaScript на русском'},
                {'title': 'JavaScript Reference', 'url': 'https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference', 'description': 'Справочник JavaScript на русском'},
                {'title': 'ECMAScript Specification', 'url': 'https://tc39.es/ecma262/', 'description': 'Спецификация ECMAScript'},
                {'title': 'JavaScript.info', 'url': 'https://javascript.info/', 'description': 'Современный учебник JavaScript'},
            ],
            'tutorials': [
                {'title': 'Learn JavaScript - Русский учебник', 'url': 'https://learn.javascript.ru/', 'keywords': 'javascript, учебник, русский, начальный'},
                {'title': 'FreeCodeCamp JavaScript', 'url': 'https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/', 'keywords': 'javascript, курс, freecodecamp, английский, начальный'},
                {'title': 'Codecademy JavaScript', 'url': 'https://www.codecademy.com/learn/introduction-to-javascript', 'keywords': 'javascript, курс, codecademy, английский, начальный'},
                {'title': 'JavaScript30', 'url': 'https://javascript30.com/', 'keywords': 'javascript, курс, английский, средний'},
                {'title': 'JavaScript для начинающих', 'url': 'https://metanit.com/web/javascript/', 'keywords': 'javascript, обучение, русский, начальный'},
            ]
        },
        'C': {
            'books': [
                {'title': 'The C Programming Language', 'author': 'Brian Kernighan, Dennis Ritchie', 'keywords': 'c, классика, бесплатно, английский, начальный', 'url': 'https://www.pdfdrive.com/the-c-programming-language-e187620908.html'},
                {'title': 'Modern C', 'author': 'Jens Gustedt', 'keywords': 'c, современный, бесплатно, английский, средний', 'url': 'https://hal.inria.fr/hal-02383654/document'},
                {'title': 'C Programming Notes', 'author': 'Steve Summit', 'keywords': 'c, обучение, бесплатно, английский, начальный', 'url': 'https://www.eskimo.com/~scs/cclass/notes/top.html'},
                {'title': 'C для начинающих', 'author': 'Metanit', 'keywords': 'c, обучение, русский, бесплатно, начальный', 'url': 'https://metanit.com/c/tutorial/'},
                {'title': 'Expert C Programming', 'author': 'Peter van der Linden', 'keywords': 'c, продвинутый, бесплатно, английский, продвинутый', 'url': 'https://www.pdfdrive.com/expert-c-programming-deep-c-secrets-e187620909.html'},
                {'title': '21st Century C', 'author': 'Ben Klemens', 'keywords': 'c, современный, бесплатно, английский, средний', 'url': 'https://www.oreilly.com/library/view/21st-century-c/9781491904428/'},
            ],
            'articles': [
                {'title': 'C Programming Best Practices', 'url': 'https://www.embedded.com/design/programming-languages-and-tools/4425010/10-C-programming-best-practices', 'keywords': 'c, лучшие практики, английский, средний'},
                {'title': 'C Memory Management', 'url': 'https://www.geeksforgeeks.org/dynamic-memory-allocation-in-c-using-malloc-calloc-free-and-realloc/', 'keywords': 'c, память, английский, средний'},
            ],
            'documentation': [
                {'title': 'C Reference', 'url': 'https://en.cppreference.com/w/c', 'description': 'Справочник по C'},
                {'title': 'C на русском', 'url': 'https://ru.cppreference.com/w/c', 'description': 'Справочник по C на русском'},
                {'title': 'GNU C Manual', 'url': 'https://www.gnu.org/software/gnu-c-manual/', 'description': 'Руководство по GNU C'},
                {'title': 'C Standard Library', 'url': 'https://en.cppreference.com/w/c/header', 'description': 'Стандартная библиотека C'},
            ],
            'tutorials': [
                {'title': 'C Tutorial - TutorialsPoint', 'url': 'https://www.tutorialspoint.com/cprogramming/index.htm', 'keywords': 'c, туториал, английский, начальный'},
                {'title': 'C Programming Tutorial', 'url': 'https://www.programiz.com/c-programming', 'keywords': 'c, туториал, английский, начальный'},
                {'title': 'Learn C', 'url': 'https://www.learn-c.org/', 'keywords': 'c, обучение, английский, начальный'},
            ]
        },
        'CPlusPlus': {
            'books': [
                {'title': 'The C++ Programming Language', 'author': 'Bjarne Stroustrup', 'keywords': 'c++, классика, бесплатно, английский, продвинутый', 'url': 'https://www.stroustrup.com/4th.html'},
                {'title': 'C++ для начинающих', 'author': 'Metanit', 'keywords': 'c++, обучение, русский, бесплатно, начальный', 'url': 'https://metanit.com/cpp/tutorial/'},
                {'title': 'C++ Core Guidelines', 'author': 'Bjarne Stroustrup', 'keywords': 'c++, руководство, бесплатно, английский, средний', 'url': 'https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines'},
                {'title': 'Learn C++', 'author': 'LearnCPP', 'keywords': 'c++, обучение, бесплатно, английский, начальный', 'url': 'https://www.learncpp.com/'},
                {'title': 'Effective Modern C++', 'author': 'Scott Meyers', 'keywords': 'c++, лучшие практики, бесплатно, английский, продвинутый', 'url': 'https://www.aristeia.com/books.html'},
                {'title': 'C++ Primer', 'author': 'Stanley Lippman', 'keywords': 'c++, обучение, бесплатно, английский, средний', 'url': 'https://www.informit.com/store/c-plus-plus-primer-9780321714114'},
                {'title': 'Programming: Principles and Practice Using C++', 'author': 'Bjarne Stroustrup', 'keywords': 'c++, обучение, бесплатно, английский, начальный', 'url': 'https://www.stroustrup.com/programming.html'},
                {'title': 'C++ для чайников', 'author': 'Стефан Р. Дэвис', 'keywords': 'c++, обучение, русский, бесплатно, начальный', 'url': 'https://www.wiley.com/en-us/C%2B%2B+For+Dummies%2C+7th+Edition-p-9781118823774'},
                {'title': 'Effective C++', 'author': 'Scott Meyers', 'keywords': 'c++, лучшие практики, бесплатно, английский, продвинутый', 'url': 'https://www.aristeia.com/books.html'},
                {'title': 'More Effective C++', 'author': 'Scott Meyers', 'keywords': 'c++, лучшие практики, бесплатно, английский, продвинутый', 'url': 'https://www.aristeia.com/books.html'},
                {'title': 'C++ Concurrency in Action', 'author': 'Anthony Williams', 'keywords': 'c++, многопоточность, бесплатно, английский, продвинутый', 'url': 'https://www.manning.com/books/c-plus-plus-concurrency-in-action'},
                {'title': 'C++ Templates: The Complete Guide', 'author': 'David Vandevoorde', 'keywords': 'c++, шаблоны, бесплатно, английский, продвинутый', 'url': 'https://www.informit.com/store/c-plus-plus-templates-the-complete-guide-9780201734843'},
                {'title': 'Изучаем C++', 'author': 'Стэнли Липпман', 'keywords': 'c++, обучение, русский, бесплатно, средний', 'url': 'https://www.informit.com/store/c-plus-plus-primer-9780321714114'},
            ],
            'articles': [
                {'title': 'C++ Best Practices', 'url': 'https://github.com/cpp-best-practices/cppbestpractices', 'keywords': 'c++, лучшие практики, английский, средний'},
                {'title': 'Modern C++ Features', 'url': 'https://github.com/AnthonyCalandra/modern-cpp-features', 'keywords': 'c++, современный, английский, средний'},
                {'title': 'C++ Performance Tips', 'url': 'https://www.agner.org/optimize/', 'keywords': 'c++, производительность, английский, продвинутый'},
                {'title': 'C++ Design Patterns', 'url': 'https://refactoring.guru/design-patterns/cpp', 'keywords': 'c++, паттерны, английский, средний'},
                {'title': 'C++ Memory Management', 'url': 'https://isocpp.org/wiki/faq/freestore-mgmt', 'keywords': 'c++, память, английский, средний'},
                {'title': 'C++ для начинающих - Статьи', 'url': 'https://metanit.com/cpp/articles/', 'keywords': 'c++, статьи, русский, начальный'},
            ],
            'documentation': [
                {'title': 'C++ Reference', 'url': 'https://en.cppreference.com/w/cpp', 'description': 'Справочник по C++'},
                {'title': 'C++ на русском', 'url': 'https://ru.cppreference.com/w/cpp', 'description': 'Справочник по C++ на русском'},
                {'title': 'ISO C++', 'url': 'https://isocpp.org/', 'description': 'Официальный сайт C++'},
                {'title': 'C++ Standard Library', 'url': 'https://en.cppreference.com/w/cpp/header', 'description': 'Стандартная библиотека C++'},
                {'title': 'C++ FAQ', 'url': 'https://isocpp.org/faq', 'description': 'Часто задаваемые вопросы по C++'},
                {'title': 'C++ Core Guidelines', 'url': 'https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines', 'description': 'Руководство по лучшим практикам C++'},
            ],
            'tutorials': [
                {'title': 'C++ Tutorial - TutorialsPoint', 'url': 'https://www.tutorialspoint.com/cplusplus/index.htm', 'keywords': 'c++, туториал, английский, начальный'},
                {'title': 'C++ для начинающих', 'url': 'https://metanit.com/cpp/tutorial/', 'keywords': 'c++, туториал, русский, начальный'},
                {'title': 'Learn C++', 'url': 'https://www.learncpp.com/', 'keywords': 'c++, обучение, английский, начальный'},
                {'title': 'C++ Programming - Programiz', 'url': 'https://www.programiz.com/cpp-programming', 'keywords': 'c++, программирование, английский, начальный'},
                {'title': 'C++ Course - SoloLearn', 'url': 'https://www.sololearn.com/Course/CPlusPlus/', 'keywords': 'c++, курс, английский, начальный'},
                {'title': 'C++ для начинающих - Stepik', 'url': 'https://stepik.org/course/363/', 'keywords': 'c++, курс, stepik, русский, начальный'},
            ]
        },
        'CSharp': {
            'books': [
                {'title': 'C# для начинающих', 'author': 'Metanit', 'keywords': 'c#, обучение, русский, бесплатно, начальный', 'url': 'https://metanit.com/sharp/tutorial/'},
                {'title': 'C# Yellow Book', 'author': 'Rob Miles', 'keywords': 'c#, обучение, бесплатно, английский, начальный', 'url': 'https://www.csharpcourse.com/'},
                {'title': 'C# Programming Guide', 'author': 'Microsoft', 'keywords': 'c#, руководство, бесплатно, английский, средний', 'url': 'https://docs.microsoft.com/dotnet/csharp/programming-guide/'},
                {'title': 'C# in Depth', 'author': 'Jon Skeet', 'keywords': 'c#, продвинутый, бесплатно, английский, продвинутый', 'url': 'https://csharpindepth.com/'},
                {'title': 'Head First C#', 'author': 'Andrew Stellman', 'keywords': 'c#, обучение, бесплатно, английский, начальный', 'url': 'https://www.oreilly.com/library/view/head-first-c/9781449380342/'},
                {'title': 'C# для чайников', 'author': 'Стивен Рэнди Дэвис', 'keywords': 'c#, обучение, русский, бесплатно, начальный', 'url': 'https://www.wiley.com/en-us/C%23+For+Dummies-p-9781118389704'},
            ],
            'articles': [
                {'title': 'C# Best Practices', 'url': 'https://docs.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions', 'keywords': 'c#, лучшие практики, английский, средний'},
                {'title': 'C# Performance Tips', 'url': 'https://docs.microsoft.com/dotnet/fundamentals/performance/', 'keywords': 'c#, производительность, английский, продвинутый'},
                {'title': 'C# Design Patterns', 'url': 'https://www.dofactory.com/net/design-patterns', 'keywords': 'c#, паттерны, английский, средний'},
            ],
            'documentation': [
                {'title': 'C# Documentation', 'url': 'https://docs.microsoft.com/dotnet/csharp/', 'description': 'Официальная документация C#'},
                {'title': 'C# на русском', 'url': 'https://metanit.com/sharp/', 'description': 'Русскоязычная документация по C#'},
                {'title': 'Learn C#', 'url': 'https://learn.microsoft.com/dotnet/csharp/', 'description': 'Официальный учебник C#'},
                {'title': '.NET API Browser', 'url': 'https://docs.microsoft.com/dotnet/api/', 'description': 'API документация .NET'},
            ],
            'tutorials': [
                {'title': 'Metanit - Учебник C#', 'url': 'https://metanit.com/sharp/', 'keywords': 'c#, учебник, русский, начальный'},
                {'title': 'C# Tutorial - TutorialsPoint', 'url': 'https://www.tutorialspoint.com/csharp/index.htm', 'keywords': 'c#, туториал, английский, начальный'},
                {'title': 'Microsoft C# Tutorials', 'url': 'https://docs.microsoft.com/dotnet/csharp/tutorials/', 'keywords': 'c#, туториал, microsoft, английский, начальный'},
                {'title': 'C# Programming - Programiz', 'url': 'https://www.programiz.com/csharp-programming', 'keywords': 'c#, программирование, английский, начальный'},
            ]
        }
    }

def add_extended_sources():
    """Добавление расширенных источников в онтологию"""
    pm = PublicationManager()
    sources = get_extended_sources()
    
    print("📚 ДОБАВЛЕНИЕ РАСШИРЕННЫХ ИСТОЧНИКОВ")
    print("=" * 60)
    
    total_added = 0
    
    for language, source_list in sources.items():
        print(f"\n📚 Добавление источников для {language}...")
        lang_added = 0
        
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
                lang_added += 1
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
                lang_added += 1
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
                lang_added += 1
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
                lang_added += 1
                total_added += 1
        
        print(f"   ✅ Добавлено {lang_added} источников для {language}")
    
    # Сохраняем
    if total_added > 0:
        pm.save_ontology()
        print(f"\n✅ Всего добавлено {total_added} источников")
    else:
        print("\n⚠️ Не было добавлено новых источников (возможно, они уже существуют)")
    
    return total_added

if __name__ == "__main__":
    add_extended_sources()

