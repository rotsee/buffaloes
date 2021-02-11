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

top = 10
start_year = 2009
end_year = 2019
measures = ['Name', 'Län', 'Kommun']


def emission_excess(measure, top=top, year=end_year):
    df = df_co2[(df_co2.Year == year)].groupby(measure)[
        [measure, 'Emissions']].sum().sort_values('Emissions', ascending=False).head(top)
    df = df_co2[df_co2[measure].isin(list(df.index))].groupby(
        [measure, 'Year']).sum().reset_index()
    return df


def emissions_pecentage_change(measure, top=top, start_year=start_year, end_year=end_year):
    df = df_co2[(df_co2.Year == end_year) | (df_co2.Year == start_year)
                ][[measure, 'Emissions', 'Year']]

    df = df.groupby([measure, 'Year']).sum().unstack('Year').reset_index()
    df.columns = df.columns.droplevel()
    df.columns = [measure, start_year, end_year]
    df = df[(df[start_year] != 0) & (df[end_year] != 0) & (
        df[start_year].notna()) & (df[end_year].notna())]

    df['percentage_change'] = percentage_change(df[start_year], df[end_year])

    if measure != 'Län':
        df = df.sort_values(by='percentage_change')
        df = pd.concat([df.head(top), df.tail(top)])
    return df


def percentage_change(col1, col2):
    return ((col2 - col1) / col1) * 100


def html_emission_excess(measure):
    df = emission_excess(measure)

    fig1 = ht.fig_line(df, 'Emissions', measure,
                       labels={'Emissions': 'Emissions (tons)', 'Excess': 'Excess/Deficit'})
    fig2 = ht.fig_line(df, 'Excess', measure)

    return html.Div(id='div-emission-excess',
                    children=[ht.dcc_dropdown('emission-excess',
                                              measures, measure),
                              dcc.Graph(figure=fig1),
                              dcc.Graph(figure=fig2)])


def html_emission_pecentage_change(measure):
    df = emissions_pecentage_change(measure)

    fig = ht.fig_bar(df, measure, x='percentage_change', labels={
        'percentage_change': 'percentage_change (2009 -> 2019)'})
    fig.update_layout(
        yaxis={'categoryorder': 'total descending'}, height=800)
    fig.update_yaxes(ticklabelposition='outside right')

    return html.Div(id='div-emission-pecentage-change',
                    children=[html.H2('Percentage change of all Län from 2009 to 2019'),
                              ht.dcc_dropdown('emission-pecentage-change',
                                              measures, measure),
                              dcc.Graph(figure=fig)])


layout = ht.layout(app_dir,
                   'Top co2 emitters',
                   [html_emission_excess('Name'),
                    html_emission_pecentage_change('Län')])


@ app.callback(
    Output('div-emission-excess', 'children'),
    Input('dropdown-emission-excess', 'value'))
def update_emission_excess(selected_value):
    if selected_value is None:
        return dash.no_update
    return html_emission_excess(selected_value)


@ app.callback(
    Output('div-emission-pecentage-change', 'children'),
    Input('dropdown-emission-pecentage-change', 'value'))
def update_emission_excess(selected_value):
    if selected_value is None:
        return dash.no_update
    return html_emission_pecentage_change(selected_value)
