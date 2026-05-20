# check_six_languages.py
from rdflib import Graph, Namespace, RDF

def check_six_languages():
    g = Graph()
    ontology_path = r"D:\OneDrive\Рабочий стол\tiobe_importer\data\programming_languages.ttl"
    
    try:
        g.parse(ontology_path, format="turtle")
        print("✅ Онтология загружена")
        
        NS = Namespace("http://www.semanticweb.org/дмитрий/ontologies/2025/10/untitled-ontology-7/")
        
        target_languages = ['Python', 'Java', 'JavaScript', 'C', 'CPlusPlus', 'CSharp']
        
        print("\n🎯 ПРОВЕРКА 6 ЯЗЫКОВ:")
        for lang in target_languages:
            lang_uri = NS[lang]
            if (lang_uri, RDF.type, NS.ProgrammingLanguage) in g:
                print(f"   ✅ {lang} - присутствует")
            else:
                print(f"   ❌ {lang} - ОТСУТСТВУЕТ")
                
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    check_six_languages()