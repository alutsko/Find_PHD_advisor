# Import packages
from dash import Dash, html, dash_table, dcc, ctx, Output, Input, State
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import mysql_utils
import neo4j_utils
import mongodb_utils

# Setting up default dashboard display
default_uni = '12'
default_df = mysql_utils.mysql_keyword_relevance(default_uni)

default_keyword = "machine learning"
default_neo4j = neo4j_utils.neo4j_faculty_keywords(default_keyword)

default_missing_fac_fields = default_neo4j[['fac_id', 'Name', 'Institution', 'Position', 'Email', 'Phone', 'PhotoURL']].to_dict('records')
display_columns = ['Name', 'Institution', 'Position', 'Email', 'Phone', 'PhotoURL']
default_missing_columns = [{"id": i, "name": i} for i in display_columns]

mongodb = mongodb_utils.create_mongo_connection()

# dropdown options for keyword and university
keyword_options = mysql_utils.fetch_dropdown_options('keyword', 'name', 'id')
neo4j_keyword_options = neo4j_utils.fetch_dropdown_options('keyword', 'keyword', 'name')
university_options = mysql_utils.fetch_dropdown_options('university', 'name', 'id')

# Initialize the app - incorporate a Dash Mantine theme
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
first_card = dbc.Card(dbc.CardBody(
    [
        dmc.Title('Find University Top Keywords', order=3),
        html.Br(),
        html.Label("Search for an institution:"),
        dcc.Dropdown(
            id='find_uni_kw_dropdown',
            options=university_options,
            placeholder="Start typing to search",
            value=None,
            searchable=True,
        ),
        html.Br(),
        html.Button('Submit', id='submit_uni_search', n_clicks=0),
        html.Hr(),
        dbc.Row([dbc.Col(children = [html.Div("Displaying top results for: ")]), dbc.Col(children = [html.Div(id="display_uni", children=[mysql_utils.mysql_get_uni_from_id(default_uni)])])]),
        
        dcc.Graph(id = 'pie', figure = px.pie(default_df, values='Keyword Relevance', names='Keyword', hole=0.25))
                
    ]),
    style={"height": "50%", "margin": "auto"}
)

def create_faculty_cards(faculty_df):
    card_list = []
    for index in faculty_df.index:
        card = dbc.Card(
                dbc.CardBody(
                    dbc.Col([dbc.Row([
                        # TODO: replace rank, name, institution, etc strings with dmc text and ad css bold style
                            dbc.Col([html.Div(className="app-div", children = [dmc.Text(className = 'bold-text', children = "Rank:"), dmc.Text(className = 'normal-text', children='#'+str(index+1))]),
                                     html.Div(className="app-div", children = [dmc.Text(className = 'bold-text', children = "Name: "), dmc.Text(className = 'normal-text', children=str(faculty_df['Name'][index]))]),
                                     html.Div(className="app-div", children = [dmc.Text(className = 'bold-text', children = "Institution: "), dmc.Text(className = 'normal-text', children=str(faculty_df['Institution'][index]))]),
                                     html.Div(className="app-div", children = [dmc.Text(className = 'bold-text', children = "Number papers with keyword: "), dmc.Text(className = 'normal-text', children=str(faculty_df['pub_count'][index]))]),
                                     ]), 
                            dbc.Col([html.Img(className= 'faculty-pic', src=faculty_df['PhotoURL'][index]), html.Img(className= 'uni-logo', src=faculty_df['uni.photoUrl'][index])]), 
                            dbc.Col([html.Div(className="app-div", children = [dmc.Text(className = 'bold-text', children = "Position: "), dmc.Text(className = 'normal-text', children=str(faculty_df['Position'][index]))]),
                                     html.Div(className="app-div", children = [dmc.Text(className = 'bold-text', children = "Email: "), dmc.Text(className = 'normal-text', children=str(faculty_df['Email'][index]))]),
                                     html.Div(className="app-div", children = [dmc.Text(className = 'bold-text', children = "Phone: "), dmc.Text(className = 'normal-text', children=str(faculty_df['Phone'][index]))])
                                    ]),
                            # dbc.Col([html.Img(className= 'uni-logo', src=faculty_df['uni.photoUrl'][index])])
                            ],
                            )],
                            ),
                ),
        )
        card_list.append(card)
    return card_list


