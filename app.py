# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input, State
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import mysql_utils
import neo4j_utils


# Setting up default dashboard display
default_uni = 'university of illinois at urbana champaign'
default_df = mysql_utils.make_query(default_uni)

default_keyword = "machine learning"
default_neo4j = neo4j_utils.neo4j_faculty_keywords(default_keyword)

default_missing_fac_fields = default_neo4j[['fac_id', 'Name', 'Institution', 'Position', 'Email', 'Phone', 'PhotoURL']].to_dict('records')
display_columns = ['Name', 'Institution', 'Position', 'Email', 'Phone', 'PhotoURL']
default_missing_columns = [{"id": i, "name": i} for i in display_columns]

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
        
        dcc.Graph(id = 'pie', figure = px.pie(default_df, values='Keyword Count', names='Keyword', title='Top 10 Keywords by Count', hole=0.25))
                
    ])
)

def create_faculty_cards(faculty_df):
    card_list = []
    for index in faculty_df.index:
        card = dbc.Card(
                dbc.CardBody(
                    dbc.Col([dbc.Row([
                            dbc.Col([html.Div("Rank #" + str(index+1)),
                                     html.Div("Name: " + str(faculty_df['Name'][index])),
                                     html.Div("Institution: " + str(faculty_df['Institution'][index])),
                                     html.Div("Number papers with keyword: " + str(faculty_df['pub_count'][index]))]), 
                            dbc.Col([html.Img(src=faculty_df['PhotoURL'][index], style= {"height": "200px", "width": "150px"})]), 
                            dbc.Col([
                                    html.Div("Position: " + str(faculty_df['Position'][index])), 
                                    html.Div("Email: " + str(faculty_df['Email'][index])), 
                                    html.Div("Phone: " + str(faculty_df['Phone'][index])),
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


third_card = dbc.Card(dbc.CardBody(
    [
        dmc.Title('Fix Missing Faculty Fields'),
        html.Br(),

        dcc.Input(id='faculty-name-search', type='search', placeholder='Search Faculty Name...', debounce=True),
        html.Br(),
        html.Hr(),
        dbc.Row([dbc.Col(children = html.Div("Faculty Search Results: "))]),
        html.Br(),
        dash_table.DataTable(id='table', data= default_missing_fac_fields, columns= default_missing_columns),
        html.Br(),
        dcc.Input(id='data_update', type='text', placeholder='Input Data Fix...', debounce=True),
        html.Br(),
        html.Hr(),
        dbc.Alert(id='tbl_out')
                 
    ])
)

app.layout = dbc.Row(
    [
        dbc.Col(first_card),
        dbc.Col(second_card),
        dbc.Col(third_card)
    ]
)

# Widget 1
@app.callback(
    Output('display_uni', 'children'),
    [Input('uni-search', 'value')],
    prevent_initial_call = True
)
def display_search(value):
    if mysql_utils.make_query(value).empty:
        return 'no results found for '+ f'{value.lower()}'
    else:   
        return f'{value.lower()}'

@app.callback(
    Output('pie', 'figure'),
    [Input('uni-search', 'value')],
    prevent_initial_call = True
)
def update_output(value):
    res = mysql_utils.make_query(value)

    if not res.empty:
        return px.pie(res, values=res['Keyword Relevance'], names=res['Keyword'], hole=0.25)
    else:
        return px.pie(res, values = pd.Series(dtype='object'), names = pd.Series(dtype='object'), hole=0.25)


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
    return create_faculty_cards(neo4j_utils.neo4j_faculty_keywords(value))

# Widget 3
@app.callback(
    [Output('table', 'data'),
     Output('table', 'columns')],
    [Input('faculty-name-search', 'value')],
    prevent_initial_call = True
)
def update_output(value):
    results = neo4j_utils.neo4j_find_faculty(value)
    res_dict = results[['fac_id', 'Name', 'Institution', 'Position', 'Email', 'Phone', 'PhotoURL']].to_dict('records')
    columns = [{"id": i, "name": i} for i in display_columns]
    return [res_dict, columns]

@app.callback(
    Output('tbl_out', 'children'),
     Input('data_update', 'value'),
     State('table', 'active_cell'),
     State('table', 'data'),
    prevent_initial_call = True
)
def update_graphs(value, active_cell, data):
    column_name_dict = {
        "Name": "name",
        "Institution": "institution",
        "Position": "position",
        "Email": "email",
        "Phone": "phone",
        "PhotoURL": "photoUrl"
    }
    database_df = pd.DataFrame(data)

    if value == None or value == "":
        raise PreventUpdate
    else:
        neo4j_utils.update_faculty_field(database_df.at[active_cell['row'], 'fac_id'], column_name_dict[active_cell['column_id']], value)
        return "***Updated " + str(column_name_dict[active_cell['column_id']]) + " with " + str(value) +  "***"

# Run the App
if __name__ == '__main__':
    app.run(debug=True)
