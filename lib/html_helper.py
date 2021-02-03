import os
from pathlib import Path

import dash_core_components as dcc
import dash_html_components as html


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def html_title(title):
    return html.Div([html.H1(title)],
                    style={'textAlign': 'center'})


def html_intro(text):
    return html.Div([dcc.Markdown(text)],
                    style={'textAlign': 'center'})


def html_body(story, items: list):
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
