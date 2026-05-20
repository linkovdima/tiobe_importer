from rdflib import Graph, Namespace, RDF, RDFS, XSD, Literal
import os

def add_missing_properties():
    """Добавление недостающих свойств в онтологию"""
    
    g = Graph()
    ontology_path = r"D:\OneDrive\Рабочий стол\tiobe_importer\data\programming_languages.ttl"
    
    if not os.path.exists(ontology_path):
        print(f"❌ Файл онтологии не найден: {ontology_path}")
        return
    
    g.parse(ontology_path, format="turtle")
    
    NS = Namespace("http://www.semanticweb.org/дмитрий/ontologies/2025/10/untitled-ontology-7/")
    g.bind("", NS)
    
    # Новые свойства для GitHub
    github_props = [
        ('githubRepositories', 'GitHub Repositories', XSD.integer),
        ('githubStars', 'GitHub Stars', XSD.integer),
        ('githubAvgStars', 'GitHub Average Stars', XSD.float),
        ('githubLastUpdated', 'GitHub Last Updated', XSD.dateTime),
    ]
    
    # Новые свойства для Stack Overflow
    stackoverflow_props = [
        ('stackOverflowQuestions', 'Stack Overflow Questions', XSD.integer),
        ('stackOverflowLastUpdated', 'Stack Overflow Last Updated', XSD.dateTime),
    ]
    
    print("➕ ДОБАВЛЕНИЕ НОВЫХ СВОЙСТВ В ОНТОЛОГИЮ")
    print("=" * 50)
    
    added_count = 0
    
    # Добавляем GitHub свойства
    for prop_name, label, data_type in github_props:
        prop_uri = NS[prop_name]
        
        if (prop_uri, RDF.type, RDF.Property) not in g:
            g.add((prop_uri, RDF.type, RDF.Property))
            g.add((prop_uri, RDFS.label, Literal(label)))
            g.add((prop_uri, RDFS.domain, NS.ProgrammingLanguage))
            g.add((prop_uri, RDFS.range, data_type))
            print(f"✅ Добавлено: {prop_name}")
            added_count += 1
        else:
            print(f"ℹ️ Уже существует: {prop_name}")
    
    # Добавляем Stack Overflow свойства
    for prop_name, label, data_type in stackoverflow_props:
        prop_uri = NS[prop_name]
        
        if (prop_uri, RDF.type, RDF.Property) not in g:
            g.add((prop_uri, RDF.type, RDF.Property))
            g.add((prop_uri, RDFS.label, Literal(label)))
            g.add((prop_uri, RDFS.domain, NS.ProgrammingLanguage))
            g.add((prop_uri, RDFS.range, data_type))
            print(f"✅ Добавлено: {prop_name}")
            added_count += 1
        else:
            print(f"ℹ️ Уже существует: {prop_name}")
    
    # Сохраняем онтологию
    if added_count > 0:
        g.serialize(ontology_path, format="turtle")
        print(f"\n💾 Онтология сохранена! Добавлено {added_count} свойств")
    else:
        print("\nℹ️ Все свойства уже существуют")

if __name__ == "__main__":
    add_missing_properties()