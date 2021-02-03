import dash_html_components as html
from lib.html_helper import *

layout = html.Div(children=[
    html_title('Top co2 emitters'),
    html_body('top_co2_emitters',
              [html.Embed(src='https://chart-studio.plotly.com/~papanash/9.embed', height="1000", width="100%")])
])
