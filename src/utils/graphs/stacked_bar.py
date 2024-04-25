from dash import html
import plotly.express as px
from src.utils.colors import STACKED_COLORS
from src.utils.constants import DRUG_INFO, CONSUMPTION_CLASSES

def set_color(df, selected_drug):
    """
    Assigns a color group based on drug selection to facilitate visualization differentiation.
    
    Parameters:
    - df (DataFrame): Input DataFrame.
    - selected_drug (str or None): Selected drug to highlight.
    
    Returns:
    - DataFrame: Updated DataFrame with a new 'color-group' column.
    """
    color_df = df.copy()

    color_df['color-group'] = color_df.apply(lambda row: row['class'] + '-selected' if row['drug']
                                             == selected_drug else row['class']+'-unselected', axis=1)

    return color_df


def translate(df):
    """
    Translates drug and class identifiers to human-readable form using predefined dictionaries.
    
    Parameters:
    - df (DataFrame): DataFrame with 'drug' and 'class' columns to be translated.
    
    Returns:
    - DataFrame: DataFrame with translated 'drug' and 'class' columns.
    """
    df['drug'] = df['drug'].apply(
        lambda x: DRUG_INFO[x]['french'].capitalize())
    df['class'] = df['class'].apply(lambda x: CONSUMPTION_CLASSES[x])
    return df


def get_plot(df, selected_drug=None):
    """
    Generates a bar plot showing drug consumption percentages with differentiated color groups.
    
    Parameters:
    - df (DataFrame): Data to plot.
    - selected_drug (str or None): Drug to highlight.
    
    Returns:
    - Figure: A Plotly bar plot figure.
    """
    df = set_color(df, selected_drug)

    # Define color sequences based on selection
    colors = [STACKED_COLORS[cl]['unselected'] for cl in STACKED_COLORS]
    colors.reverse()
    if selected_drug is not None:
        selected_colors = [STACKED_COLORS[cl]['selected']
                           for cl in STACKED_COLORS]
        selected_colors.reverse()
        if df.drug[0] == selected_drug:
            colors = selected_colors + colors
        else:
            colors = colors + selected_colors

    df = translate(df)
    order = df.drug.unique()

    fig = px.bar(df, x='drug', y='percentage', color='color-group', color_discrete_sequence=colors,
                 category_orders={'drug': order}, template='plotly_white', custom_data=['class'])

    # Customize plot layout and hover information
    fig.update_layout(
        xaxis=dict(tickfont=dict(size=14)),
        xaxis_title=None,
        yaxis_title='Distribution par fréquence (%)',
        showlegend=False
    )

    fig.update_traces(
        hovertemplate='<b>%{x}</b><br><i>%{customdata[0]}</i><br>%{y:.2f}%<extra></extra>'
    )

    return fig


def get_legend(selected_drug=None):
    """
    Creates an HTML legend for the visualization to explain the color coding.
    
    Parameters:
    - selected_drug (str or None): The drug that is specifically selected, if any.
    
    Returns:
    - Div: A Dash HTML Div element containing the legend.
    """
    def color_box(color):
        """ Helper to create a color box representation in the legend. """
        return html.Span(style={'background-color': color, 'width': '20px', 'height': '20px', 'margin-right': '5px'})
    
    # Create legend entries based on whether a drug is selected
    if selected_drug is not None:
        colors = [
            html.Div(children=[
                color_box(STACKED_COLORS[cl]['selected']),
                color_box(STACKED_COLORS[cl]['unselected']),
                html.Span(CONSUMPTION_CLASSES[cl])
            ], style={'display': 'flex', 'flex-direction': 'row', 'padding': '5px', 'align-items': 'center', 'justify-content': 'left', 'font-weight': 'bold'}) for cl in STACKED_COLORS
        ]
    else:
        colors = [
            html.Div(children=[
                color_box(STACKED_COLORS[cl]['unselected']),
                html.Span(CONSUMPTION_CLASSES[cl])
            ], style={'display': 'flex', 'flex-direction': 'row', 'padding': '5px', 'align-items': 'center', 'justify-content': 'left', 'font-weight': 'bold'}) for cl in STACKED_COLORS
        ]
    return html.Div(children=colors)
