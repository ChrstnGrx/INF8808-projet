
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Authors: Aymen, Charles De Lafontaine
    Course: INF8808
    Python Version: 3.8

    This file is the entry point for our dash app.
'''

import dash
# import dash core components, dash html
from dash import dcc, html
from dash import page_registry, no_update
from dash.dependencies import Input, Output, State
from ucimlrepo import fetch_ucirepo

import pandas as pd

import plotly.express as px

import preprocess
# import chord
import colors

external_stylesheets = ['second_page_style.css']

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets)
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

app.layout = html.Div([
    # This component will interact with the browser's URL
    dcc.Location(id='url', refresh=False),
    # This div will contain the content that changes when we navigate between pages
    html.Div(id='page-content')
])

main_page_layout = html.Div(
    id='page-content',
    className='content', children=[
        dcc.Location(id='url', refresh=False),
        # html.Header(children=[
        #     html.H1('Projet')
        # ]),
        html.Main(className='viz-container', children=[
            # dcc.Graph(className='graph', figure=fig, config=dict(
            #     scrollZoom=False,
            #     showTips=False,
            #     showAxisDragHandles=False,
            #     doubleClick=False,
            #     displayModeBar=False
            # ))

            html.Div(className='profil-susceptible-container', style={
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
                    html.Div(children=[html.Img(id='image1'), html.P(
                        'Âge')], style={'text-align': 'center'}),
                    html.Div(children=[html.Img(id='image2'), html.P(
                        'Éducation')], style={'text-align': 'center'}),
                    html.Div(children=[html.Img(id='image3'), html.P(
                        'Sexe')], style={'text-align': 'center'})
                ], style={'display': 'flex', 'justify-content': 'space-around', 'padding': '20px', 'border': '1px solid #ccc', 'box-shadow': '0px 0px 10px #aaa'})
            ]),
            html.Div(className='Drogue-info-container', children=[
                html.Div(className='Drogue-selector-and-similar-drugs-container', children=[
                    html.Div(className='Drogue-selector-container', children=[
                        dcc.Dropdown(
                            id='image-selector',
                            options=[
                                {'label': 'Set 1', 'value': 'set1'},
                                {'label': 'Set 2', 'value': 'set2'},
                                {'label': 'Set 3', 'value': 'set3'},
                                {'label': 'Set 4', 'value': 'set4'}
                            ],
                            value='set1',  # default value
                            # Center the dropdown and add margin
                            style={'width': '300px', 'margin': '0 auto 10px'}
                        ),
                    ]),
                    html.Div(className='Similar-drugs-container', children=[

                    ]),

                ]),
                html.Div(className='Drogue-personality-and-trend-container', children=[
                    html.Div(className='Drogue-personality-container', children=[

                    ]),
                    html.Div(className='Drogue-trend-container', children=[
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
                    ]),

                ]),

            ]),

        ])

    ])

second_page_layout = html.Div([
    html.Button("Page principale", id="back-button", className="back-button"),

    html.Div(className='profil-susceptible-container', children=[
        html.H1('Profil du consommateur', className='header-title'),

        html.Div(className='selectors', children=[
            html.Div(className='age-selector selector', children=[
                html.Label('Tranche d\'âge'),
                dcc.Dropdown(
                    id='age-dropdown',
                    options=[
                        {'label': '18-24 ans', 'value': '18-24'},
                        {'label': '25-34 ans', 'value': '25-34'},
                        {'label': '35-44 ans', 'value': '35-44'},
                        {'label': '45-54 ans', 'value': '45-54'},
                        {'label': '55-64 ans', 'value': '55-64'},
                        {'label': '65+ ans', 'value': '65+'},
                    ],
                    value='18-24',
                    className='selector-dropdown',
                    placeholder="Sélectionnez une tranche d'âge...",
                )
            ]),

            html.Div(className='gender-selector selector', children=[
                html.Label('Sexe',
                           className='selector-label'),
                dcc.Dropdown(
                    id='gender-dropdown',
                    options=[
                        {'label': 'Homme', 'value': 'MAN'},
                        {'label': 'Femme', 'value': 'WOMAN'},
                    ],
                    value='MAN',
                    className='selector-dropdown',
                    placeholder="Sélectionnez un sexe...",
                )
            ]),

            html.Div(className='education-selector selector', children=[
                html.Label('Niveau d\'éducation'),
                dcc.Dropdown(
                    id='education-dropdown',
                    options=[
                        {'label': 'Quitté l\'école avant 16 ans',
                         'value': 'BEFORE_16'},
                        {'label': 'Quitté l\'école à 16 ans',
                         'value': 'AT_16'},
                        {'label': 'Quitté l\'école à 17 ans',
                         'value': 'AT_17'},
                        {'label': 'Quitté l\'école à 18 ans',
                         'value': 'AT_18'},
                        {'label': 'Fréquenté une université, mais sans diplôme',
                         'value': 'SOME_COLLEGE_NO_DEGREE'},
                        {'label': 'Baccaulauréat',
                         'value': 'UNIVERSITY_DEGREE'},
                        {'label': 'Maîtrise',
                         'value': 'MASTERS_DEGREE'},
                        {'label': 'Doctorat',
                         'value': 'DOCTORATE_DEGREE'},
                    ],
                    value='UNIVERSITY_DEGREE',
                    placeholder="Sélectionnez un niveau d'éducation...",
                )
            ]),
        ]),

        html.Div(className='graphs-container', children=[
            html.Div(className='age-graph graph-box', children=[
                html.H2('Âge', className='graph-title'),
                # Replace with actual figure
                dcc.Graph(id='age-graph', figure={}),
            ]),
            html.Div(className='gender-graph graph-box', children=[
                html.H2('Sexe', className='graph-title'),
                # Replace with actual figure
                dcc.Graph(id='gender-graph', figure={}),
            ]),
            html.Div(className='education-graph graph-box', children=[
                html.H2('Niveau d\'éducation', className='graph-title'),
                # Replace with actual figure
                dcc.Graph(id='education-graph', figure={}),
            ]),
        ])
    ])
])


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/second_page':
        return second_page_layout
    else:
        # If we have a main page layout, it should be returned here when the pathname is '/'
        return main_page_layout  # Replace with your actual main page layout


@app.callback(
    Output('url', 'pathname'),
    Input('back-button', 'n_clicks'),
    prevent_initial_call=True
)
def go_back(n_clicks):
    if n_clicks:
        return '/'
    return dash.no_update


@app.callback(
    [Output('age-graph', 'figure'),
     Output('gender-graph', 'figure'),
     Output('education-graph', 'figure')],
    [Input('age-dropdown', 'value'),
     Input('gender-dropdown', 'value'),
     Input('education-dropdown', 'value')],
    prevent_initial_call=False  # Placeholders by default to draw the graphs
)
def update_graphs(age_range, gender, education):
    if not all([age_range, gender, education]):
        return dash.no_update, dash.no_update, dash.no_update

    age_figure = create_age_figure(age_range)
    gender_figure = create_gender_figure(gender)
    education_figure = create_education_figure(education)

    return age_figure, gender_figure, education_figure


def create_age_figure(age_range):
    # Just a simple example, replace with your actual data and logic
    data = {
        'Age Range': ['18-24', '25-34', '35-44', '45-54', '55-64', '65+'],
        'Count': [10, 20, 30, 40, 50, 60]
    }
    df = pd.DataFrame(data)
    fig = px.bar(df, x='Age Range', y='Count',
                 title=f'Age Distribution for {age_range}')
    fig.update_traces(marker_color='blue')
    return fig


def create_gender_figure(gender):
    # Just a simple example, replace with your actual data and logic
    data = {
        'Gender': ['Homme', 'Femme'],
        'Count': [60, 40] if gender == 'MAN' else [40, 60]
    }
    df = pd.DataFrame(data)
    fig = px.bar(df, x='Gender', y='Count',
                 title=f'Gender Distribution for {gender}')
    fig.update_traces(marker_color='pink' if gender ==
                      'WOMAN' else 'lightblue')
    return fig


def create_education_figure(education):
    # Just a simple example, replace with your actual data and logic
    data = {
        'Education Level': ['Before 16', 'At 16', 'At 17', 'At 18', 'Some College', 'Bachelor', 'Masters', 'Doctorate'],
        'Count': [5, 10, 15, 20, 25, 30, 35, 40]
    }
    df = pd.DataFrame(data)
    fig = px.bar(df, x='Education Level', y='Count',
                 title=f'Education Level Distribution for {education}')
    fig.update_traces(marker_color='orange')
    return fig
