import os
from pathlib import Path

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px


def get_project_root() -> Path:
    return Path(__file__).parent.parent

# page layout


def html_title(title):
    return html.Div([html.H2(title)], style={'textAlign': 'center'})


def html_heading(text):
    return html.Div([html.H2(text), html.Br()], style={'textAlign': 'center'})


def html_intro(text):
    return html.Div([dcc.Markdown(text)])
    # ,style={'textAlign': 'center'})


def html_body(story, items):
    intro_file = Path.joinpath(get_project_root(), story, 'intro.md')
    if os.path.exists(intro_file):
        intro_text = """{}""".format(open(intro_file).read())
        items = [html_intro(intro_text)] + items

    conclusion_file = Path.joinpath(get_project_root(), story, 'conclusion.md')
    if os.path.exists(conclusion_file):
        conclusion_text = """{}""".format(open(conclusion_file).read())
        items = items + [dcc.Markdown(conclusion_text)]

    items = [v for i in items for v in (html.Br(), html.Br(), i)]

    return html.Div(items)


def layout(story, titte, *items):
    return dbc.Container([
        html_title(titte),
        html_body(story, list(items))])


# px figure helpers


def fig_line(df, y, color, **kw):
    if 'Year' in df.columns:
        x = 'Year'
    return px.line(df, x=df[x], y=df[y], color=color,
                   hover_name=color, hover_data=df.columns, **kw)


def fig_bar(df, y, **kw):
    return px.bar(df, y=y, hover_data=df.columns, **kw)

# dcc components helpers


def dcc_dropdown(id_suffix, options, default_value):
    return dcc.Dropdown(
        id='dropdown-' + id_suffix,
        options=[{'label': i, 'value': i}
                 for i in options],
        placeholder='Select a ' + 'measure',
        value=default_value,
        style={'width': '50%'})
    # , 'display': 'flex','align - items': 'center', 'justify - content': 'center'})
