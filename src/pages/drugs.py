import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output

from src.datasets.dataframe import personality_per_drug_df
from src.utils.constants import DRUG_INFO

import src.utils.graphs.parallel_coords as pc

dash.register_page(
    __name__, 
    path='/',
    redirect_from=['/drugs'],
    title='Drugs Analysis',)

drug_options = [{'label': DRUG_INFO[drug]['french'].capitalize(), 'value': drug} for drug in DRUG_INFO]

layout = html.Div([
    dcc.Dropdown(
        id='dropdown-drug',
        options=drug_options,  # Assuming this is defined somewhere in your code
        placeholder="Sélectionnez une drogue ...",
    ),
    html.Div([
        dcc.Graph(
            id='personality_per_drug_graph',
            figure=pc.get_plot(personality_per_drug_df), 
        ),
        html.Div(
            id='personality_per_drug_legend',
            children=pc.get_legend()
        )
    ]),
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

