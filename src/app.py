
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Authors: TODO
    Course: INF8808
    Python Version: 3.8

    This file is the entry point for our dash app.
'''

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from ucimlrepo import fetch_ucirepo 

import pandas as pd

import preprocess

app = dash.Dash(__name__)
app.title = 'PROJET | INF8808'

# fetch dataset 
dataframe = fetch_ucirepo(id=373).data.original
dataframe = preprocess.drop_columns(dataframe)
dataframe = preprocess.fix_errors(dataframe)
# dataframe = preprocess.convert_scores(dataframe)

personality_per_drug_df = preprocess.personality_per_drug(dataframe)
print(personality_per_drug_df)

app.layout = html.Div(className='content', children=[
    html.Header(children=[
        html.H1('Projet')
    ]),
    dcc.Graph(
        id='parallel-coordinates',
        figure={
            'data': [
                {
                    'type': 'parcoords',
                    'dimensions': [
                        {'label': col, 'values': personality_per_drug_df[col], 'range': [-1, 1]} for col in personality_per_drug_df.columns
                    ]
                }
            ],
            'layout': {
                'title': 'Parallel Coordinates Chart'
            }
        }
    )
])
