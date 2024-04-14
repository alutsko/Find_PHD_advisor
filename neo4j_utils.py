from neo4j import GraphDatabase
import neo4j
from PIL import Image

def query_neo4j(keyword):
    URI = "bolt://localhost:7687"
    AUTH = ("neo4j", "ilovecs411")
    driver =  GraphDatabase.driver(URI, auth=AUTH)

    default_neo4j = driver.execute_query(
        "MATCH (uni:INSTITUTE)<-[:AFFILIATION_WITH]-(fac:FACULTY)-[:PUBLISH]->(pub:PUBLICATION)-[:LABEL_BY]->(keyword:KEYWORD WHERE keyword.name = \"" + keyword +"\") RETURN fac.name, fac.photoUrl, fac.position, fac.researchInterest, fac.phone, fac.email, uni.name, uni.photoUrl, COUNT(pub) ORDER BY COUNT(pub) DESC LIMIT 5",
        database_="academicworld", 
        result_transformer_= neo4j.Result.to_df
        )
    return default_neo4j