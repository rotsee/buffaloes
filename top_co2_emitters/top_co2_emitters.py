import os

import dash
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
        [measure, 'Emissions']].sum().sort_values('Emissions', ascending=False).head(top)
    df = df_co2[df_co2[measure].isin(list(df.index))].groupby(
        [measure, 'Year']).sum().reset_index()
    return df


def percentage_change(col1, col2):
    return ((col2 - col1) / col1) * 100


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


def fig_bar(df, y):
    f = px.bar(df, y=y, x='percentage_change', orientation='h',
               labels={'percentage_change': 'percentage_change (2009 -> 2019)'})

    f.update_layout(yaxis={'categoryorder': 'total descending'}, height=800)
    return f


def get_emission_excess(measure):
    measures = ['Name', 'Län', 'Kommun', 'Bransch']
    if measure is None:
        measure = measures[0]
    suffix = '(top emitters of 2019)'

    title = measure + ' ' + suffix
    df = top_emissions_by_measure(measure)

    fig1 = fig_line(df, 'Emissions', measure, labels={
                    'Emissions': 'Emissions (tons)',
                    'Excess', 'Excess/Deficit'})
    fig2 = fig_line(df, 'Excess', measure)

    return html.Div(id='div-emission-excess',
                    children=[
                        dcc_dropdown('emission-excess',
                                     measures, measure),
                        dcc.Graph(id='fig_emissions', figure=fig1),
                        dcc.Graph(id='fig_excess', figure=fig2)])


def get_emission_pecentage_change(measure, start_year=2009, end_year=2019):
    df = df_co2[(df_co2.Year == end_year) | (df_co2.Year == start_year)
                ][[measure, 'Emissions', 'Year']]

    df = df.groupby([measure, 'Year']).sum().unstack('Year').reset_index()
    df.columns = df.columns.droplevel()
    df.columns = [measure, '2009', '2019']

    df['percentage_change'] = percentage_change(df['2009'], df['2019'])

    fig = fig_bar(df, measure)

    return html.Div([html.H2('Percentage change of all Län from 2009 to 2019'),
                     dcc.Graph(figure=fig)])


layout = ht.layout(app_dir,
                   'Top co2 emitters',
                   [get_emission_excess('Name'),
                    get_emission_pecentage_change('Län')])


@ app.callback(
    Output('div-emission-excess', 'children'),
    Input('dropdown-emission-excess', 'value'))
def update_emission_excess(selected_value):
    if selected_value is None:
        return dash.no_update
    return get_emission_excess(selected_value)
