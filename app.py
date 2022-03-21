"""
TO DO:
1. impliment authentication/passowrds (with cookies if possible)
2. fix deployment in App ENgine
3. Drill down KPI's and make more charts
4. IF TIME add something to do with NLP

THEMES: https://bootswatch.com/
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
    'username': 'password'
}

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server=app.server
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)


app.layout = html.Div([
    html.H1("Term Integration Project: KPIs", style={'textAlign': 'center'}),
    html.H3("Select between raised, closed, and backloged"),
    dcc.Dropdown(
        id="priority_drop",
        options= [
            {"value": "Raised", "label": "Raised"},
            {"value": "Closed", "label": "Closed"},
            {"value": "Backlog", "label": "Backlog"}
        ]
    ),
    html.Div([
        dcc.Graph(
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
                'type' : 'log'
            }
        }
        ),
        dcc.Graph( # for average resolution time divided into priority
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
        ),
    ]), # , style={'display': 'flex', 'flex-direction': 'row'}
    
    dcc.Dropdown(
        id="dropdown",
        options= [
            {"value": "one", "label": "one"},
            {"value": "two", "label": "two"}
        ]
    ),
    html.H2(id="id-changes"),
    dash_table.DataTable(issue_cause_raised.to_dict('records'),[{"name": i, "id": i} for i in issue_cause_raised.columns], id='tbl'),
])

scatter_chart_raised_layout = {
                'title' : "Number of issues raised per priority level"
            }
avg_reso_time_raised_layout = {
                'title' : "Average resolution time by priority level"
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
        return figure
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

@app.callback(
    Output(component_id="id-changes", component_property="children"),
    Input(component_id="dropdown", component_property="value")
)
def update_bar_chart(value):
    if value == "one":
       return df_priority_raised.iloc[0,1]
    elif value == "two":
        return df_priority_raised.iloc[1,1]
    else:
        return "no value selected yet"


#app.run_server(debug=True)
if __name__ == "__main__":
    app.run_server(debug=True)