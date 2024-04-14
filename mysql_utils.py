import mysql.connector
import pandas as pd

# returns resulting dataframe from a query with given university name
def make_query(uni):

    cnx = mysql.connector.connect(user='root', password='test_root',
                                host='127.0.0.1',
                                database='academicworld')
    cursor = cnx.cursor()

    query =("SELECT name, keyword_count, score_sum, keyword_count*score_sum AS keyword_relevance " +\
    "FROM "+\
    "(SELECT keyword.name, COUNT(*) as keyword_count, SUM(faculty_keyword.score) as score_sum "+\
    "FROM faculty, university, faculty_keyword, keyword "+\
    "WHERE faculty.university_id = university.id AND LOWER(university.name) = '"+ uni.lower() +"' "+\
    "AND faculty.id = faculty_keyword.faculty_id AND faculty_keyword.keyword_id = keyword.id "+\
    "GROUP BY keyword.name) AS keyword_metrics "+\
    "ORDER BY keyword_relevance DESC "+\
    "LIMIT 10")

    cursor.execute(query)
    res = pd.DataFrame(cursor)
    cnx.close()

    if not res.empty:
        res.columns =['Keyword', 'Keyword Count', 'Keyword Score Sum', 'Keyword Relevance']
        return res
       
   
    else:
        empty = pd.DataFrame()
        return empty

