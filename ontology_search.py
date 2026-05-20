"""
Модуль поиска по онтологии языков программирования
Поддерживает поиск по ключевым словам, языкам, свойствам и связям
"""
from rdflib import Graph, Namespace, RDF, RDFS, Literal, URIRef
from rdflib.plugins.sparql import prepareQuery
from typing import List, Dict, Optional, Set
import re
from urllib.parse import quote_plus
from datetime import datetime
import time
from config import ONTOLOGY_PATH

class OntologySearch:
    def __init__(self, ontology_path=None):
        """Инициализация поискового модуля"""
        self.g = Graph()
        self.ontology_path = ontology_path or ONTOLOGY_PATH
        self.NS = Namespace("http://www.semanticweb.org/дмитрий/ontologies/2025/10/untitled-ontology-7/")
        self.load_ontology()
    
    def load_ontology(self):
        """Загрузка онтологии"""
        try:
            self.g.parse(str(self.ontology_path), format="turtle")
            print(f"✅ Онтология загружена для поиска: {len(self.g)} триплов")
            return True
        except Exception as e:
            print(f"❌ Ошибка загрузки онтологии: {e}")
            return False
    
    def search_by_keywords(
        self,
        keywords: str,
        languages: Optional[List[str]] = None,
        include_external_always: bool = False
    ) -> List[Dict]:
        """
        Поиск по ключевым словам
        
        Args:
            keywords: Строка с ключевыми словами (через пробел или запятую)
            languages: Список языков для фильтрации (None = все языки)
        
        Returns:
            Список словарей с результатами поиска
        """
        # Разбиваем ключевые слова
        keyword_list = [kw.strip().lower() for kw in re.split(r'[,\s]+', keywords) if kw.strip()]
        
        if not keyword_list:
            return []
        
        parsed_query = self._parse_semantic_query(keywords, languages)
        semantic_keywords = parsed_query["expanded_keywords"]
        results = []
        
        # Поиск в публикациях (книги, статьи) по keywords и title
        pub_results = self._search_in_publications(semantic_keywords, parsed_query["languages"])
        pub_results = [self._attach_quality_metrics(r, parsed_query, semantic_keywords) for r in pub_results]
        results.extend(pub_results)
        
        # Поиск в языках программирования по различным свойствам
        lang_results = self._search_in_languages(semantic_keywords, parsed_query["languages"])
        lang_results = [self._attach_quality_metrics(r, parsed_query, semantic_keywords) for r in lang_results]
        results.extend(lang_results)
        
        # Поиск в фреймворках
        framework_results = self._search_in_frameworks(semantic_keywords, parsed_query["languages"])
        framework_results = [self._attach_quality_metrics(r, parsed_query, semantic_keywords) for r in framework_results]
        results.extend(framework_results)

        fact_results = self._search_in_knowledge_facts(semantic_keywords, parsed_query["languages"])
        fact_results = [self._attach_quality_metrics(r, parsed_query, semantic_keywords) for r in fact_results]
        results.extend(fact_results)
        
        # Удаляем дубликаты и сортируем по релевантности
        ranked_results = self._deduplicate_and_rank(results, semantic_keywords)
        
        # Принудительный режим: всегда показывать внешние источники
        if include_external_always:
            external_results = self._build_external_fallback_results(keywords, parsed_query)
            return ranked_results + external_results if ranked_results else external_results

        # Если ничего не найдено в онтологии — fallback на внешние источники
        if not ranked_results:
            external_results = self._build_external_fallback_results(keywords, parsed_query)
            return external_results

        # Если найдена только общая карточка языка, но нет содержательных материалов
        # (примеров, документации, статей), добавляем внешние источники в ответ.
        has_substantive = any(r.get("type") in ("publication", "framework", "external_source") for r in ranked_results)
        only_generic_language = ranked_results and all(r.get("type") == "language" for r in ranked_results)
        semantically_specific = (
            len(parsed_query.get("predicates", [])) > 0
            or len(parsed_query.get("concepts", [])) > 0
            or len(parsed_query.get("expanded_keywords", [])) >= 3
        )

        if semantically_specific and only_generic_language and not has_substantive:
            external_results = self._build_external_fallback_results(keywords, parsed_query)
            return ranked_results + external_results

        return ranked_results

    def _parse_semantic_query(self, query: str, languages: Optional[List[str]]) -> Dict:
        """Семантический разбор запроса по сущностям и предикатам."""
        query_lower = query.lower()
        
        alias_to_language = {
            "python": "Python",
            "java": "Java",
            "javascript": "JavaScript",
            "js": "JavaScript",
            "c++": "CPlusPlus",
            "cpp": "CPlusPlus",
            "c#": "CSharp",
            "csharp": "CSharp",
            "c": "C",
        }
        
        detected_languages = set(languages or [])
        for token, lang in alias_to_language.items():
            if re.search(rf"\b{re.escape(token)}\b", query_lower):
                detected_languages.add(lang)
        
        predicate_map = {
            "hasSyntax": ["синтаксис", "syntax", "цикл", "for", "while", "if", "пример кода"],
            "hasExample": ["пример", "example", "код", "snippet", "демо"],
            "hasExplanation": ["что такое", "объясни", "определение", "definition"],
            "hasSource": ["источник", "ссылка", "документация", "книга", "статья"],
        }
        
        detected_predicates = []
        for predicate, triggers in predicate_map.items():
            if any(trigger in query_lower for trigger in triggers):
                detected_predicates.append(predicate)
        
        if not detected_predicates:
            detected_predicates = ["hasExplanation"]
        
        concept_aliases = {
            "forloop": ["for", "цикл for", "цикл"],
            "whileloop": ["while", "цикл while"],
            "listcomprehension": ["list comprehension", "генератор списка"],
        }
        detected_concepts = []
        for concept, aliases in concept_aliases.items():
            if any(alias in query_lower for alias in aliases):
                detected_concepts.append(concept)
        
        expanded_keywords = [kw.strip().lower() for kw in re.split(r"[,\s]+", query) if kw.strip()]
        for concept in detected_concepts:
            if concept not in expanded_keywords:
                expanded_keywords.append(concept)
        for pred in detected_predicates:
            pred_token = pred.replace("has", "").lower()
            if pred_token and pred_token not in expanded_keywords:
                expanded_keywords.append(pred_token)
        
        return {
            "original_query": query,
            "languages": sorted(detected_languages),
            "predicates": detected_predicates,
            "concepts": detected_concepts,
            "expanded_keywords": expanded_keywords,
        }

    def _attach_quality_metrics(self, result: Dict, parsed_query: Dict, keywords: List[str]) -> Dict:
        """Добавляет метрики точности на уровне сущностей и предикатов."""
        result_text = " ".join([
            str(result.get("name", "")),
            str(result.get("title", "")),
            str(result.get("keywords", "")),
            str(result.get("language", "")),
            str(result.get("publication_type", "")),
        ]).lower()
        
        entities = [lang.lower() for lang in parsed_query.get("languages", [])]
        predicates = [p.lower() for p in parsed_query.get("predicates", [])]
        
        entity_accuracy = 100.0
        if entities:
            matched_entities = sum(1 for entity in entities if entity.lower() in result_text)
            entity_accuracy = (matched_entities / len(entities)) * 100.0
        
        predicate_hints = {
            "hassyntax": ["syntax", "синтаксис", "for", "while", "if", "код"],
            "hasexample": ["example", "пример", "snippet", "код"],
            "hasexplanation": ["что", "определение", "definition", "описание"],
            "hassource": ["source", "источник", "url", "ссылка", "документац"],
        }
        predicate_accuracy = 100.0
        if predicates:
            matched_predicates = 0
            for predicate in predicates:
                hints = predicate_hints.get(predicate, [])
                if any(h in result_text for h in hints):
                    matched_predicates += 1
            predicate_accuracy = (matched_predicates / len(predicates)) * 100.0
        
        exactness = min(result.get("relevance", 0.0), 100.0)
        source_quality = 80.0 if result.get("url") else 60.0
        
        total_score = (
            0.3 * entity_accuracy
            + 0.25 * predicate_accuracy
            + 0.25 * exactness
            + 0.2 * source_quality
        )
        
        result["quality"] = {
            "entity_accuracy": round(entity_accuracy, 1),
            "predicate_accuracy": round(predicate_accuracy, 1),
            "answer_exactness": round(exactness, 1),
            "source_quality": round(source_quality, 1),
            "total_score": round(total_score, 1),
        }
        result["relevance"] = max(result.get("relevance", 0.0), result["quality"]["total_score"])
        return result

    def _build_external_fallback_results(self, query: str, parsed_query: Dict) -> List[Dict]:
        """Формирует fallback-результаты из доверенных внешних источников."""
        encoded = quote_plus(query)
        language = parsed_query["languages"][0] if parsed_query["languages"] else None
        
        candidates = [
            {
                "title": f"Поиск в браузере по запросу: '{query}'",
                "url": f"https://www.google.com/search?q={encoded}",
                "source_name": "Browser Search",
            },
            {
                "title": f"Поиск официальной документации по '{query}'",
                "url": f"https://www.google.com/search?q={encoded}+official+documentation",
                "source_name": "Google (official docs)",
            },
            {
                "title": f"Поиск учебных материалов по '{query}'",
                "url": f"https://www.google.com/search?q={encoded}+tutorial+guide+examples",
                "source_name": "Google (tutorials)",
            },
        ]
        
        fallback_results = []
        for idx, item in enumerate(candidates, start=1):
            result = {
                "type": "external_source",
                "name": f"ExternalSource_{idx}",
                "title": item["title"],
                "url": item["url"],
                "source_name": item["source_name"],
                "language": language,
                "keywords": query,
                "publication_type": "ExternalSource",
                "relevance": max(55.0, 75.0 - idx * 4),
                "is_fallback": True,
                "fallback_reason": "not_found_in_ontology",
            }
            fallback_results.append(self._attach_quality_metrics(result, parsed_query, parsed_query["expanded_keywords"]))
        
        return fallback_results

    def _search_in_knowledge_facts(self, keywords: List[str], languages: Optional[List[str]]) -> List[Dict]:
        """Поиск сохраненных фактов знаний (объяснения/синтаксис/примеры)."""
        results = []
        try:
            for subject in self.g.subjects(RDF.type, self.NS.KnowledgeFact):
                fact_text = self.g.value(subject, self.NS.factText)
                predicate_type = self.g.value(subject, self.NS.predicateType)
                material_type = self.g.value(subject, self.NS.materialType)
                source_url = self.g.value(subject, self.NS.hasSource)
                source_name = self.g.value(subject, self.NS.sourceName)
                query_text = self.g.value(subject, self.NS.queryText)
                title = self.g.value(subject, self.NS.title)
                lang_uri = self.g.value(subject, self.NS.aboutLanguage)

                language_name = str(lang_uri).split("/")[-1] if lang_uri else None
                if languages and language_name and language_name not in languages:
                    continue

                combined = " ".join([
                    str(fact_text or ""),
                    str(predicate_type or ""),
                    str(query_text or ""),
                    str(title or ""),
                    str(language_name or ""),
                ]).lower()
                if keywords and not any(kw in combined for kw in keywords):
                    continue

                relevance = self._calculate_relevance(keywords, [combined])
                results.append({
                    "type": "knowledge_fact",
                    "name": str(subject).split("/")[-1],
                    "title": str(title) if title else "Сохраненный факт",
                    "fact_text": str(fact_text) if fact_text else "",
                    "predicate_type": str(predicate_type) if predicate_type else "",
                    "material_type": str(material_type) if material_type else "Article",
                    "url": str(source_url) if source_url else None,
                    "source_name": str(source_name) if source_name else "Source",
                    "language": language_name,
                    "keywords": str(query_text) if query_text else "",
                    "publication_type": "KnowledgeFact",
                    "relevance": relevance,
                    "uri": str(subject),
                })
        except Exception as e:
            print(f"⚠️ Ошибка поиска по сохраненным фактам: {e}")
        return results

    def _ingest_external_results(self, external_results: List[Dict], parsed_query: Dict):
        """Сохраняет fallback-источники в онтологию для последующих запросов."""
        if not external_results:
            return
        
        try:
            retrieved_at = datetime.utcnow().isoformat()
            self.g.add((self.NS.SourceDocument, RDF.type, RDFS.Class))
            self.g.add((self.NS.hasSource, RDF.type, RDF.Property))
            self.g.add((self.NS.sourceName, RDF.type, RDF.Property))
            self.g.add((self.NS.retrievedAt, RDF.type, RDF.Property))
            self.g.add((self.NS.confidenceScore, RDF.type, RDF.Property))
            self.g.add((self.NS.queryText, RDF.type, RDF.Property))
            
            for idx, result in enumerate(external_results, start=1):
                source_uri = self.NS[f"ExternalSource_{int(time.time())}_{idx}"]
                self.g.add((source_uri, RDF.type, self.NS.SourceDocument))
                self.g.add((source_uri, self.NS.title, Literal(result.get("title", ""))))
                self.g.add((source_uri, self.NS.hasSource, URIRef(result.get("url"))))
                self.g.add((source_uri, self.NS.sourceName, Literal(result.get("source_name", "External"))))
                self.g.add((source_uri, self.NS.retrievedAt, Literal(retrieved_at)))
                self.g.add((source_uri, self.NS.confidenceScore, Literal(float(result.get("quality", {}).get("total_score", 0.0)))))
                self.g.add((source_uri, self.NS.queryText, Literal(parsed_query.get("original_query", ""))))
                
                for lang in parsed_query.get("languages", []):
                    self.g.add((source_uri, self.NS.aboutLanguage, self.NS[lang]))
            
            self.g.serialize(destination=str(self.ontology_path), format="turtle")
            print(f"✅ Fallback-источники добавлены в онтологию: {len(external_results)}")
        except Exception as e:
            print(f"⚠️ Не удалось сохранить fallback-источники в онтологию: {e}")

    def save_external_result(
        self,
        title: str,
        url: str,
        source_name: str,
        query_text: str,
        language: Optional[str] = None,
        confidence_score: Optional[float] = None
    ) -> bool:
        """Явно сохраняет выбранный внешний источник в онтологию."""
        if not title or not url:
            return False
        
        parsed_query = {
            "original_query": query_text or "",
            "languages": [language] if language else [],
            "predicates": [],
            "concepts": [],
            "expanded_keywords": [kw.strip().lower() for kw in re.split(r"[,\s]+", query_text or "") if kw.strip()],
        }
        result = {
            "type": "external_source",
            "title": title,
            "url": url,
            "source_name": source_name or "Browser Search",
            "language": language,
            "quality": {"total_score": float(confidence_score) if confidence_score is not None else 70.0},
            "is_fallback": True,
        }
        try:
            self._ingest_external_results([result], parsed_query)
            return True
        except Exception:
            return False

    def _sanitize_uri_token(self, text: str) -> str:
        token = re.sub(r"[^a-zA-Z0-9_]+", "_", (text or "").strip())
        token = re.sub(r"_+", "_", token).strip("_")
        return token or "Item"

    def _normalize_language_name(self, language: str) -> str:
        """Приводит пользовательское имя языка к имени индивида в онтологии."""
        raw = (language or "").strip()
        lowered = raw.lower()
        mapping = {
            "c++": "CPlusPlus",
            "cpp": "CPlusPlus",
            "c#": "CSharp",
            "csharp": "CSharp",
            "js": "JavaScript",
            "javascript": "JavaScript",
            "python": "Python",
            "java": "Java",
            "c": "C",
        }
        if lowered in mapping:
            return mapping[lowered]
        return self._sanitize_uri_token(raw)

    def save_knowledge_fact(
        self,
        query_text: str,
        language: str,
        material_type: str,
        fact_text: str,
        source_url: str,
        source_name: str = "Browser Source",
        title: Optional[str] = None
    ) -> bool:
        """Сохраняет факт знаний с привязкой к источнику и языку."""
        if not fact_text or not source_url:
            return False
        try:
            self.g.add((self.NS.KnowledgeFact, RDF.type, RDFS.Class))
            self.g.add((self.NS.factText, RDF.type, RDF.Property))
            self.g.add((self.NS.predicateType, RDF.type, RDF.Property))
            self.g.add((self.NS.materialType, RDF.type, RDF.Property))
            self.g.add((self.NS.basedOnQuery, RDF.type, RDF.Property))

            stamp = int(time.time())
            normalized_language = self._normalize_language_name(language or "")
            lang_token = self._sanitize_uri_token(normalized_language or "General")
            query_token = self._sanitize_uri_token(query_text or "Query")
            fact_uri = self.NS[f"KnowledgeFact_{lang_token}_{query_token}_{stamp}"]

            self.g.add((fact_uri, RDF.type, self.NS.KnowledgeFact))
            self.g.add((fact_uri, self.NS.factText, Literal(fact_text.strip())))
            material_type = (material_type or "Article").strip()
            predicate_by_material = {
                "Article": "hasExplanation",
                "Documentation": "hasSyntax",
                "Guide": "hasExplanation",
                "Tutorial": "hasExample",
                "Book": "hasExplanation",
            }
            predicate_value = predicate_by_material.get(material_type, "hasExplanation")
            self.g.add((fact_uri, self.NS.materialType, Literal(material_type)))
            self.g.add((fact_uri, self.NS.predicateType, Literal(predicate_value)))
            self.g.add((fact_uri, self.NS.basedOnQuery, Literal((query_text or "").strip())))
            self.g.add((fact_uri, self.NS.queryText, Literal((query_text or "").strip())))
            self.g.add((fact_uri, self.NS.hasSource, URIRef(source_url.strip())))
            self.g.add((fact_uri, self.NS.sourceName, Literal((source_name or "Browser Source").strip())))
            self.g.add((fact_uri, self.NS.retrievedAt, Literal(datetime.utcnow().isoformat())))
            self.g.add((fact_uri, self.NS.confidenceScore, Literal(90.0)))
            self.g.add((fact_uri, self.NS.title, Literal((title or "Сохраненный факт").strip())))

            if normalized_language:
                self.g.add((fact_uri, self.NS.aboutLanguage, self.NS[normalized_language]))

            self.g.serialize(destination=str(self.ontology_path), format="turtle")
            print("✅ Факт знаний сохранен в онтологию")
            return True
        except Exception as e:
            print(f"⚠️ Ошибка сохранения факта знаний: {e}")
            return False
    
    def _search_in_publications(self, keywords: List[str], languages: Optional[List[str]]) -> List[Dict]:
        """Поиск в публикациях (книги, статьи)"""
        results = []
        
        # SPARQL запрос для поиска публикаций
        # Создаем фильтры для ключевых слов
        keyword_conditions = []
        for kw in keywords:
            kw_lower = kw.lower()
            kw_escaped = kw.replace('"', '\\"')
            # Поиск в названии, ключевых словах и типе публикации
            keyword_conditions.append(f"""
            (CONTAINS(LCASE(STR(?title)), "{kw_escaped}") || 
             CONTAINS(LCASE(STR(?keywords)), "{kw_escaped}") ||
             (STR(?pubType) = "http://www.semanticweb.org/дмитрий/ontologies/2025/10/untitled-ontology-7/Book" && "{kw_lower}" = "книга") ||
             (STR(?pubType) = "http://www.semanticweb.org/дмитрий/ontologies/2025/10/untitled-ontology-7/Book" && "{kw_lower}" = "book") ||
             (STR(?pubType) = "http://www.semanticweb.org/дмитрий/ontologies/2025/10/untitled-ontology-7/Documentation" && "{kw_lower}" = "документация") ||
             (STR(?pubType) = "http://www.semanticweb.org/дмитрий/ontologies/2025/10/untitled-ontology-7/Tutorial" && "{kw_lower}" = "туториал") ||
             (STR(?pubType) = "http://www.semanticweb.org/дмитрий/ontologies/2025/10/untitled-ontology-7/Article" && "{kw_lower}" = "статья"))
            """)
        
        keyword_filter = " || ".join(keyword_conditions) if keyword_conditions else "true"
        
        # Добавляем фильтр по языкам если указан
        lang_filter_parts = []
        if languages:
            lang_conditions = [f"?lang = onto:{lang}" for lang in languages]
            lang_filter_parts.append(f"({' || '.join(lang_conditions)})")
        
        # Формируем полный фильтр
        filter_parts = [f"({keyword_filter})"]
        filter_parts.extend(lang_filter_parts)
        full_filter = " && ".join(filter_parts)
        
        query = f"""
        SELECT DISTINCT ?pub ?title ?keywords ?lang ?author ?url WHERE {{
          ?pub a ?pubType .
          FILTER(?pubType IN (onto:Book, onto:Article, onto:Documentation, onto:Tutorial))
          
          OPTIONAL {{ ?pub onto:title ?title . }}
          OPTIONAL {{ ?pub onto:keywords ?keywords . }}
          OPTIONAL {{ ?pub onto:aboutLanguage ?lang . }}
          OPTIONAL {{ ?pub onto:writtenBy ?author . }}
          OPTIONAL {{ ?pub onto:url ?url . }}
          
          FILTER({full_filter})
        }}
        """
        
        try:
            query_result = self.g.query(query, initNs={"onto": self.NS})
            
            for row in query_result:
                pub_uri = str(row[0])
                pub_name = pub_uri.split("/")[-1]
                
                title = str(row[1]) if row[1] else ""
                keywords_str = str(row[2]) if row[2] else ""
                lang_uri = str(row[3]) if row[3] else ""
                author_uri = str(row[4]) if row[4] else ""
                url = str(row[5]) if len(row) > 5 and row[5] else None
                
                lang_name = lang_uri.split("/")[-1] if lang_uri else None
                author_name = author_uri.split("/")[-1] if author_uri else None
                
                # Определяем тип публикации
                pub_type = None
                pub_uri_obj = self.NS[pub_name]
                if (pub_uri_obj, RDF.type, self.NS.Book) in self.g:
                    pub_type = 'Book'
                elif (pub_uri_obj, RDF.type, self.NS.Article) in self.g:
                    pub_type = 'Article'
                elif (pub_uri_obj, RDF.type, self.NS.Documentation) in self.g:
                    pub_type = 'Documentation'
                elif (pub_uri_obj, RDF.type, self.NS.Tutorial) in self.g:
                    pub_type = 'Tutorial'
                
                # Вычисляем релевантность
                relevance = self._calculate_relevance(keywords, [title, keywords_str])
                
                # Год публикации (если есть в онтологии)
                year = None
                try:
                    year_val = self.g.value(pub_uri_obj, self.NS.yearCreated)
                    if year_val:
                        year = int(year_val.toPython())
                except Exception:
                    year = None
                
                results.append({
                    'type': 'publication',
                    'name': pub_name,
                    'title': title,
                    'keywords': keywords_str,
                    'language': lang_name,
                    'author': author_name,
                    'url': url,
                    'publication_type': pub_type,
                    'year': year,
                    'relevance': relevance,
                    'uri': pub_uri
                })
        except Exception as e:
            print(f"⚠️ Ошибка поиска в публикациях: {e}")
        
        return results
    
    def _search_in_languages(self, keywords: List[str], languages: Optional[List[str]]) -> List[Dict]:
        """Поиск в языках программирования"""
        results = []
        
        # SPARQL запрос для поиска языков
        # Фильтр по ключевым словам в различных свойствах
        keyword_conditions = []
        for kw in keywords:
            kw_escaped = kw.replace('"', '\\"')
            keyword_conditions.append(f"""
            (CONTAINS(LCASE(STR(?creator)), "{kw_escaped}") ||
             CONTAINS(LCASE(STR(?paradigm)), "{kw_escaped}") ||
             CONTAINS(LCASE(STR(?domain)), "{kw_escaped}") ||
             CONTAINS(LCASE(STR(?framework)), "{kw_escaped}") ||
             CONTAINS(LCASE(STR(?typeSystem)), "{kw_escaped}") ||
             CONTAINS(LCASE(STR(?learningCurve)), "{kw_escaped}") ||
             CONTAINS(LCASE(STR(?lang)), "{kw_escaped}"))
            """)
        
        keyword_filter = " || ".join(keyword_conditions) if keyword_conditions else "true"
        
        # Формируем полный фильтр
        filter_parts = []
        if languages:
            lang_conditions = [f"?lang = onto:{lang}" for lang in languages]
            filter_parts.append(f"({' || '.join(lang_conditions)})")
        filter_parts.append(f"({keyword_filter})")
        full_filter = " && ".join(filter_parts) if filter_parts else "true"
        
        query = f"""
        SELECT DISTINCT ?lang ?creator ?paradigm ?domain ?framework ?typeSystem ?learningCurve WHERE {{
          ?lang a onto:ProgrammingLanguage .
          
          OPTIONAL {{ ?lang onto:creator ?creator . }}
          OPTIONAL {{ ?lang onto:hasParadigm ?paradigm . }}
          OPTIONAL {{ ?lang onto:usedInDomain ?domain . }}
          OPTIONAL {{ ?lang onto:hasFramework ?framework . }}
          OPTIONAL {{ ?lang onto:hasTypeSystem ?typeSystem . }}
          OPTIONAL {{ ?lang onto:learningCurve ?learningCurve . }}
          
          FILTER({full_filter})
        }}
        """
        
        try:
            query_result = self.g.query(query, initNs={"onto": self.NS})
            
            for row in query_result:
                lang_uri = str(row[0])
                lang_name = lang_uri.split("/")[-1]
                
                # Собираем все свойства
                properties = {
                    'creator': str(row[1]) if row[1] else None,
                    'paradigm': str(row[2]).split("/")[-1] if row[2] else None,
                    'domain': str(row[3]).split("/")[-1] if row[3] else None,
                    'framework': str(row[4]).split("/")[-1] if row[4] else None,
                    'typeSystem': str(row[5]).split("/")[-1] if row[5] else None,
                    'learningCurve': str(row[6]) if row[6] else None
                }
                
                # Получаем дополнительные данные
                lang_data = self._get_language_full_data(lang_name)
                
                # Вычисляем релевантность
                search_text = " ".join([str(v) for v in properties.values() if v] + [lang_name])
                relevance = self._calculate_relevance(keywords, [search_text])
                
                results.append({
                    'type': 'language',
                    'name': lang_name,
                    'display_name': self._get_display_name(lang_name),
                    'properties': properties,
                    'data': lang_data,
                    'relevance': relevance,
                    'uri': lang_uri
                })
        except Exception as e:
            print(f"⚠️ Ошибка поиска в языках: {e}")
        
        return results
    
    def _search_in_frameworks(self, keywords: List[str], languages: Optional[List[str]]) -> List[Dict]:
        """Поиск в фреймворках"""
        results = []
        
        keyword_conditions = []
        for kw in keywords:
            kw_escaped = kw.replace('"', '\\"')
            keyword_conditions.append(f"""
            (CONTAINS(LCASE(STR(?framework)), "{kw_escaped}") ||
             CONTAINS(LCASE(STR(?lang)), "{kw_escaped}"))
            """)
        
        keyword_filter = " || ".join(keyword_conditions) if keyword_conditions else "true"
        
        # Формируем полный фильтр
        filter_parts = []
        if languages:
            lang_conditions = [f"?lang = onto:{lang}" for lang in languages]
            filter_parts.append(f"({' || '.join(lang_conditions)})")
        filter_parts.append(f"({keyword_filter})")
        full_filter = " && ".join(filter_parts) if filter_parts else "true"
        
        query = f"""
        SELECT DISTINCT ?framework ?lang WHERE {{
          ?framework a onto:Framework .
          OPTIONAL {{ ?framework onto:writtenIn ?lang . }}
          
          FILTER({full_filter})
        }}
        """
        
        try:
            query_result = self.g.query(query, initNs={"onto": self.NS})
            
            for row in query_result:
                framework_uri = str(row[0])
                framework_name = framework_uri.split("/")[-1]
                lang_uri = str(row[1]) if row[1] else ""
                lang_name = lang_uri.split("/")[-1] if lang_uri else None
                
                search_text = f"{framework_name} {lang_name}" if lang_name else framework_name
                relevance = self._calculate_relevance(keywords, [search_text])
                
                results.append({
                    'type': 'framework',
                    'name': framework_name,
                    'language': lang_name,
                    'relevance': relevance,
                    'uri': framework_uri
                })
        except Exception as e:
            print(f"⚠️ Ошибка поиска в фреймворках: {e}")
        
        return results
    
    def _get_language_full_data(self, lang_name: str) -> Dict:
        """Получение полных данных о языке"""
        lang_uri = self.NS[lang_name]
        
        query = """
        SELECT ?prop ?value WHERE {
          ?lang ?prop ?value .
          FILTER(?lang = onto:%s)
        }
        """ % lang_name
        
        data = {}
        
        try:
            results = self.g.query(query, initNs={"onto": self.NS})
            
            for row in results:
                prop_name = str(row[0]).split("/")[-1]
                value = row[1]
                
                # Преобразуем значения
                if isinstance(value, Literal):
                    value_str = str(value)
                    # Пробуем преобразовать в число
                    try:
                        if '.' in value_str:
                            value = float(value_str)
                        else:
                            value = int(value_str)
                    except:
                        value = value_str
                else:
                    value_str = str(value)
                    value = value_str.split("/")[-1]
                
                # Группируем множественные значения
                if prop_name in data:
                    if not isinstance(data[prop_name], list):
                        data[prop_name] = [data[prop_name]]
                    data[prop_name].append(value)
                else:
                    data[prop_name] = value
        except Exception as e:
            print(f"⚠️ Ошибка получения данных языка {lang_name}: {e}")
        
        return data
    
    def _calculate_relevance(self, keywords: List[str], texts: List[str]) -> float:
        """Вычисление релевантности результата"""
        if not texts:
            return 0.0
        
        text = " ".join(texts).lower()
        matches = sum(1 for kw in keywords if kw in text)
        
        # Бонус за точное совпадение
        exact_matches = sum(1 for kw in keywords if kw == text.strip())
        
        relevance = (matches / len(keywords)) * 100 + exact_matches * 20
        
        return min(relevance, 100.0)
    
    def _deduplicate_and_rank(self, results: List[Dict], keywords: List[str]) -> List[Dict]:
        """Удаление дубликатов и сортировка по релевантности"""
        seen = set()
        unique_results = []
        
        for result in results:
            # Создаем уникальный ключ
            key = (result['type'], result.get('name', ''), result.get('uri', ''))
            
            if key not in seen:
                seen.add(key)
                unique_results.append(result)
        
        # Сортируем по релевантности
        unique_results.sort(key=lambda x: x.get('relevance', 0), reverse=True)
        
        return unique_results
    
    def _get_display_name(self, internal_name: str) -> str:
        """Преобразование внутреннего имени в отображаемое"""
        name_mapping = {
            'Python': 'Python',
            'Java': 'Java',
            'JavaScript': 'JavaScript',
            'C': 'C',
            'CPlusPlus': 'C++',
            'CSharp': 'C#'
        }
        return name_mapping.get(internal_name, internal_name)
    
    def search_by_language(self, language_name: str) -> Dict:
        """Поиск информации о конкретном языке"""
        lang_data = self._get_language_full_data(language_name)
        
        if not lang_data:
            return None
        
        # Получаем связанные публикации
        publications = self._get_language_publications(language_name)
        
        # Получаем связанные фреймворки
        frameworks = self._get_language_frameworks(language_name)
        
        return {
            'language': language_name,
            'display_name': self._get_display_name(language_name),
            'data': lang_data,
            'publications': publications,
            'frameworks': frameworks
        }
    
    def _get_language_publications(self, lang_name: str) -> List[Dict]:
        """Получение публикаций о языке"""
        query = """
        SELECT ?pub ?title ?keywords ?author WHERE {
          ?pub onto:aboutLanguage onto:%s .
          OPTIONAL { ?pub onto:title ?title . }
          OPTIONAL { ?pub onto:keywords ?keywords . }
          OPTIONAL { ?pub onto:writtenBy ?author . }
        }
        """ % lang_name
        
        publications = []
        
        try:
            results = self.g.query(query, initNs={"onto": self.NS})
            
            for row in results:
                pub_uri = str(row[0])
                pub_name = pub_uri.split("/")[-1]
                
                publications.append({
                    'name': pub_name,
                    'title': str(row[1]) if row[1] else "",
                    'keywords': str(row[2]) if row[2] else "",
                    'author': str(row[3]).split("/")[-1] if row[3] else None
                })
        except Exception as e:
            print(f"⚠️ Ошибка получения публикаций: {e}")
        
        return publications
    
    def _get_language_frameworks(self, lang_name: str) -> List[str]:
        """Получение фреймворков языка"""
        query = """
        SELECT ?framework WHERE {
          ?framework onto:writtenIn onto:%s .
        }
        """ % lang_name
        
        frameworks = []
        
        try:
            results = self.g.query(query, initNs={"onto": self.NS})
            
            for row in results:
                framework_uri = str(row[0])
                framework_name = framework_uri.split("/")[-1]
                frameworks.append(framework_name)
        except Exception as e:
            print(f"⚠️ Ошибка получения фреймворков: {e}")
        
        return frameworks
    
    def get_all_languages(self) -> List[str]:
        """Получение списка всех языков"""
        query = """
        SELECT DISTINCT ?lang WHERE {
          ?lang a onto:ProgrammingLanguage .
        }
        """
        
        languages = []
        
        try:
            results = self.g.query(query, initNs={"onto": self.NS})
            
            for row in results:
                lang_uri = str(row[0])
                lang_name = lang_uri.split("/")[-1]
                languages.append(lang_name)
        except Exception as e:
            print(f"⚠️ Ошибка получения списка языков: {e}")
        
        return sorted(languages)

