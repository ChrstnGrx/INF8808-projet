
# -*- coding: utf-8 -*-
'''
    File name: app.py
    Authors: Aymen, Charles De Lafontaine
    Course: INF8808
    Python Version: 3.8

    This file is the entry point for our dash app.
'''

# import src.utils.preprocess as preprocess
# import plotly.express as px
# import pandas as pd
# from src.chord import create_chord_diagram, create_legend, active_palette
# from ucimlrepo import fetch_ucirepo
import dash
from dash import dcc, html
# from dash import page_registry, no_update
# from dash.dependencies import Input, Output, State
import sys
from pathlib import Path
# import utils.graphs.parallel_coords as pc
# import utils.graphs.stacked_bar as sb
from src.components import footer

base_path = Path(__file__).resolve().parent.parent
sys.path.append(str(base_path))

app = dash.Dash(
    __name__, 
    use_pages=True,
    # external_stylesheets=[
    #     'main_page_style.css', 
    #     'second_page_style.css',
    # ],
    external_stylesheets=[
        'assets/style.css',
    ],
    title='PROJET | INF8808'
)

app.layout = html.Div([
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container,
    footer
])

# # fetch dataset
# dataframe = fetch_ucirepo(id=373).data.original
# dataframe = preprocess.drop_columns(dataframe)
# dataframe = preprocess.fix_errors(dataframe)
# # dataframe = preprocess.convert_scores(dataframe)
# personality_per_drug_df = preprocess.personality_per_drug(dataframe)
# consumption_per_drug_df = preprocess.consumption_per_drug(dataframe)
# drug_corr_df = preprocess.drug_correlation(dataframe)
# drug_options, default_value = preprocess.generate_drogue_options(dataframe)

# # print(personality_per_drug_df)
# # print(drug_corr_df)
# # chord.create_chord_diagram(drug_corr_df)

# app.layout = html.Div([
#     # This component will interact with the browser's URL
#     dcc.Location(id='url', refresh=False),
#     html.Button("Second page", id="forward-button",
#                 className="forward-button"),
#     # This div will contain the content that changes when we navigate between pages
#     html.Div(id='page-content')
# ])

# main_page_layout = html.Div([
#     html.Div(className='rectangle-container', children=[
#         html.H1('Profil Susceptible', className='title'),
#         html.Div(className='image-boxes', children=[  # Use this div to group the image boxes
#             html.Div(className='image-box', children=[
#                 html.Img(src='/assets/icons/graduate-cap-solid.svg'),
#                 html.Label('Education', className='image-label')
#             ]),
#             html.Div(className='image-box', children=[
#                 html.Img(src='/assets/icons/diploma.svg'),
#                 html.Label('Age', className='image-label')
#             ]),
#             html.Div(className='image-box', children=[
#                 html.Img(src='/assets/icons/man.svg'),
#                 html.Label('Gender', className='image-label')
#             ])
#         ])
#     ]),

#     # Grid with adjusted box styles and rectangles in the second column 
#     html.Div(
#         className='grid-container',
#         children=[
#             html.Div(
#                 className='box-1',
#                 children=[
#                     dcc.Dropdown(
#                         id='dropdown-drug',
#                         className = 'dropdown-drug-selector',
#                         options=drug_options,  # Assuming this is defined somewhere in your code
#                         placeholder="Sélectionnez une drogue ...",
#                         style={'width': '100%'}  # Adjusting width and margin
#                     ),
#                     html.Div(
#                         className='image-box gateway-drug-variant',
#                         children=[
#                             html.Img(src='/assets/icons/gateway-drugs.png'),
#                             html.Label('Attention : Ceci s\'agit d\'une drogue passerelle', 
#                                     className='image-label-gateway', 
#                                     )],
#                     )
#                 ]
#             ),
#             html.Div(className='rectangle-1', 
#                      children=[
#                         dcc.Graph(
#                             id='personality_per_drug_graph', 
#                             figure=pc.get_plot(personality_per_drug_df), 
#                             config={'responsive': True}
#                         ),
#                         html.Div(className='legend', children=pc.get_legend())
#                     ]),
#             html.Div(className='box-2',
#                      children=[
#                         dcc.Graph(
#                             id='graph-3',
#                             figure=sb.get_plot(consumption_per_drug_df),  
#                             config={'responsive': True}           
#                         ),
#                         html.Div(className='legend', children=sb.get_legend())
#                      ]),
#             html.Div(className='rectangle-2',
#                 children=dcc.Graph(
#                     id='graph-4', 
#                     figure={}, 
#                     config={'responsive': True}  # Make the graph responsive to its container
#                 )
#             )
#         ]),