second_card = dbc.Card(dbc.CardBody(
    [
        dmc.Title('Find Faculty Best Keywords', order=3),
        html.Br(),
        html.Label("Select for a keyword:"),
        dcc.Dropdown(
            id='find_kw_fac_dropdown',
            options=neo4j_keyword_options,
            placeholder="Start typing to search",
            value=None,
            searchable=True,
        ),
        html.Br(),
        html.Button('Submit', id='submit_kw_search', n_clicks=0),
        html.Hr(),
        dbc.Row([dbc.Col(children = [html.Div("Displaying top faculty for: ")]), dbc.Col(children = [html.Div(id="display_keyword", children=[default_keyword])])]),
        html.Br(),
        dbc.Col(id = 'faculty_col', children = create_faculty_cards(default_neo4j))
                 
    ]),
)


third_card = dbc.Card(dbc.CardBody(
    [
        dmc.Title('Fix Missing Faculty Fields', order=3),
        html.Br(),
        html.Div(className = 'input-button-parent',
                 children = [html.Div(className = 'input-button-child', children = dcc.Input(id='faculty_name_search', type='search', placeholder='Search Faculty Name...', debounce=True)), 
                           html.Div(className = 'input-button-child', children =html.Button('Search', id='submit_facname_search', n_clicks=0))]),
        html.Hr(),
        dbc.Row([dbc.Col(children = html.Div("Faculty Search Results: "))]),
        html.Br(),
        dash_table.DataTable(  
            id='table', data= default_missing_fac_fields, columns= default_missing_columns,
            style_table={'overflowX': 'auto'}),
        html.Br(),
        dcc.Input(id='data_update', type='text', placeholder='Input Data Fix...', debounce=True),
        html.Br(),
        html.Br(),
        html.Button('Submit', id='submit_facfix', n_clicks=0),
        html.Br(),
        html.Hr(),
        dbc.Alert(id='tbl_out')
                 
    ])
)

fourth_card = dbc.Card(
   dbc.CardBody([
      dmc.Title('Add a new entry', order=3),
      html.Br(),
      html.Label("I want to add a:"),
      dcc.Dropdown(
         id= 'update-dropdown', 
         options = [
            {'label': 'new faculty', 'value': 'faculty'},
            {'label': 'new publication', 'value': 'publication'}
         ],
         placeholder='Select an option',
      ),
      html.Hr(),
      dmc.Text("Please fill in the information completely in order to update the database"),
      html.Div(id='input-fields-container'),
      html.Br(),
      html.Button('Submit', id='submit-fac-pub', n_clicks=0),
      html.Br(),
      html.Br(),
      dbc.Toast(
         [html.P("Thanks for updating our database!", className="mb-3")],
         id='notification-toast',
         header='New entry successfully added',
         icon='success',
         color='success',
         is_open=False,
         dismissable=True,
         duration=3000,
      ),
   ]),
   style={"height": "75%", "margin": "auto"}
)

# 5th widget



fifth_card = dbc.Card(
    dbc.CardBody([
        dmc.Title("Find publications in your research area from the university you're interested in", order=3),
        html.Br(),
        html.Label("Select your research interest:"),
        dcc.Dropdown(
            id='keyword-dropdown',
            options=keyword_options,
            placeholder="Start typing to search",
            value=None,
            searchable=True,
            ),
        html.Label("Select the university:"),
        dcc.Dropdown(
            id='university-dropdown',
            options=university_options,
            placeholder="Start typing to search",
            value=None,
            searchable=True,
        ),
        html.Br(),
        html.Button('Submit', id='submit-research-uni-button'),
        html.Hr(),
        html.Br(),
        dcc.Store(id='data-store', storage_type='memory'),
        html.Div(id='publication-results'),
   ]),
   style={"height": "50%", "margin": "auto"}
)

