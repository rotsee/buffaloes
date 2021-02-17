import importlib
import sys

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, server

stories = ['climate_goals', 'top_co2_emitters_2019', 'top_co2_emitters']


modules = [importlib.import_module(i + '.' + i) for i in stories]


def navbar():
    if len(stories) < 2:
        return html.Br()

    links = []
    for s in stories:
        name = s.replace('_', ' ').capitalize()
        links.append(dbc.NavLink(name, href='/' + s, active='exact'))
        links.append(html.Br())

    return dbc.Navbar(dbc.Nav(links, pills=True))


app.layout = html.Div([
    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    navbar(),

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
