"""Hi Pepe!"""
from bq_api import *
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
import dash_auth
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from dash.exceptions import PreventUpdate

# FUNCTION TO QUERY DATABASE BASED ON SEARCH
def search(type, input, size, sheet):
    return query_to_df(f"SELECT * FROM tip_dataset_1.{sheet} WHERE {type} LIKE '%{input}%'").head(size)

# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'Admin' : 'firefly'
}

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server=app.server
# BASIC AUTHENTICATION USING DASH IN-BUILT TOOL
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

# APPLICATION LAYOUT
app.layout = html.Div([
    html.Div([
        dbc.Row([
            dbc.Col(html.Img(className="image", width="25%", src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn.freebiesupply.com%2Flogos%2Flarge%2F2x%2Fiberia-airlines-1-logo-png-transparent.png&f=1&nofb=1", alt="Iberia"))
        ], justify="center")
    ]),
    html.Div([
        dbc.Row([html.H1("Incidents Report", style={'textAlign': 'center'}),]),
        dbc.Row([
            dbc.Col(html.P("Select between raised, closed, and backlogged reports:", style={'textAlign': 'center'}
            ), md=4)
        ], justify="center", align="end"),
        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id="priority_drop",
                options= [
                    {"value": "Raised", "label": "Raised"},
                    {"value": "Closed", "label": "Closed"},
                    {"value": "Backlog", "label": "Backlog"}
                ],
                value="Raised"
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
                            marker_color=['#C4393D', '#DFB32A','#C4393D','#DFB32A']
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
    ]),
        
    html.Div([
        dbc.Row([
            dbc.Col(dcc.Graph(id="cause_pie", style={'textAlign': 'center'}), md=6),
            dbc.Col(
                dcc.Graph(
                id="weekly_chart",
                figure = {
                    'data' : [
                        go.Bar( #this allows there to be a graph from a set dataframe
                            x = weekly_incidents_riaised.Week,
                            y = weekly_incidents_riaised.Incident_Count,
                        )
                    ],
                    'layout' : {
                        'title' : "Number of issues raised per week in 2021",
                        'type' : 'log',
                        'plot_bgcolor' : 'rgba(0, 0, 0, 0)'
                    }
                }
            )
            , md=6),
    ]),
    html.Div([
        html.Spacer(),
        dbc.Row([
            dbc.Col(html.H2("Advanced filtering", style={'textAlign': 'center'}))
        ], justify="center"),
        dbc.Row([
            dbc.Col(html.P("Choose the column you want to filter by:"), md=4),
            dbc.Col(
                dcc.Dropdown(
                id="column_select_drop",
                options= [
                    {"value": "Incidenct_Code", "label": "Incident_Code"},
                    {"value": "Customer_Company_Group", "label": "Customer_Company_Group"},
                    {"value": "Customer_Company", "label": "Customer_Company"},
                    {"value": "Incident_Status", "label": "Incident_Status"},
                    {"value": "Incident_Description", "label": "Incident_Description"},
                    {"value": "Support_Group", "label": "Support_Group"},
                    {"value": "Tower_Group", "label": "Tower_Group"},
                    {"value": "Domain_Group", "label": "Domain_Group"},
                    {"value": "Priority", "label": "Priority"},
                    {"value": "Urgency", "label": "Urgency"},
                    {"value": "Resolution_Description", "label": "Resolution_Description"},
                    {"value": "Assigned_Organization", "label": "Assigned_Organization"},
                    {"value": "Inc__Category", "label": "Inc__Category"},
                    {"value": "Last_Modified_Date", "label": "Last_Modified_Date"},
                    {"value": "Inc__Type", "label": "Inc__Type"},
                    {"value": "Inc__Element", "label": "Inc__Element"},
                    {"value": "Aging__Days_", "label": "Aging__Days_"},
                    {"value": "Localizaci__n_Cliente", "label": "Localizaci__n_Cliente"},
                    {"value": "Departamento_Cliente", "label": "Departamento_Cliente"}
                ],
                placeholder="Incident_Description"), md=4
            ),
        ], justify="center"),
        dbc.Row([
            dbc.Col(html.P("Choose number of results to show"), md=4),
            dbc.Col(
                dcc.Dropdown(
                id="head_size",
                options= [
                    {"value": 5, "label": "5"},
                    {"value": 10, "label": "10"},
                    {"value": 50, "label": "50"},
                    {"value": '', "label": "all"},
                ],
                value=""),
                md=4
            ),
        ], justify="center"),
        dbc.Row([
            dbc.Col(html.P("enter search query"), md=4),
            dbc.Col(
                dcc.Input(
                    id="input_id",
                    placeholder="insert search here",
                    value=""
                ), md=4
            ),
        ], justify="center"),
        html.Spacer(),
        dbc.Row([
            html.Button(id="submit_button", n_clicks=0, children = 'Submit')
        ], justify="center", align="center"),            
        html.Spacer(),
        dbc.Row([
            dbc.Col(dbc.Spinner(color="#A31523", children = dash_table.DataTable(
                id="df_select",
                style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold'},
                style_table={'overflowX': 'auto'}
            )))
        ])
        ])
    ]),
    

    html.Div([
        dbc.Row([
            dbc.Col(html.Strong("Made in Madrid by Drew"), style={'textAlign': 'center'})
        ])
    ])
], style={'background-color': '#E9E9E9'})

scatter_chart_raised_layout = {
                'title' : "Number of issues raised per priority level",
                'type' : 'log',
                'plot_bgcolor' : 'rgba(0, 0, 0, 0)',
                'paper_bgcolor' : 'rgba(0, 0, 0, 0)',
                'yaxis' : {
                    'title' : 'Number of issues - log',
                    'type' : 'log'
                }
            }
avg_reso_time_raised_layout = {
                'title' : "Average resolution time by priority level",
                'plot_bgcolor' : 'rgba(0, 0, 0, 0)',
                'paper_bgcolor' : 'rgba(0, 0, 0, 0)',
                'yaxis' : {
                    'title' : 'Time in hours'
                }
            }

weekly_layout = {
                'title' : "Number of issues raised per week in 2021",
                'plot_bgcolor' : 'rgba(0, 0, 0, 0)',
                'paper_bgcolor' : 'rgba(0, 0, 0, 0)',
                'yaxis' : {
                    'title' : 'Number of issues'
                }
            }

# CALLBACK FOR SEARCH COLUMN INPUT
@app.callback(
    Output(component_id="df_select", component_property="data"),
    [Input(component_id="submit_button", component_property="n_clicks"),
    Input(component_id="priority_drop", component_property="value")],
    [State(component_id="column_select_drop", component_property="value"),
    State(component_id="input_id", component_property="value"),
    State(component_id="head_size", component_property="value")]
    
)
def update_column(n_clicks, priority_drop, column_select_drop, input_id, head_size):
    if input_id == "":
        raise PreventUpdate
    if priority_drop == "Raised":
        sheet = "raised"
    elif priority_drop == "Closed":
        sheet = "closed"
    else:
        sheet = "backlog"
    data=search(column_select_drop, input_id, head_size, sheet).to_dict('records')
    return data

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
                    x = ['Baja', 'Media', 'Alta', 'Crítica'],
                    y = df_priority_raised.Count,
                    marker_color=['#C4393D','#DFB32A','#C4393D','#DFB32A']
                )
            ],
            'layout' : scatter_chart_raised_layout
        }
    elif value == 'Closed':
        figure = {
            'data' : [
                go.Bar( #this allows there to be a graph from a set dataframe
                    x = ['Baja', 'Media', 'Alta', 'Crítica'],
                    y = df_priority_closed.Count,
                    marker_color=['#C4393D', '#DFB32A','#C4393D','#DFB32A']
                )
            ],
            'layout' : scatter_chart_raised_layout
        }
    else:
        figure = {
            'data' : [
                go.Bar( #this allows there to be a graph from a set dataframe
                    x = ['Baja', 'Media', 'Alta', 'Crítica'],
                    y = df_priority_backlog.Count,
                    marker_color=['#C4393D', '#DFB32A','#C4393D','#DFB32A']
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
                    x = ['Baja', 'Media', 'Alta', 'Crítica'],
                    y = Average_res_time_raised.AVE_Resolution_time_hours,
                    marker_color=['#C4393D', '#DFB32A','#C4393D','#DFB32A']
                )
            ],
            'layout' : avg_reso_time_raised_layout
        }
        return figure
    elif value == 'Closed':
        figure = {
            'data' : [
                go.Bar( #this allows there to be a graph from a set dataframe
                    x = ['Baja', 'Media', 'Alta', 'Crítica'],
                    y = Average_res_time_closed.AVE_Resolution_time_hours,
                    marker_color=['#C4393D', '#DFB32A','#C4393D','#DFB32A']
                )
            ],
            'layout' : avg_reso_time_raised_layout
        }
    else:
        figure = {
            'data' : [
                go.Bar( #this allows there to be a graph from a set dataframe
                    x = ['Baja', 'Media', 'Alta', 'Crítica'],
                    y = Average_res_time_backlog.AVE_Resolution_time_hours,
                    marker_color=['#C4393D', '#DFB32A','#C4393D','#DFB32A']
                )
            ],
            'layout' : avg_reso_time_raised_layout
        }
    return figure
