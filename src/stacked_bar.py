from colors import STACKED_COLORS
import plotly.express as px
from constants import DRUG_INFO, CONSUMPTION_CLASSES
from dash import html
import numpy as np

def set_color(my_df, selected_drug):
    color_df = my_df.copy()

    color_df['color-group'] = color_df.apply(lambda row: row['class'] + '-selected' if row['drug'] == selected_drug else row['class']+'-unselected', axis=1)

    return color_df

def translate(my_df):
    my_df['drug'] = my_df['drug'].apply(lambda x: DRUG_INFO[x]['french'].capitalize())
    my_df['class'] = my_df['class'].apply(lambda x: CONSUMPTION_CLASSES[x])
    return my_df

def get_plot(my_df, selected_drug=None):
    print(my_df)
    my_df = set_color(my_df, selected_drug)
    order = my_df.drug.unique()

    colors = [STACKED_COLORS[cl]['unselected'] for cl in STACKED_COLORS]
    colors.reverse()
    if selected_drug is not None:
        selected_colors = [STACKED_COLORS[cl]['selected'] for cl in STACKED_COLORS]
        selected_colors.reverse()
        if my_df.drug[0] == selected_drug:
            colors = selected_colors + colors
        else:
            colors = colors + selected_colors

    my_df = translate(my_df)
    fig = px.bar(my_df, x='drug', y='percentage', color='color-group', color_discrete_sequence=colors, category_orders={'drug': order}, template='plotly_white', custom_data=['class'])
    
    fig.update_layout(
        xaxis_title=None,
        yaxis_title='Distribution (%) par fréquence',
        showlegend=False
        )
    
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br><i>%{customdata[0]}</i><br>%{y:.2f}%<extra></extra>'
    )
    
    return fig

def get_legend(selected_drug=None):
    def color_box(color):
        return html.Span(style={'background-color': color, 'width': '20px', 'height': '20px'})

    if selected_drug is not None:
        colors = [
            html.Div(children=[
                color_box(STACKED_COLORS[cl]['selected']),
                color_box(STACKED_COLORS[cl]['unselected']),
                html.Span(CONSUMPTION_CLASSES[cl])
            ], style={'display': 'flex', 'flex-direction': 'row'}) for cl in STACKED_COLORS
        ]
    else :
        colors = [
            html.Div(children=[
                color_box(STACKED_COLORS[cl]['unselected']),
                html.Span(CONSUMPTION_CLASSES[cl])
            ], style={'display': 'flex', 'flex-direction': 'row'}) for cl in STACKED_COLORS
        ]
    return html.Div(children=colors)