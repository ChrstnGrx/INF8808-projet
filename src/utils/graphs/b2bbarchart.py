import plotly.express as px
from plotly.subplots import make_subplots

def draw_b2b_barchart(dataframe, gender):
    """
    Creates a back-to-back horizontal bar chart.

    Args:
        dataframe: The dataframe to use for creating the bar chart.
        gender: The gender for which to create the chart ("MAN" for male, any other value for female).

    Returns:
        The figure of the bar chart.
    """

    # Adding text columns for percentages
    dataframe['homme_text'] = dataframe['Homme'].astype(str) + "%"
    dataframe['femme_text'] = dataframe['Femme'].astype(str) + "%"

    # Selecting data for men and women
    men_bars = dataframe[['variable', 'Homme', 'homme_text']]
    women_bars = dataframe[['variable', 'Femme', 'femme_text']]

    # Creating individual bar charts for men and women
    fig_men = px.bar(men_bars, x='Homme', y='variable', orientation='h', text='homme_text', color_discrete_sequence =['#29b6f6']*len(men_bars), title='Homme', template='plotly_white')
    fig_women = px.bar(women_bars, x='Femme', y='variable', orientation='h', text='femme_text', color_discrete_sequence =['#424242']*len(women_bars), title='Femme', template='plotly_white')
    
    # Positioning text outside of the bars
    fig_men.update_traces(textposition='outside')
    fig_women.update_traces(textposition='outside')
    
    # Updating colors based on gender
    if (gender != "MAN"):
        fig_men.update_traces(marker=dict(color='#424242'), showlegend=False)
        fig_women.update_traces(marker=dict(color='#29b6f6'), showlegend=False)

    # Creating the layout for the subplots
    fig = make_subplots(specs=[[{"secondary_y": True}, {}]], rows=1, cols=2, subplot_titles=('Homme', 'Femme'), shared_yaxes=True)

    # Adding individual bar charts to subplots
    fig.add_trace(fig_men['data'][0], row=1, col=1,  secondary_y=True)
    fig.add_trace(fig_women['data'][0], row=1, col=2)

    # Updating the layout of the subplots
    fig.update_layout( showlegend=False, xaxis=(dict(range=[max(list(men_bars['Homme']))+5,0])),plot_bgcolor = "white",height=700, xaxis2=dict(range=[0, max(list(women_bars['Femme']))+5]), margin=dict(pad=40))
    fig.update_xaxes(mirror=True, ticks='outside', showline=True, gridcolor='lightgrey')

    # Setting the hover text
    for _, trace in enumerate(fig.data):
        trace.hovertemplate = f'<b>Drogue:</b> %{{y}}<br><b>Portion:</b> %{{x}}%<extra></extra>'
        
    return fig
