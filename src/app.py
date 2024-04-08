
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Authors: TODO
    Course: INF8808
    Python Version: 3.8

    This file is the entry point for our dash app.
'''

import dash
# import dash core components, dash html
from dash import dcc, html
from dash.dependencies import Input, Output
from ucimlrepo import fetch_ucirepo 

import pandas as pd

import preprocess
# import chord
import colors

app = dash.Dash(__name__)
app.title = 'PROJET | INF8808'

# fetch dataset 
dataframe = fetch_ucirepo(id=373).data.original
dataframe = preprocess.drop_columns(dataframe)
dataframe = preprocess.fix_errors(dataframe)
# dataframe = preprocess.convert_scores(dataframe)

personality_per_drug_df = preprocess.personality_per_drug(dataframe)
# print(personality_per_drug_df)

drug_corr_df = preprocess.drug_correlation(dataframe)
print(drug_corr_df)
# chord.create_chord_diagram(drug_corr_df)

app.layout = html.Div(className='content', children=[
    html.Header(children=[
        html.H1('Projet')
    ]),
    html.Main(className='viz-container', children=[
        # dcc.Graph(className='graph', figure=fig, config=dict(
        #     scrollZoom=False,
        #     showTips=False,
        #     showAxisDragHandles=False,
        #     doubleClick=False,
        #     displayModeBar=False
        # ))

        html.Div(className='profil-susceptible-container',style={
            'border': '1px solid black',  # Black outline
            'width': '60%',  # Smaller width
            'margin': '0 auto',  # Centering
            'padding': '20px',
            'box-shadow': '0px 0px 10px #aaa'
        }, children=[
            # text
            html.H2('Profil Susceptible', style={'textAlign': 'left'}),
            # Div
            html.Div(id='image-boxes', children=[
                html.Div(children=[html.Img(id='image1'), html.P('Age')], style={'text-align': 'center'}),
                html.Div(children=[html.Img(id='image2'), html.P('Education')], style={'text-align': 'center'}),
                html.Div(children=[html.Img(id='image3'), html.P('Gender')], style={'text-align': 'center'})
            ], style={'display': 'flex', 'justify-content': 'space-around', 'padding': '20px', 'border': '1px solid #ccc', 'box-shadow': '0px 0px 10px #aaa'})
        ]),
        dcc.Dropdown(
            id='image-selector',
            options=[
                {'label': 'Set 1', 'value': 'set1'},
                {'label': 'Set 2', 'value': 'set2'},
                {'label': 'Set 3', 'value': 'set3'},
                {'label': 'Set 4', 'value': 'set4'}
            ],
            value='set1',  # default value
            style={'width': '300px', 'margin': '0 auto 10px'}  # Center the dropdown and add margin
        ),
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
        ),


    ])

])

for group in colors.GROUPS:
    app.layout.children.append(
        html.Div(className='color-container', style={'display': 'inline-block'}, children=[
            html.H2(group),
            html.Div(style={'background-color': colors.MAIN_COLORS[group], 'height': '50px', 'width': '100px'}, children=colors.MAIN_COLORS[group]),
            html.Div(style={'height': '20px', 'width': '100px'}),
            html.Div(className='color-list', children=[
                html.Div(style={'background-color': color, 'height': '50px', 'width': '100px'}, children=color) for color in colors.TRIADS[group]
            ]),
            html.Div(style={'height': '20px', 'width': '100px'}),
            html.Div(className='color-list', children=[
                html.Div(style={'background-color': color, 'height': '50px', 'width': '100px'}, children=color) for color in colors.SHADES[group]
            ]),
        ])
    )
