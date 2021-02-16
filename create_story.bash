story="$1"

mkdir $story
cd $story

touch intro.md
touch conclusion.md
touch $story.py

printf "import os
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

layout = ht.layout(app_dir,
                   'title',
                   [])" >> $story.py

