from rdflib import Graph, Namespace, RDF

def check_updated():
    g = Graph()
    ontology_path = r"D:\OneDrive\Документы\protege_test\my_ontology.ttl"
    g.parse(ontology_path, format="turtle")
    
    NS = Namespace("http://www.semanticweb.org/дмитрий/ontologies/2025/10/untitled-ontology-7/")
    
    print("📈 ОБНОВЛЕННЫЕ РЕЙТИНГИ TIOBE:")
    print("=" * 50)
    
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
        
        print(f"• {lang_name}: #{rank} ({rating})")

if __name__ == "__main__":
    check_updated()