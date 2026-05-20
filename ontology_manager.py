import os
from rdflib import Graph, Namespace, RDF, Literal
from pathlib import Path
from config import ONTOLOGY_PATH

class OntologyManager:
    def __init__(self, ontology_path=None):
        self.g = Graph()
        self.ontology_path = ontology_path or ONTOLOGY_PATH
        self.NS = Namespace("http://www.semanticweb.org/дмитрий/ontologies/2025/10/untitled-ontology-7/")
        
        # Загружаем онтологию
        self.load_ontology()
    
    def load_ontology(self):
        """Загрузка онтологии из файла"""
        try:
            # Преобразуем в строку если это Path объект
            ontology_path_str = str(self.ontology_path)
        
            if os.path.exists(ontology_path_str):
                self.g.parse(ontology_path_str, format="turtle")
                print(f"✅ Онтология загружена: {len(self.g)} триплов")
            
                # Проверим какие языки есть
                languages = list(self.g.subjects(RDF.type, self.NS.ProgrammingLanguage))
                print(f"📊 Найдено языков в онтологии: {len(languages)}")
                for lang in languages:
                    lang_name = str(lang).split("/")[-1]
                    print(f"   • {lang_name}")
                
                return True
            else:
                print(f"❌ Файл онтологии не найден: {ontology_path_str}")
                return False
        except Exception as e:
            print(f"❌ Ошибка загрузки онтологии: {e}")
            return False
    
    def _initialize_ontology(self):
        """Инициализация базовой структуры онтологии"""
        print("🆕 Создание базовой структуры онтологии...")
        # Здесь можно добавить базовые классы и свойства
        # Пока просто создаем пустую онтологию
        pass
    
    def save_ontology(self, path=None):
        """Сохранение онтологии"""
        save_path = path or self.ontology_path
        try:
            self.g.serialize(destination=save_path, format="turtle")
            print(f"💾 Онтология сохранена: {save_path}")
            return True
        except Exception as e:
            print(f"❌ Ошибка сохранения онтологии: {e}")
            return False
    
    def language_exists(self, language_name):
        """Проверка существования языка в онтологии"""
        lang_uri = self.NS[language_name]
        return (lang_uri, RDF.type, self.NS.ProgrammingLanguage) in self.g
    
    def update_language_ranking(self, language_name, rank, rating):
        """Обновление рейтинга языка"""
        if not self.language_exists(language_name):
            print(f"⚠️ Язык {language_name} не найден в онтологии")
            return False
        
        lang_uri = self.NS[language_name]
        
        try:
            # Удаляем старые значения
            self.g.remove((lang_uri, self.NS.tiobeRank, None))
            self.g.remove((lang_uri, self.NS.tiobeRating, None))
            
            # Добавляем новые
            self.g.add((lang_uri, self.NS.tiobeRank, Literal(int(rank))))
            self.g.add((lang_uri, self.NS.tiobeRating, Literal(rating)))
            
            print(f"✅ Обновлен {language_name}: #{rank} ({rating})")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка обновления {language_name}: {e}")
            return False
    
    def get_language_info(self, language_name):
        """Получение информации о языке"""
        if not self.language_exists(language_name):
            return None
        
        lang_uri = self.NS[language_name]
        info = {'name': language_name}
        
        # Получаем рейтинг TIOBE
        rank = self.g.value(lang_uri, self.NS.tiobeRank)
        rating = self.g.value(lang_uri, self.NS.tiobeRating)
        
        if rank:
            info['tiobe_rank'] = int(rank)
        if rating:
            info['tiobe_rating'] = str(rating)
            
        return info