#_______
#CALLBACK FOR WEEKLY INCIDENTS
@app.callback(
    Output(component_id="weekly_chart", component_property="figure"),
    Input(component_id="priority_drop", component_property="value")
)
def update_data(value):
    if value == 'Raised':
        figure = {
            'data' : [
                go.Bar( #this allows there to be a graph from a set dataframe
                    x = weekly_incidents_riaised.Week,
                    y = weekly_incidents_riaised.Incident_Count,
                    marker_color=['#C4393D']*20
                )
            ],
            'layout' : weekly_layout
        }
        return figure
    elif value == 'Closed':
        figure = {
            'data' : [
                go.Bar( #this allows there to be a graph from a set dataframe
                    x = weekly_incidents_closed.Week,
                    y = weekly_incidents_closed.Incident_Count,
                    marker_color=['#C4393D']*20
                )
            ],
            'layout' : weekly_layout
        }
    else:
        figure = {
            'data' : [
                go.Bar( #this allows there to be a graph from a set dataframe
                    x = weekly_incidents_backlog.Week,
                    y = weekly_incidents_backlog.Incident_Count,
                    marker_color=['#C4393D']*20
                )
            ],
            'layout' : weekly_layout
        }
    return figure


#CALLBACK FOR PIE CHART
@app.callback(
    Output(component_id="cause_pie", component_property="figure"),
    Input(component_id="priority_drop", component_property="value")
)
def update_pie(value):
    if value == "Raised":
        piechart = px.pie(
            issue_cause_raised,
            values = issue_cause_raised["Incident_Count"],
            names = issue_cause_raised["Inc__Type"],
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        piechart.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)
        piechart.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)', title="Top causes of reported incidents")
    elif value == "Closed":
        piechart = px.pie(
            issue_cause_closed,
            values = issue_cause_closed["Incident_Count"],
            names = issue_cause_closed["Inc__Type"],
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        piechart.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)
        piechart.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)', title="Top causes of reported incidents")
    else:
        piechart = px.pie(
            issue_cause_backlog,
            values = issue_cause_backlog["Incident_Count"],
            names = issue_cause_backlog["Inc__Type"],
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        piechart.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)
        piechart.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)', title="Top causes of reported incidents")
    return piechart

if __name__ == "__main__":
    app.run_server(debug=True)