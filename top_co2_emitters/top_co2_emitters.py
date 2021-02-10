import os

import dash_core_components as dcc
import dash_html_components as html
import lib.html_helper as ht
import numpy as np
import pandas as pd
import plotly.express as px
from app import app
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


def dcc_dropdown(id_suffix, options, default_value):
    return dcc.Dropdown(
        id='dropdown-' + id_suffix,
        options=[{'label': i, 'value': i}
                 for i in options],
        placeholder='Select a ' + 'measure',
        value=default_value,
        style={'width': '50%'})
    # , 'display': 'flex','align - items': 'center', 'justify - content': 'center'})


def fig_line(df, y, color, **kw):
    return px.line(df, x=df.Year, y=df[y], color=color,
                   hover_name=color, hover_data=df.columns, **kw)


def get_emission_excess(measure):
    measures = ['Name', 'Län', 'Kommun', 'Bransch']
    if measure is None:
        measure = measures[0]
    suffix = '(top emitters of 2019)'

    title = measure + ' ' + suffix
    df = top_emissions_by_measure(measure)

    fig1 = fig_line(df, 'Emissions', measure, labels={
                    'Emissions': 'Emissions (tons)'})
    fig2 = fig_line(df, 'Excess', measure)

    return html.Div(id='div-emission-excess',
                    children=[
                        dcc_dropdown('emission-excess',
                                     measures, measure),
                        dcc.Graph(id='fig_emissions', figure=fig1),
                        dcc.Graph(id='fig_excess', figure=fig2)])


layout = ht.layout(app_dir,
                   'Top co2 emitters',
                   [get_emission_excess('Name')])


@ app.callback(
    Output('div-emission-excess', 'children'),
    Input('dropdown-emission-excess', 'value'))
def update_emission_excess(selected_value):
    return get_emission_excess(selected_value)