sixth_card = dbc.Card(
    dbc.CardBody([
        dmc.Title("Trending keywords by institution", order=3),
        html.Br(),
        html.Label("Select your research interest:"),
        dcc.Dropdown(
            id='trending-keyword-dropdown',
            options=mysql_utils.fetch_dropdown_options('keyword', 'name', 'id'),
            placeholder="Start typing to search",
            value=None,
            searchable=True,
            ),
        html.Br(),
        html.Button('Submit', id='submit-keyword-button'),
        html.Hr(),
        dcc.Graph(id='bar-graph',
            style={'height': '400px', 'width': '100%'}),
    ]),
   style={"height": "50%", "margin": "auto"}
)


app.layout = dbc.Container(
    [
        dbc.Row([dbc.Col([first_card, fourth_card]), dbc.Col([fifth_card, sixth_card]), dbc.Col(second_card)]),
        dbc.Col(third_card)
    ],
    
    fluid = True
)

# Widget 1
@app.callback(
    Output('display_uni', 'children'),
    Input('submit_uni_search', 'n_clicks'),
    State('find_uni_kw_dropdown', 'value'),
    prevent_initial_call = True
)
def display_institution_search(n_clicks, value):
    if n_clicks > 0:
        if value == "":
            raise PreventUpdate
        elif mysql_utils.mysql_keyword_relevance(value).empty:
            return 'no results found'
        else:   
            return mysql_utils.mysql_get_uni_from_id(value)

@app.callback(
    Output('pie', 'figure'),
    Input('submit_uni_search', 'n_clicks'),
    [State('find_uni_kw_dropdown', 'value')],
    prevent_initial_call = True
)
def update_relevance_piechart(n_clicks, value):
    if n_clicks > 0:
        res = mysql_utils.mysql_keyword_relevance(value)
        if value == "":
            raise PreventUpdate
        elif not res.empty:
            return px.pie(res, values='Keyword Relevance', names='Keyword', hole=0.25)
        else:
            return px.pie(res, values = pd.Series(dtype='object'), names = pd.Series(dtype='object'), hole=0.25)


# Widget 2
@app.callback(
    Output('display_keyword', 'children'),
    Input('submit_kw_search', 'n_clicks'),
    [State('find_kw_fac_dropdown', 'value')],
    prevent_initial_call = True
)
def display_keyword_search(n_clicks, value):
    if n_clicks > 0:
        if value == "":
            raise PreventUpdate
        elif neo4j_utils.neo4j_faculty_keywords(value).empty:
            return 'no results found'
        else:
            return f'{value.lower()}'

@app.callback(
    Output('faculty_col', 'children'),
    Input('submit_kw_search', 'n_clicks'),
    [State('find_kw_fac_dropdown', 'value')],
    prevent_initial_call = True
)
def update_faculty_output(n_clicks, value):
    if n_clicks > 0:
        return create_faculty_cards(neo4j_utils.neo4j_faculty_keywords(value))

# Widget 3
@app.callback(
    Output('table', 'data'),
    Output('table', 'columns'),
    Output('tbl_out', 'children'),

    Input('submit_facname_search', 'n_clicks'),
    Input('submit_facfix', 'n_clicks'),

    State('faculty_name_search', 'value'),
    State('data_update', 'value'),
    State('table', 'active_cell'),
    State('table', 'data'),
    

    prevent_initial_call = True
)
def update_faculty_table(search_fac, submit_fac, fac_name_value, update_fix, active_cell, table_data):
    triggered_id = ctx.triggered_id

    if triggered_id == 'submit_facname_search':
        return update_faculty_table(search_fac, fac_name_value)
    elif triggered_id == 'submit_facfix':
        return update_fac_field(submit_fac, update_fix, active_cell, fac_name_value, table_data)
   

def update_faculty_table(n_clicks, value):
    if n_clicks > 0:
        results = neo4j_utils.neo4j_find_faculty(value)
    
        if value == "" or results.empty:
            raise PreventUpdate
        else:
            res_dict = results[['fac_id', 'Name', 'Institution', 'Position', 'Email', 'Phone', 'PhotoURL']].to_dict('records')
            columns = [{"id": i, "name": i} for i in display_columns]
            return [res_dict, columns, '']