def test_search():
    """Тестирование поискового модуля"""
    search = OntologySearch()
    
    print("🔍 ТЕСТИРОВАНИЕ ПОИСКА")
    print("=" * 60)
    
    # Тест 1: Поиск по ключевым словам
    print("\n1. Поиск по ключевым словам: 'web development'")
    results = search.search_by_keywords("web development")
    print(f"   Найдено результатов: {len(results)}")
    for i, result in enumerate(results[:5], 1):
        print(f"   {i}. [{result['type']}] {result.get('name', result.get('title', 'N/A'))} (релевантность: {result.get('relevance', 0):.1f}%)")
    
    # Тест 2: Поиск по конкретному языку
    print("\n2. Поиск информации о Python")
    lang_info = search.search_by_language("Python")
    if lang_info:
        print(f"   Язык: {lang_info['display_name']}")
        print(f"   Свойств: {len(lang_info['data'])}")
        print(f"   Публикаций: {len(lang_info['publications'])}")
        print(f"   Фреймворков: {len(lang_info['frameworks'])}")
    
    # Тест 3: Поиск с фильтром по языкам
    print("\n3. Поиск 'object oriented' в Python и Java")
    results = search.search_by_keywords("object oriented", languages=["Python", "Java"])
    print(f"   Найдено результатов: {len(results)}")
    for i, result in enumerate(results[:3], 1):
        print(f"   {i}. [{result['type']}] {result.get('name', result.get('title', 'N/A'))}")

if __name__ == "__main__":
    test_search()

