"""
    This module contains the content of the first page.
"""
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output

from src.datasets.dataframe import drug_corr_df, personality_per_drug_df, consumption_per_drug_df, profiles_df
from src.utils.constants import DRUG_INFO, GATEWAY_DRUGS, AGE_IMAGE_PATHS, GENDER_IMAGE_PATHS, EDUCATION_IMAGE_PATHS

import src.utils.graphs.parallel_coords as pc
import src.utils.graphs.stacked_bar as sb
import src.utils.graphs.chord_diagram as cd

# Registering the path for nav buttons
dash.register_page(
    __name__,
    path='/',
    redirect_from=['/drugs'],
    title='Analyse des drogues',)

drug_options = [{'label': DRUG_INFO[drug]['french'].capitalize(), 'value': drug}
                for drug in DRUG_INFO]

layout = html.Div(id='drugs-page', children=[
    html.Div(id='header', children=[
        html.Div(id='nav', children=[
            html.Button('Quel est mon risque?', id='forward-button', n_clicks=0),
        ]),
        html.H1('Prévention des drogues'),
    ]),
    html.Div(className='page-content', children=[
        html.P("La consommation de drogues est une problématique majeure qui intéresse un large éventail de personnes et d'organisation. Par ce fait, une analyse sur la consommation de drogues est cruciale pour justifier et cibler les efforts de prévention et de sensibilisation. L'objectif principal de cette étude consiste à identifier et à faire ressortir les principaux facteurs liés à la consommation de drogues grâce à l'analyse approfondie d'un riche ensemble de données regroupant des informations sur 1885 individus, leurs personnalités, leurs antécédents sociodémographiques et leurs habitudes de consommation de 18 substances psychoactives différentes. Grâce à cette recherche, nous visons à apporter des éléments probants susceptibles d'orienter les efforts de prévention et d'éducation en matière de mauvaise utilisation de substances psychoactives."),
        html.P("Plus précisement, cette page sert à décrire le profil typique d'une personne consommant une drogue spécifique et ses habitudes de consommation."),
        dcc.Dropdown(
            id='dropdown-drug',
            options=drug_options,
            placeholder="Veuillez sélectionner une drogue...",
        ),
        html.Div(className='disclaimer', children=["N.B. Si aucune drogue n'est sélectionnée, les graphiques affichent les informations générales pour toutes les drogues. Les graphiques qui n'ont pas de vue générale sont cachés."]),
        html.Div(id='warning'),
        html.H2('Qui en sont les consommateurs ?'),
        html.P("D'une part, il est important de connaître les consommateurs typiques de chaque drogue. Ainsi, les intervenants peuvent cibler les groupes les plus à risque selon les drogues visées et mieux reconnaître les risques associés."),
        html.Div(id='profile'),
        html.Div(
            id='personality_per_drug',
            className='chart-container',
            children=[
                html.H3(
                    'Tendances pour chaque trait de personnalité selon la drogue consommée'),
                html.P("Chaque drogue a tendance à intéresser des types de personnalité différentes. Voici donc un graphique qui montre l'écart entre la moyenne de chaque personnalité et sa valeur normale (0), pour chaque drogue."),
                dcc.Graph(
                    id='personality_per_drug_graph',
                    className='chart',
                    figure=pc.get_plot(personality_per_drug_df),
                ),
                html.Div(className='legend-wrapper', children=[
                    html.H4("Légende"),
                    html.Div(
                        id='personality_per_drug_legend',
                        className='legend',
                        children=pc.get_legend()
                    )
                ]),
                html.P("On voit des tendances générales qui démontrent que, peu importe la drogue, les consommateurs sont souvent plus neurotiques, plus ouverts, moins agréables, moins consciencieux, plus impulsifs et plus à la recherche de sensations. Ce sont donc ces traits qui doivent être surveillés lors de la prévention. En effet, les consommateurs d'aucune drogue (répondants sobres) ont souvent des traits de personalité opposés. Cependant, les traits de personalité des consommateurs d'alcool se situent toujours autour de la valeur normale (0). ")
            ]
        ),
        html.H2('Quelles sont les habitudes de consommation?'),
        html.P('D\'autre part, il est important de connaître comment les drogues sont consommées. Cela peut aider les intervenants à comprendre la gravité de la consommation.'),
        html.Div(
            id='drug_consumption',
            className='chart-container',
            children=[
                html.H3('Fréquences de consommation pour chaque drogue'),
                html.P('La fréquence de consommation est une des mesures les plus importantes pour évaluer la gravité de la consommation. Ce graphique montre donc, pour l\'échantillon donné, quelles drogues ont tendances à être utilisées plus fréquement.'),
                html.P('Il est possibler de sélectionner une zone dans le graphique pour aggrandir les détails.'),
                dcc.Graph(
                    id='drug_consumption_graph',
                    className='chart',
                    figure=sb.get_plot(consumption_per_drug_df),
                ),
                html.Div(id='legend-drug-consumption', className='legend-wrapper', children=[
                    html.H4("Légende"),
                    html.Div(
                        id='drug_consumption_legend',
                        className='legend',
                        children=sb.get_legend()
                    )
                ]),
                html.P('On voit que l\'alcool est la drogue la plus consommée, suivie par le cannabis et la nicotine. Les autres drogues sont consommées beaucoup moins fréquemment.'),
            ]
        ),
        html.Div(id='jointly-consumed-drugs', className='chart-container'),
    ])
    
])

