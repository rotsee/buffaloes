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

df = pd.read_csv(csv_file, index_col=0)


def climate_goal_projection(target=2045, target_value_max=10.7):
    fig = go.Figure()

    fig.add_trace(go.Bar(x=df.year, y=df.value))
    fig.add_trace(
        go.Bar(x=[target], y=[target_value_max], marker_color='green'))
    fig.update_traces(showlegend=False)

    last_year = df.iloc[-1].year
    last_value = df.iloc[-1].value

    fig.add_trace(go.Scatter(x=[last_year, target], y=[last_value, 38.3],
                             name='1.1% reduction (current average)', line=dict(color='blue', dash='dash')))
    fig.add_trace(go.Scatter(x=[last_year, target], y=[
        last_value, 0], name='6% reduction (offset needed)', line=dict(color='green', dash='dot')))
    fig.add_trace(go.Scatter(x=[last_year, target], y=[
        last_value, target_value_max], name='10% reduction (offset not needed)', line=dict(color='green', dash='dot')))

    tick_years = [1990, 2000, 2010, 2020, 2030, 2040, 2045]
    fig.update_layout(yaxis={'title': 'Emissions (M tons)'},
                      xaxis=dict(tickmode='array',
                                 tickvals=tick_years, ticktext=tick_years),
                      height=500)

    return dcc.Graph(figure=fig)


layout = ht.layout(app_dir,
                   'Can Sweden meet its climate goals?',
                   [climate_goal_projection()])
