import glob
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import lib.html_helper as ht
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app import app
from dash.dependencies import Input, Output

app_dir = os.path.basename(os.path.dirname(__file__))

files = glob.glob(os.path.dirname(__file__) + '/*.csv')

if len(files) == 1:
    csv_file = files[0]

df_pct_change = pd.read_csv(csv_file, index_col=0)
emission_color = px.colors.qualitative.Plotly[0]


def project(df, target_year, current_year, current_value, change):

    if change is None:
        change = round(df['pct_change'].mean(), 2)

    i = df.last_valid_index() + 1

    if current_year == target_year:
        return current_year, round(current_value, 1)
    else:
        current_year = current_year + 1

        current_value - abs(change) / 100 * current_value

        return project(df, target_year, current_year, current_value - abs(change) / 100 * current_value, change)


def climate_goal_projection(measure='value', target=2045, target_value_max=10.7):
    df = df_pct_change
    fig = go.Figure()

    fig.add_trace(
        go.Bar(x=df.year, y=df[measure], marker_color=emission_color))
    fig.update_traces(showlegend=False)
    fig.add_trace(
        go.Bar(x=[target], y=[target_value_max], marker_color='green', name='emission offset'))

    last = df.iloc[-1]

    project_pct = abs(round(df['pct_change'].mean(), 1))
    #project_val = project(df, 2045, df.year.iat[-1], df.value.iat[-1])

    fig.add_trace(go.Scatter(x=[last.year, target], y=[last.value, 38.3],
                             name=str(project_pct) +
                             '% reduction (current average)',
                             line=dict(color=emission_color, dash='dash')))

    fig.add_trace(go.Scatter(x=[last.year, target], y=[
        last.value, 0], name='6% reduction (offset needed)', line=dict(color='green', dash='dot')))
    fig.add_trace(go.Scatter(x=[last.year, target], y=[
        last.value, target_value_max], name='10% reduction (offset not needed)', line=dict(color='green', dash='dot')))

    tick_years = [1990, 2000, 2010, 2020, 2030, 2040, 2045]
    fig.update_layout(yaxis={'title': 'Emissions (M tons)'},
                      xaxis=dict(tickmode='array',
                                 tickvals=tick_years, ticktext=tick_years),
                      height=500)

    return dcc.Graph(figure=fig)


transport_goal = 'The long-term goal is complemented by several interim targets. One such a goal is to limit the emissions from domestic transport. By 2030, excluding domestic aviation, it will be reduced by at least 70 percent compared with 2010.'


def transport_goal_projection(measure='domestic_transport', target=2030, target_value_max=6.2):
    df = df_pct_change[df_pct_change.year > 2009]
    fig = go.Figure()

    fig.add_trace(
        go.Bar(x=df.year, y=df[measure], marker_color=emission_color))
    fig.add_trace(
        go.Bar(x=[target], y=[target_value_max], marker_color=emission_color))
    fig.update_traces(showlegend=False)

    last = df.iloc[-1]

    project_pct = abs(round(df['pct_change_domestic_transport'].mean(), 1))

    # project_val = project(df, target, last.year, df.domestic_transport.iat[-1], 8.5) 14.5

    fig.add_trace(go.Scatter(x=[last.year, target], y=[last[measure], 14.5],
                             name=str(project_pct) + '% reduction (current average)', line=dict(color=emission_color, dash='dash')))

    fig.add_trace(go.Scatter(x=[last.year, target], y=[
        last[measure], target_value_max], name='8.5% reduction', line=dict(color='green', dash='dot')))

    tick_years = [2010, 2020, 2030]
    fig.update_layout(yaxis={'title': 'Emissions (M tons)'},
                      xaxis=dict(tickmode='array',
                                 tickvals=tick_years, ticktext=tick_years),
                      height=500)

    return html.Div([ht.html_heading('Tranport goals'), ht.html_intro(transport_goal), dcc.Graph(figure=fig)])


layout = ht.layout(app_dir,
                   'Can Sweden meet its climate goals?',
                   climate_goal_projection(),
                   transport_goal_projection())
