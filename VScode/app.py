from pandas import value_counts
from bq_api import *
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px

app = Dash(__name__)


app.layout = html.Div([
    html.H1("Dash test 1"),
    dcc.Dropdown(
        id="priority_drop",
        options= [
            {"value": "Raised", "label": "Raised"},
            {"value": "Closed", "label": "Closed"},
            {"value": "Backlog", "label": "Backlog"}
        ]
    ),
    dcc.Graph(
        id="scatter_chart_raised",
        figure = {
            'data' : [
                go.Bar( #this allows there to be a graph from a set dataframe
                    x = df_priority_raised.priority,
                    y = df_priority_raised.Count
                )
            ]
        }
    ),
    dcc.Graph(
        id="scatter_chart_closed",
        figure = {
            'data' : [
                go.Bar( #this allows there to be a graph from a set dataframe
                    x = df_priority_closed.priority,
                    y = df_priority_closed.Count
                )
            ]
        }
    ),
    dcc.Dropdown(
        id="dropdown",
        options= [
            {"value": "one", "label": "one"},
            {"value": "two", "label": "two"}
        ]
    ),
    html.H2(id="id-changes")
])
# NEED TO FIGURE OUT WHY THIS CALLBACK IS CAUSING PAGE TO FREEZE
"""@app.callback(
    Output(component_id="scatter_chart", component_property="figure"),
    Input(component_id="priority_drop", component_property="value")
)
def update_data(value):
    if value == 'Raised':
        figure = {
            'data' : [
                go.Bar( #this allows there to be a graph from a set dataframe
                    x = df_priority_raised.priority,
                    y = df_priority_raised.Count
                )
            ]
        }
        return figure """

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


app.run_server(debug=True)

"""
                go.Bar( #this allows there to be a graph from a set dataframe
                    x = df_priority_raised.priority,
                    y = df_priority_raised.Count
                )

                , 
            'layout': go.Layout(
                title = 'This is title',
                hovermode='closest'

            )
            """