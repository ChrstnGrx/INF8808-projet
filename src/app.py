
# -*- coding: utf-8 -*-
'''
    File name: app.py
    Authors: Aymen, Charles De Lafontaine
    Course: INF8808
    Python Version: 3.8

    This file is the entry point for our dash app.
'''

import dash
from dash import dcc, html
import sys
from pathlib import Path

base_path = Path(__file__).resolve().parent.parent
sys.path.append(str(base_path))

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

app.layout = html.Div([
    dcc.Location(id='url-forward', refresh=True),
    dcc.Location(id='url-forward-forward', refresh=True),
    dcc.Location(id='url-back', refresh=True),
    dcc.Location(id='url-back-back', refresh=True),
    html.Div([
        html.Div(
            dcc.Link('',
                     href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
])
