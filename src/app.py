
# -*- coding: utf-8 -*-
'''
    File name: app.py
    Course: INF8808
    Python Version: 3.8

    This file is the entry point for our dash app.
'''
import dash
from dash import dcc, html

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        'assets/style.css',
        'assets/drugs_style.css',
        'assets/demographics_style.css',
    ],
    title='PROJET | INF8808'
)

authors = [
    "Charles DE LAFONTAINE", "Dieynaba DIALLO", "Erika FOSSOUO",
    "Christine GROUX", "Samira YAZDANPOURMOGHADAM", "Aymen-Alaeddine ZEGHAIDA"
]

app.layout = html.Div([
    dcc.Location(id='url-forward', refresh=True),
    dcc.Location(id='url-forward-forward', refresh=True),
    dcc.Location(id='url-back', refresh=True),
    dcc.Location(id='url-back-back', refresh=True),
    html.Div([
        html.Div(
            dcc.Link('', href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container,
    html.Div(children=[
        html.Div([html.Div(author, className="author") for author in authors]),
        html.Div('Projet final pour le cours INF8808'),
        html.Div('Polytechnique Montréal'),
    ], id='footer')
])
