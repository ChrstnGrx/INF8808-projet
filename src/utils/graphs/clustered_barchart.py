import plotly.express as px

def cluster_by_age(df, colors):
    """
    Creates a clustered bar chart grouped by age.

    Args:
        df: DataFrame containing the data.
        colors: List of colors for the bars.

    Returns:
        fig: Clustered bar chart.
    """
    # Creating the clustered bar chart
    fig = px.bar(df, x='drug', y=df.columns[1:],
                 barmode='group',
                 labels={'drug': 'Drogue', 'value': 'Portion de consommateurs', 'variable': 'Groupe d\'âge'})
    
    for i, trace in enumerate(fig.data):
        trace.hovertemplate = f'<b>Tranche d\'âge:</b> {trace["legendgroup"]}<br><b>Drogue:</b> %{{x}}<br><b>Portion de consommateurs:</b> %{{y:.2%}}<extra></extra>'

    # Applying colors to the bars
    for i in range(len(colors)):
        fig.data[i].marker.color = colors[i]

    fig.update_xaxes(tickangle=45)
    fig.update_yaxes(tickformat=",.0%",
                     title_text="Proportion de consommateurs (%)")
    
    fig.update_layout(
        legend_title_text='Tranches d\'âge',
        template='plotly_white',
        legend_traceorder="reversed",
        legend_yanchor="middle",
        legend_y=0.5
    )

    return fig


def cluster_by_education(df, colors):
    """
    Creates a clustered bar chart grouped by education level.

    Args:
        df: DataFrame containing the data.
        colors: List of colors for the bars.

    Returns:
        fig: Clustered bar chart.
    """
    # Creating the clustered bar chart
    fig = px.bar(df, x='drug', y=df.columns[1:],
                barmode='group',
                labels={'drug': 'Drogue', 'value': 'Portion de consommateurs', 'variable': 'Niveau d\'éducation'})

    for i, trace in enumerate(fig.data):
        trace.hovertemplate = f'<b>Niveau d\'éducation:</b> {trace["legendgroup"]}<br><b>Drogue:</b> %{{x}}<br><b>Portion de consommateurs:</b> %{{y:.2%}}<extra></extra>'

    for i in range(len(colors)):
        fig.data[i].marker.color = colors[i]

    fig.update_xaxes(tickangle=45)
    fig.update_yaxes(tickformat=",.0%",
                     title_text="Proportion de consommateurs (%)")

    fig.update_layout(
        legend_title_text='Niveau d\'éducation',
        template='plotly_white',
        legend_traceorder="reversed",
        legend_yanchor="middle",
        legend_y=0.5
    )

    return fig
