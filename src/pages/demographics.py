import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import src.utils.preprocess as preprocess
import src.utils.constants as constants
import src.utils.graphs.b2bbarchart as b2bbarchart
import src.utils.graphs.clustered_barchart as clustered_barchart
from src.datasets.dataframe import b2bbarchart_df
from src.datasets.dataframe import cluster_by_age_df, age_df_colors, dataframe
from src.datasets.dataframe import cluster_by_education_df, education_df_colors

dash.register_page(
    __name__,
    path='/demographics',
    title='Analyse démographique'
)

layout = html.Div(id='demographics-page', children=[
    html.Div(id='header', children=[
        html.Div(id='nav', children=[
                html.Button('Vers l\'analyse des drogues',
                            id='back-button', n_clicks=0),
        ]),
        html.H1('Analyse démographique'),
    ]),
    html.Div(children=[
        html.H2('Tranches d\'âge'),
        html.Div(className='viz', children=[
            dcc.Dropdown(
                id='dropdown-age',
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
            ),
        ]),
        html.H3('Portion de consommateurs de drogues selon la tranche d\'âge'),
        dcc.Graph(
            id='age-graph', figure=clustered_barchart.cluster_by_age(cluster_by_age_df, age_df_colors)),
    ]),
    html.Div(children=[
        html.H2('Sexe'),
        html.Div(className='viz', children=[
            dcc.Dropdown(
                id='dropdown-gender',
                options=[
                    {'label': 'Homme', 'value': 'MAN'},
                    {'label': 'Femme', 'value': 'WOMAN'},
                ],
                value='MAN',
                className='selector-dropdown',
                placeholder="Sélectionnez un sexe...",
            ),
        ]),
        html.H3('Portion de consommateurs de drogues selon le sexe'),
        dcc.Graph(id='gender-graph',
                  figure=b2bbarchart.draw_b2b_barchart(b2bbarchart_df, "MAN")),
    ]),
    html.Div(children=[
        html.H2('Niveau d\'éducation'),
        html.Div(className='viz', children=[
            dcc.Dropdown(
                id='dropdown-education',
                options=[
                    {'label': 'Ayant quitté l\'école avant 16 ans', 'value': 'BEFORE_16'},
                    {'label': 'Ayant quitté l\'école à 16 ans', 'value': 'AT_16'},
                    {'label': 'Ayant quitté l\'école à 17 ans', 'value': 'AT_17'},
                    {'label': 'Ayant quitté l\'école à 18 ans', 'value': 'AT_18'},
                    {'label': 'Ayant fréquenté une université, mais sans diplôme','value': 'SOME_COLLEGE_NO_DEGREE'},
                    {'label': 'Baccaulauréat', 'value': 'UNIVERSITY_DEGREE'},
                    {'label': 'Maîtrise', 'value': 'MASTER_DEGREE'},
                    {'label': 'Doctorat', 'value': 'DOCTORATE_DEGREE'},
                ],
                value='UNIVERSITY_DEGREE',
                className='selector-dropdown',
                placeholder="Sélectionnez un niveau d'éducation...",
            ),
        ]),
        html.H3('Portion de consommateurs de drogues selon le niveau d\'éducation'),
        dcc.Graph(id='education-graph', figure=clustered_barchart.cluster_by_education(
            cluster_by_education_df, education_df_colors)),
    ]),
])


@callback(
    Output('url-back', 'pathname'),
    Input('back-button', 'n_clicks'),
    prevent_initial_call=True
)
def navigate_to_drugs(n_clicks):
    if n_clicks > 0:
        return '/drugs'


@callback(
    Output('age-graph', 'figure'),
    Input('dropdown-age', 'value'),
    prevent_initial_call=False  # Placeholders by default to draw the graphs
)
def create_age_figure(age_range):
    if not age_range:
        return dash.no_update, dash.no_update, dash.no_update

    df, colors = preprocess.create_age_dataframe(dataframe.copy(), age_range)
    return clustered_barchart.cluster_by_age(df, colors)


@callback(
    Output('gender-graph', 'figure'),
    Input('dropdown-gender', 'value')
)
def personality_per_drug_graph(gender):
    return b2bbarchart.draw_b2b_barchart(b2bbarchart_df, gender)


@callback(
    Output('education-graph', 'figure'),
    Input('dropdown-education', 'value'),
    prevent_initial_call=False  # Placeholders by default to draw the graphs
)
def create_education_figure(education):
    if not education:
        return dash.no_update, dash.no_update, dash.no_update

    education_level = ''
    for values in constants.EducationLevel.__members__.values():
        if (education == values.value['code']):
            education_level = values
            break

    df, colors = preprocess.create_education_level_dataframe(
        dataframe, education_level)
    return clustered_barchart.cluster_by_education(df, colors)
