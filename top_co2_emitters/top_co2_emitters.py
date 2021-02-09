import os

import dash_core_components as dcc
import dash_html_components as html
import lib.html_helper as ht
import numpy as np
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

app_dir = os.path.basename(os.path.dirname(__file__))

csv_file = app_dir + '/co2_emissions.csv'
df_co2 = pd.read_csv(csv_file, index_col=0)

top = 10
top_2019_emissions = df_co2[(df_co2.Year == 2019)].groupby('Name')[
    'Name', 'Emissions'].sum().sort_values('Emissions', ascending=False).head(top)
df_top_2019_emissions = df_co2[df_co2.Name.isin(list(top_2019_emissions.index))].groupby(
    ['Name', 'Year'])['Emissions', 'Excess'].sum().reset_index()

top_2019_excess = df_co2[(df_co2.Year == 2019)].groupby('Name')[
    'Name', 'Excess'].sum().sort_values('Excess', ascending=False).head(top)
df_top_2019_excess = df_co2[df_co2.Name.isin(list(top_2019_excess.index))].groupby(
    ['Name', 'Year'])['Emissions', 'Excess'].sum().reset_index()

df_top_by_kommun = df_co2.groupby(['Län', 'Year'])[
    'Emissions', 'Excess'].sum().reset_index()


def fig_line(df, y, category):
    return px.line(df, x=df.Year, y=df[y], color=category,
                   hover_name=category, hover_data=df.columns)


def fig_top(measure):
    if measure == 'Emissions':
        title = 'Top emitters of 2019'
        df = df_top_2019_emissions
        category = 'Name'
    if measure == 'Excess':
        df = df_top_2019_excess
        category = 'Name'
    if measure == 'Region':
        title = 'Top regions'
        df = df_top_by_kommun
        category = 'Län'

    fig1 = fig_line(df, 'Emissions', category)
    fig2 = fig_line(df, 'Excess', category)

    # dcc.Graph(id='fig_' + measure + y, figure=fig)
    return html.Div([dcc.Graph(figure=fig1), dcc.Graph(figure=fig2)])


layout = ht.layout(app_dir,
                   'Top co2 emitters',
                   [fig_top('Emissions'),
                    fig_top('Region')])
