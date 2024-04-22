import plotly.graph_objects as go
import src.colors as c
from src.utils.constants import PERSONNALITY_INFO, DRUG_INFO
from dash import html

c_selected = c.GROUP4_3
c_not_selected = c.NEUTRAL_1
c_sober = c.NEUTRAL_3


def set_color(my_df, selected_drug):
    color_df = my_df.copy()
    color_df['color'] = 0
    color_df.color['sober'] = 1

    if selected_drug:
        color_df.color[selected_drug] = 0.5

    return color_df

def get_colorscale(selected_drug):
    if selected_drug is not None:
        colorscale = [(0.00, c_not_selected), (0.30, c_not_selected), (0.31, "white"),  (0.34, "white"), (0.35, c_selected), (0.65, c_selected), (0.66, "white"),  (0.69, "white"), (0.70, c_sober),  (1.00, c_sober)]
    else:
        colorscale = [(0.00, c_not_selected), (0.45, c_not_selected), (0.46, "white"),  (0.54, "white"), (0.55, c_sober), (1, c_sober)]
    return colorscale

def get_dimensions(my_df, selected_drug):
    def round(x):
        return int(x * 100) / 100

    dimensions = []
    for personality in my_df.columns:
        if personality != 'color':
            tickvals = [-1, -0.5, 0, 0.5, 1]
            if selected_drug is not None:
                selected_value = round(my_df[personality][selected_drug])
                for i in range(0, len(tickvals)):
                    if tickvals[i] > selected_value - 0.1 and tickvals[i] < selected_value + 0.1:
                        tickvals.pop(i)
                        break
                tickvals.append(selected_value)
            dimensions.append({'label': PERSONNALITY_INFO[personality]['french'], 'values': my_df[personality], 'range': [-1, 1], 'tickvals': tickvals})
    return dimensions

def get_plot(my_df, selected_drug=None):
    my_df = set_color(my_df, selected_drug)

    fig = go.Figure(
        go.Parcoords(
            line=dict(color=my_df['color'], colorscale = get_colorscale(selected_drug)),
            dimensions=get_dimensions(my_df, selected_drug)
        )
    )
    return fig

def get_legend(selected_drug=None):    
    def legend_box(color, text):
        return html.Div(children=[
                html.Span(style={'background-color': color, 'width': '20px', 'height': '20px'}),
                html.Span(text)
            ], style={'display': 'flex', 'flex-direction': 'row'})


    if selected_drug is None:
        colors = [
            legend_box(c_not_selected, 'Consommateurs de drogues'),
            legend_box(c_sober, 'Répondants sobres')
        ]
    else :
        colors = [
            legend_box(c_selected, 'Consommateurs de ' + DRUG_INFO[selected_drug]['french']),
            legend_box(c_not_selected, 'Consommateurs des autres drogues'),
            legend_box(c_sober, 'Répondants sobres')
        ]
    return html.Div(children=colors)