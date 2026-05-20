# Создайте check_updated_data.py
from rdflib import Graph, Namespace, RDF

def check_updated_data():
    g = Graph()
    ontology_path = r"D:\OneDrive\Рабочий стол\tiobe_importer\data\programming_languages.ttl"
    g.parse(ontology_path, format="turtle")
    
    NS = Namespace("http://www.semanticweb.org/дмитрий/ontologies/2025/10/untitled-ontology-7/")
    
    print("📊 ДАННЫЕ В ОНТОЛОГИИ:")
    print("=" * 50)
    
    query = """
    SELECT ?lang ?tiobeRank ?tiobeRating ?githubRepos ?stackOverflowQuestions WHERE {
      ?lang a onto:ProgrammingLanguage .
      OPTIONAL { ?lang onto:tiobeRank ?tiobeRank . }
      OPTIONAL { ?lang onto:tiobeRating ?tiobeRating . }
      OPTIONAL { ?lang onto:githubRepositories ?githubRepos . }
      OPTIONAL { ?lang onto:stackOverflowQuestions ?stackOverflowQuestions . }
    }
    """
    
    results = g.query(query, initNs={"onto": NS})
    
    for row in results:
        lang_name = str(row[0]).split("/")[-1]
        tiobe_rank = row[1] if row[1] else "N/A"
        tiobe_rating = row[2] if row[2] else "N/A"
        github_repos = row[3] if row[3] else "N/A"
        stack_questions = row[4] if row[4] else "N/A"
        
        print(f"\n🎯 {lang_name}:")
        print(f"   TIOBE: #{tiobe_rank} ({tiobe_rating})")
        print(f"   GitHub: {github_repos} репозиториев")
        print(f"   Stack Overflow: {stack_questions} вопросов")

if __name__ == "__main__":
    check_updated_data()