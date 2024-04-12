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
    path='/',
    redirect_from=['/drugs'],
    title='Drugs Analysis',)

drug_options = [{'label': DRUG_INFO[drug]['french'].capitalize(), 'value': drug} for drug in DRUG_INFO]

layout = html.Div(id='drugs-page', children=[
    dcc.Dropdown(
        id='dropdown-drug',
        options=drug_options,
        placeholder="Sélectionnez une drogue.",
    ),
    html.Div(id='warning'),
    html.Div(id='typical-person'),
    html.Div(
        id='personality_per_drug', 
        className='chart-container',
        children=[
            html.H1('Tendances pour chaque trait de personnalité selon la drogue consommée'),
            dcc.Graph(
                id='personality_per_drug_graph',
                className='chart',
                figure=pc.get_plot(personality_per_drug_df), 
            ),
            html.Div(
                id='personality_per_drug_legend',
                className='legend',
                children=pc.get_legend()
            )
        ]
    ),
    html.Div(
        id='drug_consumption', 
        className='chart-container',
        children=[
            html.H1('Fréquences de consommations pour chaque drogue'),
            dcc.Graph(
                id='drug_consumption_graph',
                className='chart',
                figure=sb.get_plot(consumption_per_drug_df), 
            ),
            html.Div(
                id='drug_consumption_legend',
                className='legend',
                children=sb.get_legend()
            )
        ]
    ),
    html.Div(id='jointly-consumed-drugs', className='chart-container'),

])

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
    if drug is not None :
        return [
            html.H1('Drogues consommees conjointement'),
            html.Div(id='chord-diagram-container', children=[
                    dcc.Graph(figure=cd.create_chord_diagram(drug_corr_df, drug)),
                    html.Div(id='chord-diagram', children=cd.create_legend(drug, drug_corr_df)),
                ]),
        ]