def update_fac_field(n_clicks, value, active_cell, fac_name_value, data):
    column_name_dict = {
        "Name": "name",
        "Institution": "institution",
        "Position": "position",
        "Email": "email",
        "Phone": "phone",
        "PhotoURL": "photoUrl"
    }
    database_df = pd.DataFrame(data)

    if n_clicks > 0:
        if value == None or value == "" or active_cell['column_id'] == 'Name':
            raise PreventUpdate
        elif column_name_dict[active_cell['column_id']] != 'name':
            neo4j_utils.neo4j_update_faculty_field(database_df.at[active_cell['row'], 'fac_id'], column_name_dict[active_cell['column_id']], value)
            results = neo4j_utils.neo4j_find_faculty(fac_name_value)
            res_dict = results[['fac_id', 'Name', 'Institution', 'Position', 'Email', 'Phone', 'PhotoURL']].to_dict('records')
            columns = [{"id": i, "name": i} for i in display_columns]
            update_message = "***Updated " + str(column_name_dict[active_cell['column_id']]) + " with " + str(value) +  "***"

            return [res_dict, columns, update_message]
       
# Widget 4
# callback to generate input fields based on selection from dropdown
@app.callback(
   Output('input-fields-container', 'children'),
   [Input('update-dropdown', 'value')],
   prevent_initial_call = True

)
def generate_input_fields(option):
   if option == 'faculty':
      return html.Div(
         [
            html.Label("faculty name: ", style={'margin-right': '10px'}),
            dcc.Input(id='name-input', value='', type='text', className='mb-2'),
            html.Br(),
            html.Label("position: ", style={'margin-right': '10px'}),
            dcc.Input(id='position-input', value='', type='text', className='mb-2'),
            html.Br(),
            html.Label("research interest: ", style={'margin-right': '10px'}),
            dcc.Input(id='researchInterest-input', value='', type='text', className='mb-2'),
            html.Br(),
            html.Label("email: ", style={'margin-right': '10px'}),
            dcc.Input(id='email-input', value='', type='email', className='mb-2'),
            html.Br(),
            html.Label("phone: ", style={'margin-right': '10px'}),
            dcc.Input(id='phone-input', value='', type='tel', className='mb-2'),
            html.Br(),
            html.Label("university name: ", style={'margin-right': '10px'}),
            dcc.Input(id='affiliation.id-input', value='', type='text', className='mb-2'),
            html.Br(),
            html.Label("university photo url: ", style={'margin-right': '10px'}),
            dcc.Input(id='affiliation.photoUrl-input', value='', type='text', className='mb-2'),
            html.Br(),
            html.Label("faculty photo url: ", style={'margin-right': '10px'}),
            dcc.Input(id='photoUrl-input', value='', type='text', className='mb-2'),
            html.Br(),
            html.Label("keywords: ", style={'margin-right': '10px'}),
            dcc.Input(id='faculty.keywords.name-input', value='', type='text', className='mb-2'),
            html.Br(),
            html.Label("publication id numbers: ", style={'margin-right': '10px'}),
            dcc.Input(id='publications-input', value='', type='number'),
         ]
      )
   elif option == 'publication':
      return html.Div(
         [
            html.Label("publication id number: ", style={'margin-right': '10px'}),
            dcc.Input(id='id-input', value='', type='number', className='mb-2'),
            html.Br(),
            html.Label("title: ", style={'margin-right': '10px'}),
            dcc.Input(id='title-input', value='', type='text', className='mb-2'),
            html.Br(),
            html.Label("journal or venue: ", style={'margin-right': '10px'}),
            dcc.Input(id='venue-input', value='', type='text', className='mb-2'),
            html.Br(),
            html.Label("year of publication: ", style={'margin-right': '10px'}),
            dcc.Input(id='year-input', value='', type='number', className='mb-2'),
            html.Br(),
            html.Label("number of times publication has been cited by other articles: ", style={'margin-right': '10px'}),
            dcc.Input(id='numCitations-input', value='', type='number', className='mb-2'),
            html.Br(),
            html.Label("keywords: ", style={'margin-right': '10px'}),
            dcc.Input(id='publications.keywords.name-input', value='', type='text'),
         ]
      )
   else:
      return html.Div()