# ])

# second_page_layout = html.Div([
#     html.Button("Page principale", id="back-button", className="back-button"),

#     html.Div(className='profil-susceptible-container', children=[
#         html.H1('Profil du consommateur', className='header-title'),

#         html.Div(className='selectors', children=[
#             html.Div(className='age-selector selector', children=[
#                 html.Label('Tranche d\'âge'),
#                 dcc.Dropdown(
#                     id='age-dropdown',
#                     options=[
#                         {'label': '18-24 ans', 'value': '18-24'},
#                         {'label': '25-34 ans', 'value': '25-34'},
#                         {'label': '35-44 ans', 'value': '35-44'},
#                         {'label': '45-54 ans', 'value': '45-54'},
#                         {'label': '55-64 ans', 'value': '55-64'},
#                         {'label': '65+ ans', 'value': '65+'},
#                     ],
#                     value='18-24',
#                     className='selector-dropdown',
#                     placeholder="Sélectionnez une tranche d'âge...",
#                 )
#             ]),

#             html.Div(className='gender-selector selector', children=[
#                 html.Label('Sexe',
#                            className='selector-label'),
#                 dcc.Dropdown(
#                     id='gender-dropdown',
#                     options=[
#                         {'label': 'Homme', 'value': 'MAN'},
#                         {'label': 'Femme', 'value': 'WOMAN'},
#                     ],
#                     value='MAN',
#                     className='selector-dropdown',
#                     placeholder="Sélectionnez un sexe...",
#                 )
#             ]),

#             html.Div(className='education-selector selector', children=[
#                 html.Label('Niveau d\'éducation'),
#                 dcc.Dropdown(
#                     id='education-dropdown',
#                     options=[
#                         {'label': 'Quitté l\'école avant 16 ans',
#                          'value': 'BEFORE_16'},
#                         {'label': 'Quitté l\'école à 16 ans',
#                          'value': 'AT_16'},
#                         {'label': 'Quitté l\'école à 17 ans',
#                          'value': 'AT_17'},
#                         {'label': 'Quitté l\'école à 18 ans',
#                          'value': 'AT_18'},
#                         {'label': 'Fréquenté une université, mais sans diplôme',
#                          'value': 'SOME_COLLEGE_NO_DEGREE'},
#                         {'label': 'Baccaulauréat',
#                          'value': 'UNIVERSITY_DEGREE'},
#                         {'label': 'Maîtrise',
#                          'value': 'MASTERS_DEGREE'},
#                         {'label': 'Doctorat',
#                          'value': 'DOCTORATE_DEGREE'},
#                     ],
#                     value='UNIVERSITY_DEGREE',
#                     placeholder="Sélectionnez un niveau d'éducation...",
#                 )
#             ]),
#         ]),

