# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc
from PIL import Image
import mysql.connector

cnx = mysql.connector.connect(user='root', password='test_root',
                              host='127.0.0.1',
                              database='academicworld')
cursor = cnx.cursor()

text ="SELECT name, keyword_count, score_sum, keyword_count*score_sum AS keyword_relevance " +\
"FROM "+\
"(SELECT keyword.name, COUNT(*) as keyword_count, SUM(faculty_keyword.score) as score_sum "+\
"FROM faculty, university, faculty_keyword, keyword "+\
"WHERE faculty.university_id = university.id AND LOWER(university.name) = 'massachusetts institute of technology' "+\
"AND faculty.id = faculty_keyword.faculty_id AND faculty_keyword.keyword_id = keyword.id "+\
"GROUP BY keyword.name) AS keyword_metrics "+\
"ORDER BY keyword_relevance DESC "+\
"LIMIT 10"

query = (text)
cursor.execute(query)
res = pd.DataFrame(cursor)
res.columns =['Keyword', 'Keyword Count', 'Keyword Score Sum', 'Keyword Relevance']
    
# Initialize the app - incorporate a Dash Mantine theme
external_stylesheets = [dmc.theme.DEFAULT_COLORS]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = dmc.Container([
    dmc.Title('CS411 Project', color="blue", size="h3"),
    
    dmc.Grid([
        
        dmc.Col([
            dmc.Title('Find University Top Keywords', color="blue", size="normal"),
            dcc.Input(id='search-bar', type='search', placeholder='Search Universities...'),
            dash_table.DataTable(res.to_dict('records'), id='table')
        ], span=6),
    ]),

], fluid=True)

@app.callback(
    Output('table', 'data'),
    [Input('search-bar', 'value')],
    prevent_initial_call = True
)
def update_output(value):
    text ="SELECT name, keyword_count, score_sum, keyword_count*score_sum AS keyword_relevance " +\
    "FROM "+\
    "(SELECT keyword.name, COUNT(*) as keyword_count, SUM(faculty_keyword.score) as score_sum "+\
    "FROM faculty, university, faculty_keyword, keyword "+\
    "WHERE faculty.university_id = university.id AND LOWER(university.name) = '" + value.lower() + "' "+\
    "AND faculty.id = faculty_keyword.faculty_id AND faculty_keyword.keyword_id = keyword.id "+\
    "GROUP BY keyword.name) AS keyword_metrics "+\
    "ORDER BY keyword_relevance DESC "+\
    "LIMIT 10"
    

    query = (text)
    
    cnx = mysql.connector.connect(user='root', password='test_root',
                              host='127.0.0.1',
                              database='academicworld')
    cursor = cnx.cursor()
    cursor.execute(query)
    res = pd.DataFrame(cursor)

    if not res.empty:
        res.columns =['Keyword', 'Keyword Count', 'Keyword Score Sum', 'Keyword Relevance']
        res_dict = res.to_dict('records')
        return res_dict
    else:
        empty = pd.DataFrame(data = [['']],columns = ['University Not Found'])
        return empty.to_dict('records')
   
    return res.to_dict('records')

# Run the App
if __name__ == '__main__':
    app.run(debug=True)

cnx.close()