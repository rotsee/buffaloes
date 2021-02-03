import json
import os

import chart_studio.tools as tls
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from lib.html_helper import *

layout = html.Div(children=[
    html_title('Top co2 emitters'),
    html_body('top_co2_emitters',
              [html.Embed(src='https://chart-studio.plotly.com/~papanash/9.embed', height="1000", width="100%")])
])