#         html.Div(className='graphs-container', children=[
#             html.Div(className='age-graph graph-box', children=[
#                 html.H2('Âge', className='graph-title'),
#                 # Replace with actual figure
#                 dcc.Graph(id='age-graph', figure={}),
#             ]),
#             html.Div(className='gender-graph graph-box', children=[
#                 html.H2('Sexe', className='graph-title'),
#                 # Replace with actual figure
#                 dcc.Graph(id='gender-graph', figure={}),
#             ]),
#             html.Div(className='education-graph graph-box', children=[
#                 html.H2('Niveau d\'éducation', className='graph-title'),
#                 # Replace with actual figure
#                 dcc.Graph(id='education-graph', figure={}),
#             ]),
#         ])
#     ])
# ])


# @ app.callback(
#     [Output('chord-diagram', 'figure'),
#      Output('chord-diagram-legend', 'children')],
#     [Input('image-selector', 'value')]
# )
# def update_chord_diagram_and_legend(active_drug):
#     if not active_drug:
#         # Or return an empty figure and empty legend if you prefer
#         return dash.no_update, dash.no_update

#     # Assuming `drug_corr_df` is your DataFrame with the correlations
#     fig = create_chord_diagram(drug_corr_df, active_drug)
#     legend = create_legend(active_drug, drug_corr_df, active_palette)

#     return fig, legend


# @ app.callback(
#     Output('page-content', 'children'),
#     [Input('url', 'pathname')]
# )
# def display_page(pathname):
#     if pathname == '/second_page':
#         return second_page_layout
#     else:
#         # If we have a main page layout, it should be returned here when the pathname is '/'
#         return main_page_layout  # Replace with your actual main page layout


# @ app.callback(
#     Output('url', 'pathname'),
#     Input('back-button', 'n_clicks'),
#     prevent_initial_call=True
# )
# def go_back(n_clicks):
#     if n_clicks:
#         return '/'
#     return dash.no_update


# @ app.callback(
#     [Output('age-graph', 'figure'),
#      Output('gender-graph', 'figure'),
#      Output('education-graph', 'figure')],
#     [Input('age-dropdown', 'value'),
#      Input('gender-dropdown', 'value'),
#      Input('education-dropdown', 'value')],
#     prevent_initial_call=False  # Placeholders by default to draw the graphs
# )
# def update_graphs(age_range, gender, education):
#     if not all([age_range, gender, education]):
#         return dash.no_update, dash.no_update, dash.no_update

#     age_figure = create_age_figure(age_range)
#     gender_figure = create_gender_figure(gender)
#     education_figure = create_education_figure(education)

#     return age_figure, gender_figure, education_figure


# def create_age_figure(age_range):
#     # Just a simple example, replace with your actual data and logic
#     data = {
#         'Age Range': ['18-24', '25-34', '35-44', '45-54', '55-64', '65+'],
#         'Count': [10, 20, 30, 40, 50, 60]
#     }
#     df = pd.DataFrame(data)
#     fig = px.bar(df, x='Age Range', y='Count',
#                  title=f'Age Distribution for {age_range}')
#     fig.update_traces(marker_color='blue')
#     return fig


# def create_gender_figure(gender):
#     # Just a simple example, replace with your actual data and logic
#     data = {
#         'Gender': ['Homme', 'Femme'],
#         'Count': [60, 40] if gender == 'MAN' else [40, 60]
#     }
#     df = pd.DataFrame(data)
#     fig = px.bar(df, x='Gender', y='Count',
#                  title=f'Gender Distribution for {gender}')
#     fig.update_traces(marker_color='pink' if gender ==
#                       'WOMAN' else 'lightblue')
#     return fig


# def create_education_figure(education):
#     # Just a simple example, replace with your actual data and logic
#     data = {
#         'Education Level': ['Before 16', 'At 16', 'At 17', 'At 18', 'Some College', 'Bachelor', 'Masters', 'Doctorate'],
#         'Count': [5, 10, 15, 20, 25, 30, 35, 40]
#     }
#     df = pd.DataFrame(data)
#     fig = px.bar(df, x='Education Level', y='Count',
#                  title=f'Education Level Distribution for {education}')
#     fig.update_traces(marker_color='orange')
#     return fig
