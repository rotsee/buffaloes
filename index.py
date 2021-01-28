import importlib
import sys

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, server

stories = ['top_co2_emitters', 'pulitzer']

modules = [importlib.import_module(i + '.' + i) for i in stories]


def html_links():
    links = []
    for i in stories:
        links.append(dcc.Link(i, href='/' + i))
        links.append(html.Br())

    return html.Div(links)


app.layout = html.Div([
    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    html_links(),

    # content will be rendered in this element
    html.Div(id='page-content')
])


@ app.callback(Output('page-content', 'children'),
               Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return modules[0].layout
    else:
        module = sys.modules[pathname[1:] + '.' + pathname[1:]]
        return module.layout
    # else:
    #     return '404'


if __name__ == '__main__':
    app.run_server(debug=True)
