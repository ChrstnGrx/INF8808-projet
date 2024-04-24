'''
    Contains functions to create the clustered barcharts.
'''
import plotly.express as px
import src.utils.constants as constants

import sys
from pathlib import Path

base_path = Path(__file__).resolve().parent.parent
sys.path.append(str(base_path))


def cluster_by_age(data_frame, colors):
    result_df = data_frame

    # Créer le graphique en barres groupées
    fig = px.bar(result_df, x='drug', y=result_df.columns[1:],
                 barmode='group',
                 labels={'drug': 'Drogue', 'value': 'Portion de consommateurs', 'variable': 'Groupe d\'âge'})

    fig.update_yaxes(tickformat=",.0%",
                     title_text="Portion de consommateurs (%)")

    fig.update_layout(legend_title_text='Tranches d\'âge')

    for i, trace in enumerate(fig.data):
        trace.hovertemplate = f'<b>Tranche d\'âge:</b> {trace["legendgroup"]}<br><b>Drogue:</b> %{{x}}<br><b>Portion de consommateurs:</b> %{{y:.2%}}<extra></extra>'

    fig.update_xaxes(tickangle=45)

    # Apply colors to the bars
    for i in range(len(colors)):
        fig.data[i].marker.color = colors[i]

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background for the plot area
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background for the paper area
    )    

    # Appliquer les couleurs aux barres du graphique
    for i in range(len(colors)):  # Boucler sur les trois barres de chaque cluster
        fig.data[i].marker.color = colors[i]

    return fig


def cluster_by_education(df, colors):
    result_df = df

    french_drugs = []
    for key, value in constants.DRUG_INFO.items():
        french_drugs.append(value['french'])
    result_df['drug'] = french_drugs

    fig = px.bar(result_df, x='drug', y=result_df.columns[1:],
                 barmode='group',
                 labels={'drug': 'Drogue', 'value': 'Portion de consommateurs', 'variable': 'Niveau d\'éducation'})

    fig.update_yaxes(tickformat=",.0%",
                     title_text="Portion de consommateurs (%)")
    fig.update_layout(legend_title_text='Niveau d\'éducation')

    for i, trace in enumerate(fig.data):
        trace.hovertemplate = f'<b>Niveau d\'éducation:</b> {trace["legendgroup"]}<br><b>Drogue:</b> %{{x}}<br><b>Portion de consommateurs:</b> %{{y:.2%}}<extra></extra>'

    fig.update_xaxes(tickangle=45)

    # Apply colors to the bars
    for i in range(len(colors)):
        fig.data[i].marker.color = colors[i]

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background for the plot area
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background for the paper area
    ) 
    
    # Appliquer les couleurs aux barres du graphique
    for i in range(len(colors)):  # Boucler sur les barres de chaque cluster
        fig.data[i].marker.color = colors[i]

    return fig
