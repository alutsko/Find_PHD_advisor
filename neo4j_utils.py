from neo4j import GraphDatabase
import neo4j
from PIL import Image

def neo4j_faculty_keywords(keyword):
    URI = "bolt://localhost:7687"
    AUTH = ("neo4j", "ilovecs411")
    driver =  GraphDatabase.driver(URI, auth=AUTH)

    neo4j_query_res = driver.execute_query(
        "MATCH (uni:INSTITUTE)<-[:AFFILIATION_WITH]-(fac:FACULTY)-[:PUBLISH]->(pub:PUBLICATION)-[:LABEL_BY]->(keyword:KEYWORD WHERE keyword.name = \"" + keyword +"\") RETURN fac.name, fac.photoUrl, fac.position, fac.researchInterest, fac.phone, fac.email, uni.name, uni.photoUrl, COUNT(pub) ORDER BY COUNT(pub) DESC LIMIT 5",
        database_="academicworld", 
        result_transformer_= neo4j.Result.to_df
        )
    return neo4j_query_res

def neo4j_find_faculty(name):
    URI = "bolt://localhost:7687"
    AUTH = ("neo4j", "ilovecs411")
    driver =  GraphDatabase.driver(URI, auth=AUTH)

    neo4j_query_res = driver.execute_query(
        "MATCH (fac:FACULTY WHERE fac.name CONTAINS \"" + name +"\")-[]->(uni:INSTITUTE) RETURN fac.id, fac.name AS Name, uni.name AS Institution, fac.position AS Position, fac.email AS Email, fac.phone AS Phone, fac.photoUrl as PhotoURL",
        database_="academicworld", 
        result_transformer_= neo4j.Result.to_df
        )
    # print(neo4j_query_res['Name', 'Institution', 'Position', 'Email', 'Phone', 'PhotoURL'])
    return neo4j_query_res