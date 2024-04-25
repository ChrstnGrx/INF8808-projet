from dash import html
import plotly.graph_objects as go
from src.utils.colors import CHORD_PALETTE
from src.utils.conversions import FRENCH_DRUG_NAMES
import math


def get_legend(drug_corr_df, drug):
    legend = create_legend(drug, drug_corr_df, CHORD_PALETTE)
    return legend

def get_plot(drug_corr_df, drug):
    fig = create_chord_diagram(drug_corr_df, drug)
    return fig

def activate_drug_palette(df, drug):
    """
    Activates the color palette for a given drug.

    Args:
        df: DataFrame containing drug correlation data.
        drug: Name of the drug.

    Returns:
        colors: Dictionary containing the indices of activated colors for drug connections.
    """
    colors = {}
    weights = df['weight'].astype(float)
    max_weight = weights.max()
    for index, row in df.iterrows():
        is_active = drug in (row['source'], row['target'])
        if is_active:
            weight_normalized = row['weight'] / max_weight
            color_index = int(weight_normalized * (len(CHORD_PALETTE) - 1))
            colors[index] = CHORD_PALETTE[color_index]
    return colors

def create_legend(active_drug, df):
    """
    Creates the legend for the chord correlation diagram.

    Args:
        active_drug: The active drug.
        df: DataFrame containing the drug correlation data.

    Returns:
        legend_component: HTML component representing the legend.
    """
    legend_categories = determine_legend_categories(
        df, active_drug, CHORD_PALETTE)
    legend_texts = ["Extrêmement faible", "Très faible", "Faible",
                    "Moyenne", "Élevée", "Très élevée", "Extrêmement élevée"]

    # Génération de la légende sous forme de liste de composants html.Li
    legend_items = [html.Li(style={'color': CHORD_PALETTE[i]}, children=legend_texts[i])
                    for i in legend_categories]
    
    # Envelopper les éléments dans une structure ul et div
    legend_component = html.Div([
        html.H4("Indice de consommation conjointe", style={
                'fontFamily': 'Oswald, sans-serif', 'fontSize': '1.35em', 'textAlign': 'center', 'textDecoration': 'underline'}),
        html.Ul(legend_items, style={
                'listStyleType': 'none', 'padding': '0', 'textAlign': 'center', 'fontWeight': 'bold'})
    ], style={'border': '3px solid black', 'padding': '1.5%', 'marginTop': '0', 'marginRight': '30%', 'marginLeft': '30%', 'backgroundColor': 'rgba(0, 0, 0, 0.02)'})

    return legend_component

def create_chord_diagram(df, active_drug):
    """
    Creates the correlation chord diagram.

    Args:
        df: DataFrame containing the drug correlation data.
        active_drug: Name of the active drug.

    Returns:
        fig: Chord diagram.
    """
    # Retrieve the list of unique drugs
    drugs = sorted(set(df['source'].unique()) | set(df['target'].unique()))
    n = len(drugs)

    # List of drugs connected to the active drug
    connected_drugs = df[df['source'] == active_drug]['target'].tolist(
    ) + df[df['target'] == active_drug]['source'].tolist()

    # Assign an index to each drug
    drug_indices = {drug: idx for idx, drug in enumerate(drugs)}

    # Normalize weights and adjust the scale
    df['weight'] = df['weight'].astype(
        float) / df['weight'].astype(float).max() * 10

    fig = go.Figure()

    # Add a base circle
    fig.add_trace(go.Scatterpolar(
        r=[1] * 360,
        theta=list(range(360)),
        mode='lines',
        line=dict(color='black', width=2),
        hoverinfo='none',
    ))

    colors = activate_drug_palette(df, active_drug)

    # Add connections with their respective weights
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

    # Filters for only connected drugs
    connected_drugs = set(df[df['source'] == active_drug]['target'].tolist()) | set(
        df[df['target'] == active_drug]['source'].tolist()) | {active_drug}

    # Update drug_indices to include only connected drugs
    drug_indices = {drug: idx for idx,
                    drug in enumerate(sorted(connected_drugs))}
    n = len(drug_indices)  # Mise à jour de 'n' en fonction des drogues connectées
    
    # Update values and text for angular axis markers
    tickvals = [idx * 360 / n for idx,
                drug in enumerate(sorted(connected_drugs))]
    ticktext = [FRENCH_DRUG_NAMES.get(drug, drug)
                for drug in sorted(connected_drugs)]

    fig.update_layout(
        title={
            'text': "",
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

def determine_legend_categories(df, active_drug, CHORD_PALETTE):
    """
    Determines legend categories based on connection weights.

    Args:
        df: DataFrame containing drug correlation data.
        active_drug: Name of the active drug.
        active_palette: Active color palette.

    Returns:
        categories_present: Set of present legend categories.
    """
    connection_weights = df[(df['source'] == active_drug) | (
        df['target'] == active_drug)]['weight']
    normalized_weights = connection_weights / df['weight'].max()
    categories_present = set()
    for weight in normalized_weights:
        if not math.isnan(weight):
            color_index = int(weight * (len(CHORD_PALETTE) - 1))
            categories_present.add(color_index)
    return sorted(categories_present)
