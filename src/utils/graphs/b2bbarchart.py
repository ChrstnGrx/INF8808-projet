'''
    Contains some functions related to the creation of the horizontal back to back barchart.
'''
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd


def draw_b2b_barchart(dataframe, gender):
    '''
        Creates the horizontal back to back barchart.

        Args:
            dataframe: The dataframe to use to create the barchart

        Returns:
            The barchart figure
    '''
    men_bars = dataframe[['variable', 'Homme']].rename(
        columns={'Homme': 'H_Value'})
    women_bars = dataframe[['variable', 'Femme']].rename(
        columns={'Femme': 'F_Value'})

    # Create a dataframe for right side bars
    # Create individual bar charts for women and men
    fig_men = px.bar(men_bars, x='H_Value', y='variable',
                     orientation='h', text='H_Value', color='H_Value', title='Homme')
    fig_women = px.bar(women_bars, x='F_Value', y='variable',
                       orientation='h', text='F_Value', color='F_Value', title='Femme')

    fig_men.update_traces(marker=dict(color='#29b6f6'), showlegend=False)
    fig_women.update_traces(marker=dict(color='#424242'), showlegend=False)
    # Update figure traces for each chart
    if (gender != "MAN"):
        fig_men.update_traces(marker=dict(color='#424242'), showlegend=False)
        fig_women.update_traces(marker=dict(color='#29b6f6'), showlegend=False)

    # Combine the two figures using subplots
    fig = make_subplots(specs=[[{"secondary_y": True}, {}]], rows=1, cols=2, subplot_titles=(
        'Homme', 'Femme'), shared_yaxes=True)

    # Add the individual figures to the subplot grid
    fig.add_trace(fig_men['data'][0], row=1, col=1,  secondary_y=True)
    fig.add_trace(fig_women['data'][0], row=1, col=2)
    fig.update_layout(showlegend=False, xaxis_autorange='reversed')
    return fig