@callback(
    Output('url-forward', 'pathname'),
    Input('forward-button', 'n_clicks'),
    prevent_initial_call=True
)
def navigate_to_demographics(n_clicks):
    if n_clicks > 0:
        return '/demographics'

@callback(
    Output('profile', 'children'),
    Input('dropdown-drug', 'value')
)
def profile(drug):
    if drug is not None:
        return [
            html.H3('Profil susceptible'),
            html.P("En regardant les données des répondants, on s'apperçoit que certains groupes sont disproportionément représentés dans les consommateurs de certaines drogues spécifiques. Afin de compenser les biais liés à l'échantillonnage et de trouver un profil significatif, la normalisation des données a été effectuée en calculant la proportion de consommateurs pour chaque substance et chaque catégorie démographique (sexe, tranche d'âge, et niveau d'éducation). Cette méthode permet de déterminer les caractéristiques typiques des personnes les plus susceptibles de consommer une drogue spécifique, fournissant ainsi une base solide pour élaborer des stratégies de prévention ciblées. Voici donc les caractéristiques d'une personnes qui est le plus susceptible de consommer la drogue sélectionnée."),
            html.Div(className='viz', children=[
                html.Div(id='typical-person', children=typical_person(drug)),
            ]),
        ]
    return html.Div()

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
            html.H3('Drogues consommées conjointement'),
            html.P('Une autre mesure important à connaître sont les relations entre les différentes drogues. En effet, certaines drogues sont souvent consommées ensemble, ce qui peut indiquer des comportements à risque. Le graphique ci-dessous montre donc la corrélation entre la consommation de la drogues sélectionnées avec les autres drogues, c\'est à dire combien de répondant ont consommé à la fois les deux drogues comparées.'),
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
    # This ensures that no residual content is displayed when the drug is not a gateway drug
    if drug is not None and drug in GATEWAY_DRUGS:
        return html.Div([
            html.P("Attention : Ceci s'agit d'une drogue passerelle!",
                   className='warning-text'),
            html.Div(
                className='icon-container',
                children=[
                    html.Img(id='gateway-warning-icon',
                             src="/assets/icons/gateway-drugs.png")
                ]
            ),
            html.P('Cela signifie que cette drogue a tendance à être dans les premières essayées. Il est donc important de sensibiliser à ses dangers.', 
                   id='gateway-warning-description'),
        ], id='gateway-warning-container')
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

def typical_person(drug):
    if drug is not None:
        profile = profiles_df[profiles_df['drug'] == drug].iloc[0]
        return [
            html.P('Les consommateurs de cette drogue ont tendance à...',
                          className='typical-person-description'),
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
                                profile['most_common_education']),
                                          className='typical-person-description')
                        ]
                    ),
                    html.Div(
                        className='icon-container',
                        children=[
                            html.Img(src=AGE_IMAGE_PATHS.get(
                                profile['most_common_age'], '/assets/icons/gateway-drugs.png')),
                            html.Label('Âge'),
                            html.P(f"...être âgés entre {profile['most_common_age']}.",
                                          className='typical-person-description')
                        ]
                    ),
                    html.Div(
                        className='icon-container',
                        children=[
                            html.Img(src=GENDER_IMAGE_PATHS.get(
                                profile['most_common_gender'], '/assets/gateway-drugs.png')),
                            html.Label('Genre'),
                            html.P(f"...être un.e {profile['most_common_gender'].lower()}.",
                                          className='typical-person-description')
                        ]
                    )
                ]
            )
        ]
