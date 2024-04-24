import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output

from src.datasets.dataframe import drug_corr_df, personality_per_drug_df, consumption_per_drug_df, profiles_df
from src.utils.constants import DRUG_INFO, GATEWAY_DRUGS, AGE_IMAGE_PATHS, GENDER_IMAGE_PATHS, EDUCATION_IMAGE_PATHS

import src.utils.graphs.parallel_coords as pc
import src.utils.graphs.stacked_bar as sb
import src.utils.graphs.chord_diagram as cd

dash.register_page(
    __name__,
    path='/drugs',
    title='Analyse des drogues',)

drug_options = [{'label': DRUG_INFO[drug]['french'].capitalize(), 'value': drug}
                for drug in DRUG_INFO]


# print()


drug_options = [{'label': DRUG_INFO[drug]['french'].capitalize(), 'value': drug}
                for drug in DRUG_INFO]

layout = html.Div(id='drugs-page', children=[
    html.Div(id='header', children=[
        html.Div(id='nav', children=[
            html.Button('Vers l\'accueil',
                        id='back-back-button', n_clicks=0),
                html.Button('Vers l\'analyse démographique',
                            id='forward-button', n_clicks=0),
        ]),
        html.H1('Analyse des drogues'),
    ]),
    html.Div(id='viz1-wrapper', children=[
        html.H2('Profil susceptible'),
        html.Div(className='viz', children=[
            dcc.Dropdown(
                id='dropdown-drug',
                options=drug_options,
                placeholder="Veuillez sélectionner une drogue...",
            ),
            html.Div(id='warning'),
            html.Div(id='typical-person'),
        ]),
    ]),
    html.Div(
        id='personality_per_drug',
        className='chart-container',
        children=[
            html.H2(
                'Tendances pour chaque trait de personnalité selon la drogue consommée'),
            dcc.Graph(
                id='personality_per_drug_graph',
                className='chart',
                figure=pc.get_plot(personality_per_drug_df),
            ),
            html.Div(className='legend-wrapper', children=[
                html.H3("Légende"),
                html.Div(
                    id='personality_per_drug_legend',
                    className='legend',
                    children=pc.get_legend()
                )
            ])
        ]
    ),
    html.Div(
        id='drug_consumption',
        className='chart-container',
        children=[
            html.H2('Fréquences de consommation pour chaque drogue'),
            dcc.Graph(
                id='drug_consumption_graph',
                className='chart',
                figure=sb.get_plot(consumption_per_drug_df),
            ),
            html.Div(id='legend-drug-consumption', className='legend-wrapper', children=[
                html.H3("Légende"),
                html.Div(
                    id='drug_consumption_legend',
                    className='legend',
                    children=sb.get_legend()
                )
            ])
        ]
    ),
    html.Div(id='jointly-consumed-drugs', className='chart-container'),
])


@callback(
    Output('url-back-back', 'pathname'),
    Input('back-back-button', 'n_clicks'),
    prevent_initial_call=True
)
def navigate_to_home(n_clicks):
    if n_clicks > 0:
        return '/home'


@callback(
    Output('url-forward', 'pathname'),
    Input('forward-button', 'n_clicks'),
    prevent_initial_call=True
)
def navigate_to_demographics(n_clicks):
    if n_clicks > 0:
        return '/demographics'


@callback(
    Output('personality_per_drug_graph', 'figure'),
    Input('dropdown-drug', 'value')
)
def personality_per_drug_graph(drug):
    return pc.get_plot(personality_per_drug_df, drug)


@callback(
    Output('personality_per_drug_legend', 'children'),
    Input('dropdown-drug', 'value')
)
def personality_per_drug_legend(drug):
    return pc.get_legend(drug)


@callback(
    Output('drug_consumption_graph', 'figure'),
    Input('dropdown-drug', 'value')
)
def drug_consumption_graph(drug):
    return sb.get_plot(consumption_per_drug_df, drug)


@callback(
    Output('drug_consumption_legend', 'children'),
    Input('dropdown-drug', 'value')
)
def drug_consumption_legend(drug):
    return sb.get_legend(drug)


@callback(
    Output('jointly-consumed-drugs', 'children'),
    Input('dropdown-drug', 'value')
)
def jointly_consumed_drugs(drug):
    if drug is not None:
        return [
            html.H2('Drogues consommées conjointement'),
            html.Div(id='chord-diagram-container', children=[
                dcc.Graph(figure=cd.create_chord_diagram(drug_corr_df, drug)),
                html.Div(id='chord-diagram',
                         children=cd.create_legend(drug, drug_corr_df)),
            ]),
        ]


@callback(
    Output('warning', 'children'),
    Input('dropdown-drug', 'value')
)
def warning(drug):
    if drug is not None and drug in GATEWAY_DRUGS:
        return html.Div([
            html.P("Attention : Ceci s'agit d'une drogue passerelle!",
                   style={'font-weight': 'bold', 'text-align': 'center'}),
            html.Div(
                # Use the same class as you have styled or a new one for specific styling
                className='icon-container',
                children=[
                    html.Img(src="/assets/icons/gateway-drugs.png",
                             style={'height': '80px', 'margin': 'auto', 'display': 'block'})
                ]
            ),
        ], style={'text-align': 'center', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})
    # This ensures that no residual content is displayed when the drug is not a gateway drug
    return html.Div()


def print_education(raw_education_level: str) -> str:
    """
    Print the education level in a more readable format.
    :param: raw_education_level: The education level to print.
    :return: The education level in a more readable format.
    """
    raw_education_level = raw_education_level.lower()
    if raw_education_level[0] in ['q', 'f']:
        return f"...avoir {raw_education_level}."
    else:
        return f"...avoir une {raw_education_level}."


@callback(
    Output('typical-person', 'children'),
    Input('dropdown-drug', 'value')
)
def typical_person(drug):
    if drug is not None:
        profile = profiles_df[profiles_df['drug'] == drug].iloc[0]
        print(profile)
        return [
            html.P('Les consommateurs de cette drogue ont tendance à...'),
            html.Div(
                className='icons-container',
                children=[
                    html.Div(
                        className='icon-container',
                        children=[
                            html.Img(src=EDUCATION_IMAGE_PATHS.get(
                                profile['most_common_education'], '/assets/icons/gateway-drugs.png')),
                            html.Label('Formation'),
                            html.P(print_education(
                                profile['most_common_education']))
                        ]
                    ),
                    html.Div(
                        className='icon-container',
                        children=[
                            html.Img(src=AGE_IMAGE_PATHS.get(
                                profile['most_common_age'], '/assets/icons/gateway-drugs.png')),
                            html.Label('Âge'),
                            html.P(
                                f"...être âgé.e entre {profile['most_common_age']}.")
                        ]
                    ),
                    html.Div(
                        className='icon-container',
                        children=[
                            html.Img(src=GENDER_IMAGE_PATHS.get(
                                profile['most_common_gender'], '/assets/gateway-drugs.png')),
                            html.Label('Genre'),
                            html.P(
                                f"...être un.e {profile['most_common_gender'].lower()}.")
                        ]
                    )
                ]
            )
        ]
