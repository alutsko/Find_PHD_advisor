# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import mysql.connector

cnx = mysql.connector.connect(user='root', password='test_root',
                              host='127.0.0.1',
                              database='academicworld')
cursor = cnx.cursor()

default_uni = 'university of illinois at urbana champaign'

text ="SELECT name, keyword_count, score_sum, keyword_count*score_sum AS keyword_relevance " +\
"FROM "+\
"(SELECT keyword.name, COUNT(*) as keyword_count, SUM(faculty_keyword.score) as score_sum "+\
"FROM faculty, university, faculty_keyword, keyword "+\
"WHERE faculty.university_id = university.id AND LOWER(university.name) = '"+ default_uni +"' "+\
"AND faculty.id = faculty_keyword.faculty_id AND faculty_keyword.keyword_id = keyword.id "+\
"GROUP BY keyword.name) AS keyword_metrics "+\
"ORDER BY keyword_relevance DESC "+\
"LIMIT 10"

query = (text)
cursor.execute(query)
default_df = pd.DataFrame(cursor)
default_df.columns =['Keyword', 'Keyword Count', 'Keyword Score Sum', 'Keyword Relevance']
    
# Initialize the app - incorporate a Dash Mantine theme
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets)



# App layout

first_card = dbc.Card(dbc.CardBody(
    [
        dmc.Title('Find University Top Keywords'),
        html.Br(),

        dcc.Input(id='uni-search', type='search', placeholder='Search Universities...', debounce=True),
        html.Br(),
        html.Hr(),
        dbc.Row([dbc.Col(children = [html.Div("Displaying top results for: ")]), dbc.Col(children = [html.Div(id="display_uni", children=[default_uni])])]),
        html.Br(),
            
        # dash_table.DataTable(res.to_dict('records'), id='table'),
        dcc.Graph(id = 'pie', figure = px.pie(default_df, values='Keyword Count', names='Keyword', title='Top 10 Keywords by Count', hole=0.25))
                
    ])
)

from neo4j import GraphDatabase
import neo4j
from PIL import Image
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "ilovecs411")
driver =  GraphDatabase.driver(URI, auth=AUTH)
default_keyword = "machine learning"
default_neo4j = driver.execute_query(
    "MATCH (uni:INSTITUTE)<-[:AFFILIATION_WITH]-(fac:FACULTY)-[:PUBLISH]->(pub:PUBLICATION)-[:LABEL_BY]->(keyword:KEYWORD WHERE keyword.name = \"" + default_keyword +"\") RETURN fac.name, fac.photoUrl, fac.position, fac.researchInterest, fac.phone, fac.email, uni.name, uni.photoUrl, COUNT(pub) ORDER BY COUNT(pub) DESC LIMIT 5",
    database_="academicworld", 
    result_transformer_= neo4j.Result.to_df
    )

def create_faculty_cards(faculty_df):
    card_list = []
    for index in faculty_df.index:
        card = dbc.Card(
                dbc.CardBody(
                    dbc.Col([dbc.Row([
                            dbc.Col([html.Div("Rank #" + str(index+1)),
                                     html.Div("Name: " + str(faculty_df['fac.name'][index])),
                                     html.Div("Institution: " + str(faculty_df['uni.name'][index]))]), 
                            dbc.Col([html.Img(src=faculty_df['fac.photoUrl'][index], style= {"height": "200px", "width": "150px"})]), 
                            dbc.Col([
                                    html.Div("Position: " + str(faculty_df['fac.position'][index])), 
                                    html.Div("Email: " + str(faculty_df['fac.email'][index])), 
                                    html.Div("Phone: " + str(faculty_df['fac.phone'][index])),
                                    html.Img(src=faculty_df['uni.photoUrl'][index], style={"height": "100px", "width": "100px"})])
                            ])])
                )
            
        )
        card_list.append(card)
    return card_list


second_card = dbc.Card(dbc.CardBody(
    [
        dmc.Title('Find Faculty Best Keywords'),
        html.Br(),

        dcc.Input(id='keyword-search', type='search', placeholder='Search Keywords...', debounce=True),
        html.Br(),
        html.Hr(),
        dbc.Row([dbc.Col(children = [html.Div("Displaying top faculty for: ")]), dbc.Col(children = [html.Div(id="display_keyword", children=[default_keyword])])]),
        html.Br(),
        dbc.Col(id = 'faculty-col', children = create_faculty_cards(default_neo4j))
                 
    ])
)

app.layout = dbc.Row(
    [
        dbc.Col(first_card),
        dbc.Col(second_card)
    ]
)

# Widget 1
@app.callback(
    Output('display_uni', 'children'),
    [Input('uni-search', 'value')],
    prevent_initial_call = True
)
def display_search(value):
    return f'{value.lower()}'

@app.callback(
    Output('pie', 'figure'),
    [Input('uni-search', 'value')],
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
    fig = ""

    if not res.empty:
        res.columns =['Keyword', 'Keyword Count', 'Keyword Score Sum', 'Keyword Relevance']
        # res_dict = res.to_dict('records')
        # data = res_dict
        fig = px.pie(res, values=res['Keyword Relevance'], names=res['Keyword'], hole=0.25)
    else:
        # empty = pd.DataFrame(data = [['']],columns = ['University Not Found'])
        # data = empty.to_dict('records')
        # fig = px.pie(default_df, values=default_df['Keyword Count'], names=default_df['Keyword'], hole=0.25)
        raise PreventUpdate
    
   
    return fig

# Widget 2
@app.callback(
    Output('display_keyword', 'children'),
    [Input('keyword-search', 'value')],
    prevent_initial_call = True
)
def display_search(value):
    return f'{value.lower()}'
@app.callback(
    Output('faculty-col', 'children'),
    [Input('keyword-search', 'value')],
    prevent_initial_call = True
)
def update_output(value):
    driver =  GraphDatabase.driver(URI, auth=AUTH)
    keyword = value
    faculty_df = driver.execute_query(
        "MATCH (uni:INSTITUTE)<-[:AFFILIATION_WITH]-(fac:FACULTY)-[:PUBLISH]->(pub:PUBLICATION)-[:LABEL_BY]->(keyword:KEYWORD WHERE keyword.name = \"" + keyword +"\") RETURN fac.name, fac.photoUrl, fac.position, fac.researchInterest, fac.phone, fac.email, uni.name, uni.photoUrl, COUNT(pub) ORDER BY COUNT(pub) DESC LIMIT 5",
        database_="academicworld", 
        result_transformer_= neo4j.Result.to_df
        )
    return create_faculty_cards(faculty_df)

# Run the App
if __name__ == '__main__':
    app.run(debug=True)

cnx.close()