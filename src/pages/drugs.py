import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output

from src.datasets.dataframe import drug_corr_df, personality_per_drug_df, consumption_per_drug_df
from src.utils.constants import DRUG_INFO, GATEWAY_DRUGS

import src.utils.graphs.parallel_coords as pc
import src.utils.graphs.stacked_bar as sb
import src.utils.graphs.chord_diagram as cd

dash.register_page(
    __name__,
    path='/drugs',
    title='Analyse des drogues',)

drug_options = [{'label': DRUG_INFO[drug]['french'].capitalize(), 'value': drug}
                for drug in DRUG_INFO]

layout = html.Div(id='drugs-page', children=[
    html.Div(id='header', children=[
        html.Div(id='nav', children=[
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
        return html.P('Attention : Ceci s\'agit d\'une drogue passerelle!')


@callback(
    Output('typical-person', 'children'),
    Input('dropdown-drug', 'value')
)
def typical_person(drug):
    if drug is not None:
        return [
            html.P('Les consommateurs de cette drogue ont tendance à...'),
            html.Div(
                className='icons-container',
                children=[
                    html.Div(
                        className='icon-container',
                        children=[
                            html.Img(
                                src='/assets/icons/graduate-cap-solid.svg'),
                            html.Label('Formation'),
                            html.P('... avoir complété un baccalauréat.')
                        ]
                    ),
                    html.Div(
                        className='icon-container',
                        children=[
                            html.Img(src='/assets/icons/diploma.svg'),
                            html.Label('Âge'),
                            html.P('...être âgé entre 45 et 55 ans.')
                        ]
                    ),
                    html.Div(
                        className='icon-container',
                        children=[
                            html.Img(src='/assets/icons/man.svg'),
                            html.Label('Genre'),
                            html.P('...être un homme.')
                        ]
                    )
                ]
            )
        ]
