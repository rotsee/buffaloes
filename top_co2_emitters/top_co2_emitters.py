import os

import dash_html_components as html
import lib.html_helper as ht

app_dir = os.path.basename(os.path.dirname(__file__))


layout = ht.layout(app_dir,
                   'Top co2 emitters',
                   [html.Br()])
