import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output

from src.datasets.dataframe import personality_per_drug_df, consumption_per_drug_df
from src.utils.constants import DRUG_INFO

import src.utils.graphs.parallel_coords as pc
import src.utils.graphs.stacked_bar as sb

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
    html.Div(
        id='personality_per_drug', 
        className='chart-container',
        children=[
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