# callback to grab inputs and send to db
@app.callback(
   Output('notification-toast', 'is_open'),
   Input('submit-fac-pub', 'n_clicks'),
   [State('update-dropdown', 'value'),
    State('input-fields-container', 'children')],
    prevent_initial_call = True
)
def capture_and_update(n_clicks, option, input_fields):
   if n_clicks is not None and option is not None and input_fields is not None:
      data = {}
      temp_dict = input_fields['props']['children']
      for input_field in temp_dict:
         if 'id' in input_field['props']:
            input_id = input_field['props']['id']
            if 'value' in input_field['props']:
               input_value = input_field['props']['value']
               data[input_id] = input_value

      collection_name = 'faculty' if option == 'faculty' else 'publications'
      mongodb[collection_name].insert_one(data)

      return True
   else:
      return False
   

# Widget 5
# callback to capture user selections
@app.callback(
    Output('data-store', 'data'),
    Input('submit-research-uni-button', 'n_clicks'),
    State('keyword-dropdown', 'value'),
    State('university-dropdown', 'value'),
    prevent_initial_call = True
)
def capture_user_selections(n_clicks, keyword_id, university_id):
    if n_clicks and keyword_id and university_id:
        return {'keyword_id': keyword_id, 'university_id': university_id}
    else:
        return None


# callback to get data from stored procedure and joins
@app.callback(
    Output('publication-results', 'children'),
    Input('data-store', 'data'),
    prevent_initial_call = True
)
def process_user_selections(data):
    if data:
        # calling stored procedure
        keyword_id = data.get('keyword_id')
        university_id = data.get('university_id')
        res = mysql_utils.GetPublicationsByKeywordAndUniversity(keyword_id, university_id)

        # creating table of results
        if not res.empty:
            table = dash_table.DataTable(
                id= 'datatable',
                data= res.to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_cell={'whiteSpace': 'normal',
                            'overflowWrap': 'break-word',
                            'height': 'auto',
                            'textAlign': 'left',}
            )
            table_card = html.Div(table, style={'width': '100%', 'height': '400px', 'overflowY': 'scroll'})
            return table_card
        else:
            return html.Div([
                html.Br(),
                html.H6("This institution has not been involved in any publications on this research topic"),
            ])
   
# Widget 6
# callback to capture user selections
@app.callback(
    Output('bar-graph', 'figure'),
    Input('submit-keyword-button', 'n_clicks'),
    State('trending-keyword-dropdown', 'value'),
    prevent_initial_call = True
)
def update_bar_graph(n_clicks, keyword_id):
    if n_clicks and keyword_id:    
        res = mysql_utils.GetTopUniversitiesByYear(keyword_id)
        if not res.empty:
            fig = px.bar(res, 
                         x='year', 
                         y='num_pubs', 
                         color='universityName', 
                         text='universityName',
                         hover_data={'universityName': True, 'num_pubs': True, 'year': False},
                         color_discrete_sequence=px.colors.qualitative.Pastel2,
                         )
            
            fig.update_layout(xaxis_title='Year', 
                              yaxis_title='Number of Publications',
                              title='Number of Publications by University', 
                              showlegend=False,
                              uniformtext_minsize=1,
                              uniformtext_mode='hide',
                              bargap=0.1,
                              barmode='stack', 
                              )
            fig.update_traces(hovertemplate='University: %{text}<br>Number of Publications: %{y}<extra></extra>')
            
            return fig
        else:
            return html.Div([
                html.Br(),
                html.H6("This institution has not been involved in any publications on this research topic"),
            ])
        
# Run the App
if __name__ == '__main__':
    app.run(debug=True)
