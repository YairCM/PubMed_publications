from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go 


# Functions
def sturges_rule(data):
    n = len(data)
    bins = int(np.ceil(1 + 3.322 * np.log10(n)))
    return bins


# Data - PubMed
file = pd.read_csv("Publications.csv")
pubmed_df = pd.DataFrame(file)
pubmed_df = pubmed_df.sort_values('Year', ascending=True)
pubmed_df = pubmed_df.rename(columns={'Count':'Publications by year'})

bins = sturges_rule(pubmed_df["Year"])
pubmed_df['Year Group'] = pd.cut(pubmed_df['Year'], bins=bins, precision=0)
pubmed_df['Cumulative Sum'] = pubmed_df['Publications by year'].cumsum()

publication_options= ['Publications by year', 'Cumulative Sum']
total_publications = pubmed_df['Publications by year'].sum()


# Section - PubMed
PM_plot = html.Div([
    html.Div([
        html.Span(children=[html.B('PubMed')], style={'marginLeft': '10px'}),
        dcc.RadioItems(
            options=[
                {'label': 'By year', 'value':publication_options[0]},
                {'label':'Total',
                'value':publication_options[1]}
            ], 
            value=publication_options[1],
            inline=True,
            labelStyle={'display': 'inline-block', 'marginLeft': '10px', 'marginRight': '10px'},
            id='Pubmed Publications')], style={'display':'flex', 'justify-content': 'space-between'}),
    dcc.Graph(id = 'graph-publications'),
    dcc.RangeSlider(
        pubmed_df['Year'].min(),
        pubmed_df["Year"].max(),
        marks={i: f'{i}' for i in range(pubmed_df['Year'].min(), pubmed_df["Year"].max()+1, bins)},
        value = [pubmed_df['Year'].max()-bins, pubmed_df["Year"].max()],
        id = 'year-slider')
], className="bg-white")



# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.MORPH])

# App layout
app.layout = html.Div([PM_plot])


# PubMed CallBacks
@app.callback(
    Output('graph-publications', 'figure'),
    Input('Pubmed Publications','value'),
    Input('year-slider', 'value')
)

def update_graph(value, year):
    subset = pubmed_df[(pubmed_df.Year >= year[0]) & (pubmed_df.Year <= year[1])]
    pubmed = px.bar(subset, x='Year', y=value,
                     text=value)
    
    pubmed.update_layout(margin=dict(l=0, r=10, t=10, b=10), xaxis_title="", yaxis_title="")

    pubmed.update_traces(hovertemplate = "<b>Year:</b> %{x}<br><b>Publications:</b> %{y}")

    return pubmed


if __name__ == "__main__":
    app.run(debug=True)
