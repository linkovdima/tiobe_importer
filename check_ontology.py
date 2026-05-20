from rdflib import Graph, Namespace, RDF

def check_ontology():
    """Проверка содержимого онтологии"""
    g = Graph()
    ontology_path = r"D:\OneDrive\Рабочий стол\tiobe_importer\data\programming_languages.ttl"
    
    try:
        g.parse(ontology_path, format="turtle")
        print("✅ Онтология загружена успешно!")
        print(f"📊 Всего триплов: {len(g)}")
        
        NS = Namespace("http://www.semanticweb.org/дмитрий/ontologies/2025/10/untitled-ontology-7/")
        
        # Проверяем языки программирования
        languages = list(g.subjects(RDF.type, NS.ProgrammingLanguage))
        print(f"\n🎯 ЯЗЫКИ ПРОГРАММИРОВАНИЯ ({len(languages)}):")
        for lang in sorted(languages):
            lang_name = str(lang).split("/")[-1]
            print(f"   • {lang_name}")
        
        # Проверяем свойства
        print(f"\n🔧 СВОЙСТВА:")
        properties = list(g.subjects(RDF.type, RDF.Property))
        for prop in sorted(properties):
            prop_name = str(prop).split("/")[-1]
            print(f"   • {prop_name}")
            
        # Проверяем TIOBE рейтинги
        print(f"\n🏆 TIOBE РЕЙТИНГИ:")
        query = """
        SELECT ?lang ?rank ?rating WHERE {
          ?lang a onto:ProgrammingLanguage .
          OPTIONAL { ?lang onto:tiobeRank ?rank . }
          OPTIONAL { ?lang onto:tiobeRating ?rating . }
        }
        ORDER BY ?rank
        """
        results = g.query(query, initNs={"onto": NS})
        for row in results:
            lang_name = str(row[0]).split("/")[-1]
            rank = row[1] if row[1] else "N/A"
            rating = row[2] if row[2] else "N/A"
            print(f"   • {lang_name}: #{rank} ({rating})")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    check_ontology()