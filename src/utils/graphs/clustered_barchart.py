'''
    Contains functions to create the clustered barcharts.
'''
import plotly.express as px

import sys
from pathlib import Path

base_path = Path(__file__).resolve().parent.parent
sys.path.append(str(base_path))


def cluster_by_age(df, colors):
    # Create clustered barchart
    fig = px.bar(df, x='drug', y=df.columns[1:],
                 barmode='group',
                 labels={'drug': 'Drogue', 'value': 'Portion de consommateurs', 'variable': 'Groupe d\'âge'})

    fig.update_yaxes(tickformat=",.0%",
                     title_text="Proportion de consommateurs (%)")

    fig.update_layout(legend_title_text='Tranches d\'âge')

    for i, trace in enumerate(fig.data):
        trace.hovertemplate = f'<b>Tranche d\'âge:</b> {trace["legendgroup"]}<br><b>Drogue:</b> %{{x}}<br><b>Portion de consommateurs:</b> %{{y:.2%}}<extra></extra>'

    fig.update_xaxes(tickangle=45)

    # Apply colors to the bars
    for i in range(len(colors)):
        fig.data[i].marker.color = colors[i]

    # White background
    fig.update_layout(template='plotly_white')

    fig.update_layout(
        legend_traceorder="reversed",
        legend_yanchor="middle",
        legend_y=0.5
    )

    return fig


def cluster_by_education(df, colors):
    fig = px.bar(df, x='drug', y=df.columns[1:],
                 barmode='group',
                 labels={'drug': 'Drogue', 'value': 'Portion de consommateurs', 'variable': 'Niveau d\'éducation'})

    fig.update_yaxes(tickformat=",.0%",
                     title_text="Proportion de consommateurs (%)")
    fig.update_layout(legend_title_text='Niveau d\'éducation')

    for i, trace in enumerate(fig.data):
        trace.hovertemplate = f'<b>Niveau d\'éducation:</b> {trace["legendgroup"]}<br><b>Drogue:</b> %{{x}}<br><b>Portion de consommateurs:</b> %{{y:.2%}}<extra></extra>'

    fig.update_xaxes(tickangle=45)

    # Apply colors to the bars
    for i in range(len(colors)):
        fig.data[i].marker.color = colors[i]

    # White background
    fig.update_layout(template='plotly_white')

    fig.update_layout(
        legend_traceorder="reversed",
        legend_yanchor="middle",
        legend_y=0.5
    )

    return fig
