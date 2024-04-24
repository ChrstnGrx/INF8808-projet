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
    men_bars = dataframe[['variable', 'Homme']]
    women_bars = dataframe[['variable', 'Femme']]
    print(men_bars)

    # Create a dataframe for right side bars
    # Create individual bar charts for women and men
    fig_men = px.bar(men_bars, x='Homme', y='variable', orientation='h', text='Homme', color_discrete_sequence =['#29b6f6']*len(men_bars), title='Homme', template='plotly_white')
    fig_women = px.bar(women_bars, x='Femme', y='variable', orientation='h', text='Femme', color_discrete_sequence =['#424242']*len(women_bars), title='Femme', template='plotly_white')

    fig_men.update_traces(textposition='outside')
    fig_women.update_traces(textposition='outside')
    # # Update figure traces for each chart
    if (gender != "MAN"):
        fig_men.update_traces(marker=dict(color='#424242'), showlegend=False)
        fig_women.update_traces(marker=dict(color='#29b6f6'), showlegend=False)

    # # Combine the two figures using subplots
    fig = make_subplots(specs=[[{"secondary_y": True}, {}]], rows=1, cols=2, subplot_titles=('Homme', 'Femme'), shared_yaxes=True)

    # # Add the individual figures to the subplot grid
    fig.add_trace(fig_men['data'][0], row=1, col=1,  secondary_y=True)
    fig.add_trace(fig_women['data'][0], row=1, col=2)
    fig.update_layout(showlegend=False, xaxis_autorange='reversed')

    # # Update the subplot layout  
    fig.update_layout( showlegend=False, xaxis_range=[max(list(men_bars['Homme']))+5,0],plot_bgcolor = "white",height=700, xaxis2=dict(range=[0, max(list(women_bars['Femme']))+5]))
    fig.update_xaxes(
    mirror=True,
    ticks='outside',
    showline=True,
    gridcolor='lightgrey'
)

    print(fig.layout)
    # Show the combined figure
    for i, trace in enumerate(fig.data):
        trace.hovertemplate = f'<b>Drogue:</b> %{{y}}<br><b>Portion:</b> %{{x}}%<extra></extra>'
        
    return fig
