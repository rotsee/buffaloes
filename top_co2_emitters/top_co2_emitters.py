import json
import os

import chart_studio.tools as tls
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#from app import app


def html_title(title):
    return html.Div([html.H1(title)],
                    style={'textAlign': 'center'})

layout = html.Div(children=[

        html_title('Top co2 emitters'),
        html.Br(), html.Br(),

        html.Embed(src='https://chart-studio.plotly.com/~papanash/9.embed', height="1200", width="100%")
])
