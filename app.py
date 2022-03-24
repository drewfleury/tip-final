"""
TO DO:
1. impliment authentication/passowrds (with cookies if possible)
2. fix deployment in App ENgine
3. Drill down KPI's and make more charts
4. IF TIME add something to do with NLP

THEMES: https://bootswatch.com/
styling cheat sheet: https://dashcheatsheet.pythonanywhere.com/
"""

# CHANGE SCALE OF Y AXIS TO LOG SCALE

from pandas import value_counts
from bq_api import *
from dash import Dash, dcc, html, Input, Output, dash_table
import dash_auth
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px

# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'username': 'password',
    'Admin' : 'firefly'
}

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server=app.server
# BASIC AUTHENTICATION USING DASH IN-BUILT TOOL
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = html.Div([
    html.Div([
        dbc.Row([
            dbc.Col(html.Img(className="image", width="25%", src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn.freebiesupply.com%2Flogos%2Flarge%2F2x%2Fiberia-airlines-1-logo-png-transparent.png&f=1&nofb=1", alt="Iberia"))
        ], justify="center")
    ]),
    html.H1("Term Integration Project: KPIs", style={'textAlign': 'center'}),
    html.Div([
        dbc.Row([
            dbc.Col(html.P("Select between raised, closed, and backloged:", style={'textAlign': 'center'}
            ), md=4)
        ], justify="center", align="end"),
        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id="priority_drop",
                options= [
                    {"value": "Raised", "label": "Raised"},
                    {"value": "Closed", "label": "Closed"},
                    {"value": "Backlog", "label": "Backlog"}
                ]
            ), md=4),
        ], justify="center"),
    ], ),
    html.Div([
        dbc.Row([
            dbc.Col(dcc.Graph(
                id="scatter_chart_raised",
                figure = {
                    'data' : [
                        go.Bar( #this allows there to be a graph from a set dataframe
                            x = df_priority_raised.priority,
                            y = df_priority_raised.Count,
                        )
                    ],
                    'layout' : {
                        'title' : "Number of issues raised per priority level",
                        'type' : 'log',
                        'plot_bgcolor' : 'rgba(0, 0, 0, 0)'
                    }
                }
            ), md=6),
            dbc.Col(dcc.Graph( # for average resolution time divided into priority
                id="avg_reso_time_raised",
                figure = {
                    'data' : [
                        go.Bar( #this allows there to be a graph from a set dataframe
                            x = Average_res_time_raised.Priority,
                            y = Average_res_time_raised.AVE_Resolution_time_hours
                        )
                    ],
                    'layout' : {
                        'title' : "Average resolution time by priority level"
                    }
                }
            ), md=6)
        ]),
    ]), # , style={'display': 'flex', 'flex-direction': 'row'}
        
    html.Div([
        html.P('Top causes of reported issues', style={'textAlign': 'center'}),
        dbc.Row([
            dbc.Col(dcc.Graph(id="cause_pie"), md=8)
        ], justify="center")
    ]),
    
    html.Div([
        dbc.Row([
            dbc.Col(html.Strong("Made in Madrid by Drew"), style={'textAlign': 'center'})
        ])
    ])
    #dash_table.DataTable(issue_cause_raised.to_dict('records'),[{"name": i, "id": i} for i in issue_cause_raised.columns], id='tbl'),
], style={'backgroundImage': 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwallup.net%2Fwp-content%2Fuploads%2F2018%2F09%2F27%2F15991-abstract-minimalistic-white.jpg&f=1&nofb=1'})

scatter_chart_raised_layout = {
                'title' : "Number of issues raised per priority level",
                'type' : 'log',
                'plot_bgcolor' : 'rgba(0, 0, 0, 0)',
                'paper_bgcolor' : 'rgba(0, 0, 0, 0)'
            }
avg_reso_time_raised_layout = {
                'title' : "Average resolution time by priority level",
                'plot_bgcolor' : 'rgba(0, 0, 0, 0)',
                'paper_bgcolor' : 'rgba(0, 0, 0, 0)'
            }

# callback for number of issues raised per priority
@app.callback(
    Output(component_id="scatter_chart_raised", component_property="figure"),
    Input(component_id="priority_drop", component_property="value")
)
def update_data_num_issues_raised(value):
    if value == 'Raised':
        figure = {
            'data' : [
                go.Bar( #this allows there to be a graph from a set dataframe
                    x = df_priority_raised.priority,
                    y = df_priority_raised.Count
                )
            ],
            'layout' : scatter_chart_raised_layout
        }
        #figure.update_yaxes(type="log")

        #return figure
    elif value == 'Closed':
        figure = {
            'data' : [
                go.Bar( #this allows there to be a graph from a set dataframe
                    x = df_priority_closed.priority,
                    y = df_priority_closed.Count
                )
            ],
            'layout' : scatter_chart_raised_layout
        }
        #figure.update_yaxes(type="log")
    else:
        figure = {
            'data' : [
                go.Bar( #this allows there to be a graph from a set dataframe
                    x = df_priority_backlog.priority,
                    y = df_priority_backlog.Count
                )
            ],
            'layout' : scatter_chart_raised_layout
        }
        #figure.update_yaxes(type="log")
    return figure

# callback for average resolution time graph
@app.callback(
    Output(component_id="avg_reso_time_raised", component_property="figure"),
    Input(component_id="priority_drop", component_property="value")
)
def update_data(value):
    if value == 'Raised':
        figure = {
            'data' : [
                go.Bar( #this allows there to be a graph from a set dataframe
                    x = Average_res_time_raised.Priority,
                    y = Average_res_time_raised.AVE_Resolution_time_hours
                )
            ],
            'layout' : avg_reso_time_raised_layout
        }
        return figure
    elif value == 'Closed':
        figure = {
            'data' : [
                go.Bar( #this allows there to be a graph from a set dataframe
                    x = Average_res_time_closed.Priority,
                    y = Average_res_time_closed.AVE_Resolution_time_hours
                )
            ],
            'layout' : avg_reso_time_raised_layout
        }
    else:
        figure = {
            'data' : [
                go.Bar( #this allows there to be a graph from a set dataframe
                    x = Average_res_time_backlog.Priority,
                    y = Average_res_time_backlog.AVE_Resolution_time_hours
                )
            ],
            'layout' : avg_reso_time_raised_layout
        }
    return figure
#_______
#CALLBACK FOR PIC CHART
@app.callback(
    Output(component_id="cause_pie", component_property="figure"),
    Input(component_id="priority_drop", component_property="value")
)
def update_pie(value):
    if value == "Raised":
        piechart = px.pie(
            issue_cause_raised,
            values = issue_cause_raised["Incident_Count"],
            names = issue_cause_raised["Inc__Type"]
        )
        piechart.update_traces(textposition='inside', textinfo='percent+label')
        piechart.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
    elif value == "Closed":
        piechart = px.pie(
            issue_cause_closed,
            values = issue_cause_closed["Incident_Count"],
            names = issue_cause_closed["Inc__Type"]
        )
        piechart.update_traces(textposition='inside', textinfo='percent+label')
        piechart.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
    else:
        piechart = px.pie(
            issue_cause_backlog,
            values = issue_cause_backlog["Incident_Count"],
            names = issue_cause_backlog["Inc__Type"]
        )
        piechart.update_traces(textposition='inside', textinfo='percent+label')
        piechart.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
    return piechart

def text_search(input):
    pass #return query_to_df(SELECT)


"""@app.callback(
    Output(component_id="id-changes", component_property="children"),
    Input(component_id="dropdown", component_property="value")
)
def update_bar_chart(value):
    if value == "one":
       return df_priority_raised.iloc[0,1]
    elif value == "two":
        return df_priority_raised.iloc[1,1]
    else:
        return "no value selected yet" """

if __name__ == "__main__":
    app.run_server(debug=True)