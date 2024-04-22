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
                barmode='group', title='Portion de consommateurs de chaque drogue pour différentes tranches d\'âge',
                labels={'drug': 'Drogue', 'value': 'Portion de consommateurs', 'variable': 'Groupe d\'âge'})
    
    fig.update_yaxes(tickformat=",.0%", title_text="Portion de consommateurs (%)")

    # Définir les couleurs pour chaque barre dans un cluster
    # colors = ['lightgray', '#29b6f6', 'darkgray']  # Couleurs pour les barres de gauche, milieu et droite

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
                barmode='group', title='Portion de consommateurs de chaque drogue pour différentes niveaux d\'éducation',
                labels={'drug': 'Drogue', 'value': 'Portion de consommateurs', 'variable': 'Niveau d\'éducation'})
    
    fig.update_yaxes(tickformat=",.0%", title_text="Portion de consommateurs (%)")

    # Appliquer les couleurs aux barres du graphique
    for i in range(len(colors)):  # Boucler sur les barres de chaque cluster
        fig.data[i].marker.color = colors[i]

    return fig
