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


def top_emissions_by_measure(measure, top=10, year=2019):
    df = df_co2[(df_co2.Year == year)].groupby(measure)[
        measure, 'Emissions'].sum().sort_values('Emissions', ascending=False).head(top)
    df = df_co2[df_co2[measure].isin(list(df.index))].groupby(
        [measure, 'Year']).sum().reset_index()
    return df


def fig_line(df, y, category):
    return px.line(df, x=df.Year, y=df[y], color=category,
                   hover_name=category, hover_data=df.columns)


def fig_emission_excess(measure):
    suffix = '(top emitters of 2019)'
    if measure in ['Name', 'Län', 'Kommun', 'Bransch']:
        title = measure + ' ' + suffix
        df = top_emissions_by_measure(measure)
        category = measure

        fig1 = fig_line(df, 'Emissions', category)
        fig2 = fig_line(df, 'Excess', category)

    # dcc.Graph(id='fig_' + measure + y, figure=fig)
    return html.Div([html.H2(title), dcc.Graph(figure=fig1), dcc.Graph(figure=fig2)])


layout = ht.layout(app_dir,
                   'Top co2 emitters',
                   [fig_emission_excess('Name'),
                    fig_emission_excess('Län')])
