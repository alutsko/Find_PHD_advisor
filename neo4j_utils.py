from neo4j import GraphDatabase
import neo4j
from PIL import Image

def neo4j_faculty_keywords(keyword):
    URI = "bolt://localhost:7687"
    AUTH = ("neo4j", "ilovecs411")
    driver =  GraphDatabase.driver(URI, auth=AUTH)

    neo4j_query_res = driver.execute_query(
        "MATCH (uni:INSTITUTE)<-[:AFFILIATION_WITH]-(fac:FACULTY)-[:PUBLISH]->(pub:PUBLICATION)-[:LABEL_BY]->(keyword:KEYWORD WHERE keyword.name = \"" + keyword +"\") RETURN fac.id as fac_id, fac.name as Name, fac.photoUrl as PhotoURL, fac.position as Position, fac.researchInterest, fac.phone as Phone, fac.email as Email, uni.name as Institution, uni.photoUrl, COUNT(pub) as pub_count ORDER BY COUNT(pub) DESC LIMIT 5",
        database_="academicworld", 
        result_transformer_= neo4j.Result.to_df
        )
    return neo4j_query_res

def neo4j_find_faculty(name):
    URI = "bolt://localhost:7687"
    AUTH = ("neo4j", "ilovecs411")
    driver =  GraphDatabase.driver(URI, auth=AUTH)

    neo4j_query_res = driver.execute_query(
        "MATCH (fac:FACULTY WHERE fac.name CONTAINS \"" + name +"\")-[]->(uni:INSTITUTE) RETURN fac.id as fac_id, fac.name AS Name, uni.name AS Institution, fac.position AS Position, fac.email AS Email, fac.phone AS Phone, fac.photoUrl as PhotoURL",
        database_="academicworld", 
        result_transformer_= neo4j.Result.to_df
        )
    return neo4j_query_res

def update_faculty_field(fac_id, field, data):
    URI = "bolt://localhost:7687"
    AUTH = ("neo4j", "ilovecs411")
    driver =  GraphDatabase.driver(URI, auth=AUTH)

    query = "MATCH (fac:FACULTY WHERE fac.id = '" + fac_id + "') SET fac." + field + " = '"+ data +"' RETURN fac"
    neo4j_query_res = driver.execute_query(
        query,
        database_="academicworld", 
        result_transformer_= neo4j.Result.to_df
        )
    return neo4j_query_res
