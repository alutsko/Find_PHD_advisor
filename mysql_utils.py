import mysql.connector
import pandas as pd

# connect to sql db
def connect_to_sql():
    cnx = mysql.connector.connect(user='root', password='test_root',
                            host='127.0.0.1',
                            database='academicworld')
    return cnx

def mysql_get_uni_from_id(uni_id):
    cnx = connect_to_sql()
    cursor = cnx.cursor()

    query =("SELECT name FROM university WHERE university.id = " + str(uni_id) + " ")
    cursor.execute(query)
    res = pd.DataFrame(cursor)
    cnx.close()
    if not res.empty:
        res.columns =['uniName']
        return res['uniName'][0] 
    else:
        empty = pd.DataFrame()
        return empty

# returns resulting dataframe from a query with given university name
def mysql_keyword_relevance(uni_id):

    cnx = connect_to_sql()
    cursor = cnx.cursor()

    query =("SELECT name, keyword_count, score_sum, keyword_count*score_sum AS keyword_relevance " +\
    "FROM "+\
    "(SELECT keyword.name, COUNT(*) as keyword_count, SUM(faculty_keyword.score) as score_sum "+\
    "FROM faculty, university, faculty_keyword, keyword "+\
    "WHERE faculty.university_id = university.id AND university.id = "+ str(uni_id) +" "+\
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


# get dropdown options
def fetch_dropdown_options(table_name, label_column, value_column):
    conn = connect_to_sql()
    cursor = conn.cursor()
    cursor.execute(f"SELECT DISTINCT {label_column}, {value_column} FROM {table_name} ORDER BY {label_column} ASC")
    options = [{'label': row[0], 'value': row[1]} for row in cursor.fetchall()]
    conn.close()
    return options

def GetPublicationsByKeywordAndUniversity(keyword_id, university_id):
    conn = connect_to_sql()
    cursor = conn.cursor(dictionary=True)
    cursor.execute( "CALL GetPublicationsByKeywordAndUniversity(%s, %s)" % (keyword_id, university_id))
    res = pd.DataFrame(cursor)
    conn.close()
    return res

def GetTopUniversitiesByYear(keyword_id):
    conn = connect_to_sql()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("CALL GetTopUniversitiesByYear(%s)" % keyword_id)
    res = pd.DataFrame(cursor)
    conn.close()
    return res