import dash
from dash import dcc, html
import plotly.graph_objects as go
from ucimlrepo import fetch_ucirepo
import src.preprocess as preprocess
import sys
from pathlib import Path

base_path = Path(__file__).resolve().parent.parent
sys.path.append(str(base_path))

app = dash.Dash(__name__)

dataframe = fetch_ucirepo(id=373).data.original
dataframe = preprocess.drop_columns(dataframe)
dataframe = preprocess.fix_errors(dataframe)
drug_corr_df = preprocess.drug_correlation(dataframe)

active_palette = ['#81d4fa', '#29b6f6', '#039be5',
                  '#0288d1', '#0277bd', '#01579b', '#004ba0']

french_drug_names = {
    'nicotine': 'Nicotine',
    'vsa': 'Solvants volatils',
    'alcohol': 'Alcool',
    'amphet': 'Amphétamines',
    'amyl': 'Amyl nitrite',
    'benzos': 'Benzodiazépines',
    'cannabis': 'Cannabis',
    'coke': 'Cocaïne',
    'crack': 'Crack',
    'ecstasy': 'Ecstasy',
    'ketamine': 'Kétamine',
    'legalh': 'Drogues légales',
    'lsd': 'LSD',
    'meth': 'Méthamphétamines',
    'mushrooms': 'Champignons magiques',
    'heroin': 'Héroïne',
}


def activate_drug_palette(df, drug, active_palette):
    colors = {}
    weights = df['weight'].astype(float)
    max_weight = weights.max()
    for index, row in df.iterrows():
        is_active = drug in (row['source'], row['target'])
        if is_active:
            weight_normalized = row['weight'] / max_weight
            color_index = int(weight_normalized * (len(active_palette) - 1))
            colors[index] = active_palette[color_index]
    return colors


def create_legend(active_drug, df, active_palette):
    legend_categories = determine_legend_categories(
        df, active_drug, active_palette)
    legend_texts = ["Extrêmement faible", "Très faible", "Faible",
                    "Moyenne", "Élevée", "Très élevée", "Extrêmement élevée"]

    # Generating the legend as a list of html.Li components
    legend_items = [html.Li(style={'color': active_palette[i]}, children=legend_texts[i])
                    for i in legend_categories]

    # Wrapping the items in a ul and div structure
    legend_component = html.Div([
        html.H3("Indice de consommation conjointe", style={
                'textAlign': 'center', 'textDecoration': 'underline'}),
        html.Ul(legend_items, style={
                'listStyleType': 'none', 'padding': '0', 'textAlign': 'center', 'fontWeight': 'bold'})
    ], style={'border': '5px groove #000', 'borderRadius': '1.5%', 'padding': '1.5%', 'marginTop': '0', 'backgroundColor': 'rgba(0, 0, 0, 0.02)'})

    return legend_component


def create_chord_diagram(df, active_drug):
    drugs = sorted(set(df['source'].unique()) | set(df['target'].unique()))
    n = len(drugs)

    connected_drugs = df[df['source'] == active_drug]['target'].tolist(
    ) + df[df['target'] == active_drug]['source'].tolist()

    drug_indices = {drug: idx for idx, drug in enumerate(drugs)}
    df['weight'] = df['weight'].astype(
        float) / df['weight'].astype(float).max() * 10

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[1] * 360,
        theta=list(range(360)),
        mode='lines',
        line=dict(color='black', width=2),
        hoverinfo='none',
    ))

    colors = activate_drug_palette(df, active_drug, active_palette)

    for i, row in df.iterrows():
        source_idx = drug_indices[row['source']]
        target_idx = drug_indices[row['target']]
        is_active_connection = active_drug in [row['source'], row['target']]
        if is_active_connection:
            fig.add_trace(go.Scatterpolar(
                r=[1, 1, None],
                theta=[source_idx / n * 360, target_idx / n * 360, None],
                mode='lines',
                line=dict(color=colors[i],
                          width=row['weight'], shape='spline'),
                name='',
                hoverinfo='none',
            ))

    # Filters for connected drugs only
    connected_drugs = set(df[df['source'] == active_drug]['target'].tolist()) | set(
        df[df['target'] == active_drug]['source'].tolist()) | {active_drug}

    # Update drug_indices to include only connected drugs
    drug_indices = {drug: idx for idx,
                    drug in enumerate(sorted(connected_drugs))}
    n = len(drug_indices)  # Update 'n' based on connected drugs

    # Update the tick values and text for the angular axis
    tickvals = [idx * 360 / n for idx,
                drug in enumerate(sorted(connected_drugs))]
    ticktext = [french_drug_names.get(drug, drug)
                for drug in sorted(connected_drugs)]

    fig.update_layout(
        title={
            'text': "Drogues consommées conjointement",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        polar=dict(
            radialaxis=dict(visible=False),
            angularaxis=dict(
                visible=True,
                tickmode='array',
                tickvals=tickvals,
                ticktext=ticktext,
                rotation=90,
                direction='clockwise',
                tickfont=dict(size=12),
            ),
            bgcolor='white'
        ),
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(l=70, r=70, t=100, b=70)
    )

    return fig


active_drug = 'alcohol'
fig = create_chord_diagram(drug_corr_df, active_drug)

max_weight = drug_corr_df['weight'].max()

# Function to determine the legend categories to include based on active connections


def determine_legend_categories(df, active_drug, active_palette):
    connection_weights = df[(df['source'] == active_drug) | (
        df['target'] == active_drug)]['weight']
    normalized_weights = connection_weights / max_weight
    categories_present = set()
    for weight in normalized_weights:
        color_index = int(weight * (len(active_palette) - 1))
        categories_present.add(color_index)
    return sorted(categories_present)


legend_categories = determine_legend_categories(
    drug_corr_df, active_drug, active_palette)
legend_texts = ["Extrêmement faible", "Très faible", "Faible",
                "Moyenne", "Élevée", "Très élevée", "Extrêmement élevée"]

# Create the legend HTML dynamically based on the categories present
legend = html.Div([
    html.H3("Indice de consommation conjointe", style={
            'textAlign': 'center', 'textDecoration': 'underline'}),
    html.Ul([html.Li(style={'color': active_palette[i]}, children=legend_texts[i])
             for i in legend_categories], style={'listStyleType': 'none', 'padding': '0', 'textAlign': 'center', 'fontWeight': 'bold'})
], style={'border': '5px groove #000', 'borderRadius': '1.5%', 'padding': '1.5%', 'marginTop': '0', 'backgroundColor': 'rgba(0, 0, 0, 0.02)'})

# Ajouter la légende à la mise en page de l'application, à droite du graphique
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Graph(figure=fig,
                  style={'display': 'flex'},
                  config={'staticPlot': True}),
        html.Div(legend, style={'display': 'flex',
                 'verticalAlign': 'top'})
    ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'justifyContent': 'space-evenly'})
])
if __name__ == '__main__':
    app.run_server(debug=True)
