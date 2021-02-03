import os

import dash_core_components as dcc
import dash_html_components as html
import lib.html_helper as ht
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app import app
from dash.dependencies import Input, Output

app_dir = os.path.basename(os.path.dirname(__file__))

csv_file = app_dir + '/pulitzer_prizes_adjusted.csv'

current_categories = {
    204: 'Public Service',
    205: 'Breaking News Reporting',
    206: 'Investigative Reporting',
    207: 'Explanatory Reporting',
    208: 'Local Reporting',
    209: 'National Reporting',
    210: 'International Reporting',
    211: 'Feature Writing',
    212: 'Commentary',
    213: 'Criticism',
    214: 'Editorial Writing',
    215: 'Editorial Cartooning',
    216: 'Breaking News Photography',
    217: 'Feature Photography',
    631: 'Audio Reporting'
}
df_pulitzer = pd.read_csv(csv_file, index_col=0)


def get_top_publishers(df: pd.DataFrame, top: int = 15) -> pd.DataFrame:
    top_pub = df.groupby('field_publication').size(
    ).sort_values(ascending=False)[:top]

    df_top = df[df.field_publication.isin(list(top_pub.keys()))].groupby(
        ['field_category', 'field_publication']).size()
    df_top = pd.DataFrame({'total': df_top}).reset_index()

    return df_top


def get_top_publishers_year(df: pd.DataFrame, top: int = 15) -> pd.DataFrame:
    df = df.drop(columns=['field_abbr_citation'])
    top_pub = df.groupby('field_publication').size(
    ).sort_values(ascending=False)[:15]
    return df[df.field_publication.isin(list(top_pub.keys()))]


df_top15 = get_top_publishers(df_pulitzer, 15)
df_top15_year = get_top_publishers_year(df_pulitzer, 15)


def get_data(type, category):
    if type == 'field_year':
        df = df_top15_year
    elif type == 'total':
        df = df_top15

    if category == 'current':
        df = df[df.field_category.isin(
            current_categories.values())]

    return df


def get_sankey(df_top: pd.DataFrame) -> pd.DataFrame:
    df_sankey = df_top[df_top.field_category.isin(
        list(current_categories.values()))].sort_values('total', ascending=False)

    nodes_sankey = list(df_sankey.field_category.unique()) + \
        list(df_sankey.field_publication.unique())
    df_sankey.field_category = df_sankey.field_category.apply(
        lambda x: nodes_sankey.index(x))
    df_sankey.field_publication = df_sankey.field_publication.apply(
        lambda x: nodes_sankey.index(x))

    return df_sankey, nodes_sankey


def fig_sankey():
    df_sankey, nodes_sankey = get_sankey(df_top15)

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            label=nodes_sankey
        ),
        link=dict(
            source=list(df_sankey.field_category),
            target=list(df_sankey.field_publication),
            value=list(df_sankey.total),
        ))])

    fig.update_layout(title_text="Top 15 publishers in current Categories",
                      font_size=15, height=1000, width=1000)
    return dcc.Graph(id='sankey', figure=fig)


def update_layout(fig):
    return fig.update_layout(title_text="Top 15 publishers",
                             height=800, width=1200,
                             yaxis={'categoryorder': 'total ascending'})


def fig_scatter(x, y, category='current'):
    color = 'field_category' if y == 'field_publication' else 'field_publication'
    size = x if x == 'total' else None

    df = get_data(x, category)
    fig = px.scatter(df, x=x, y=y, color=color, size=size)
    update_layout(fig)

    return fig


def fig_bar_size(category='current'):
    df = get_data('total', category)
    fig = px.bar(df, x='total', y='field_publication',
                 color='field_category', orientation='h')
    update_layout(fig)
    return fig


def fig_pie():
    return html.Div([
        dcc.Dropdown(
            id='dropdown',
            options=options,
            placeholder="Select a prize category",
            # value='Investigative Reporting',
            style={"width": "50%"}),
        dcc.Graph(id='pie-graph')
    ])


def html_radio(id_suffix):
    return html.Div([
        html.Label('Categories:'),
        dcc.RadioItems(id='current_old_' + id_suffix,
                       value='current',
                       options=[{'label': 'current', 'value': 'current'}, {
                           'label': 'current+old', 'value': 'current+old'}],
                       style={'display': 'inline-block'})])


top_pub = list(df_top15.field_category.unique())
options = [{'label': i, 'value': i} for i in top_pub]

layout = ht.layout(app_dir,
                   'Who wins the Pulitzer prizes in journalism?',
                   [fig_sankey(),

                    html.Div([html_radio('scatter'),
                              dcc.Tabs([
                                  dcc.Tab(label='By publication year', children=[dcc.Graph(
                                      id='scatter_1', figure=fig_scatter(x='field_year', y='field_publication'))]),
                                  dcc.Tab(label='By publication size', children=[dcc.Graph(
                                      id='scatter_2', figure=fig_scatter(x='total', y='field_publication'))]),
                                  dcc.Tab(label='By category year', children=[dcc.Graph(
                                      id='scatter_3', figure=fig_scatter(x='field_year', y='field_category'))]),
                                  dcc.Tab(label='By category size', children=[dcc.Graph(
                                      id='scatter_4', figure=fig_scatter(x='total', y='field_category'))])
                              ])]),


                    html.Div([html_radio('bar_size'),
                              dcc.Graph(id='bar_size', figure=fig_bar_size())]),

                    fig_pie()])


@ app.callback(
    Output('bar_size', 'figure'),
    Input('current_old_bar_size', 'value'))
def update_bar_size(category):
    return fig_bar_size(category)


@ app.callback(
    Output('scatter_1', 'figure'),
    Output('scatter_2', 'figure'),
    Output('scatter_3', 'figure'),
    Output('scatter_4', 'figure'),
    Input('current_old_scatter', 'value'))
def update_scatter(category):
    scatter_1 = fig_scatter(
        x='field_year', y='field_publication', category=category)
    scatter_2 = fig_scatter(
        x='total', y='field_publication', category=category)
    scatter_3 = fig_scatter(
        x='field_year', y='field_category', category=category)
    scatter_4 = fig_scatter(x='total', y='field_category', category=category)
    return scatter_1, scatter_2, scatter_3, scatter_4


@ app.callback(
    Output('pie-graph', 'figure'),
    Input('dropdown', 'value'))
def update_pie(selected_value):
    if selected_value is not None:
        df_filter = df_top15[df_top15.field_category == selected_value]
    else:
        df_filter = df_top15

    fig = px.pie(df_filter, values='total', names='field_publication',
                 title='Top 15 publishers')
    fig.update_traces(textposition='inside', textinfo='value+label')
    fig.update_layout(uniformtext_minsize=10,
                      uniformtext_mode='hide', height=800, width=800)
    return fig
