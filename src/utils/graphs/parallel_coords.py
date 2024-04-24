import plotly.graph_objects as go
import pandas as pd
from dash import html

import src.utils.colors as c
from src.utils.constants import PERSONNALITY_INFO, DRUG_INFO

pd.options.mode.chained_assignment = None

c_selected = c.GROUP4_3
c_not_selected = c.NEUTRAL_1
c_sober = c.NEUTRAL_3


def set_color(my_df, selected_drug):
    color_df = my_df.copy()
    # Set a default color index for all rows
    # A low value to pick the first color from the colorscale
    color_df['color'] = 0.1
    if selected_drug:
        # Set a specific color index for the selected drug to make it stand out
        # A value to pick the prominent color from the colorscale
        color_df.loc[selected_drug, 'color'] = 0.5
    # Set a different color index for the sober response to differentiate it
    # A high value to pick the last color from the colorscale
    color_df.loc['sober', 'color'] = 0.9
    return color_df


def get_colorscale(selected_drug):
    if selected_drug is not None:
        colorscale = [(0.00, c_not_selected), (0.30, c_not_selected), (0.31, "white"),  (0.34, "white"), (0.35,
                                                                                                          c_selected), (0.65, c_selected), (0.66, "white"),  (0.69, "white"), (0.70, c_sober),  (1.00, c_sober)]
    else:
        colorscale = [(0.00, c_not_selected), (0.45, c_not_selected),
                      (0.46, "white"),  (0.54, "white"), (0.55, c_sober), (1, c_sober)]
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
            dimensions.append({'label': PERSONNALITY_INFO[personality]['french'],
                              'values': my_df[personality], 'range': [-1, 1], 'tickvals': tickvals})
    return dimensions


def get_plot(my_df, selected_drug=None):
    my_df = set_color(my_df, selected_drug)

    fig = go.Figure(
        go.Parcoords(
            line=dict(
                # This should now properly map to the colorscale
                color=my_df['color'],
                colorscale=get_colorscale(selected_drug)
            ),
            dimensions=get_dimensions(my_df, selected_drug)
        )
    )

    # Update layout for font size, which affects all text including the dimension titles
    fig.update_layout(
        font=dict(
            size=14  # Adjust the size as needed
        )
    )

    return fig


def get_legend(selected_drug=None):
    def legend_box(color, text):
        return html.Div(children=[
            html.Span(style={'background-color': color,
                      'width': '20px', 'height': '20px', 'margin-right': '5px'}),
            html.Span(text)
        ], style={'display': 'flex', 'flex-direction': 'row', 'padding': '5px', 'align-items': 'center', 'justify-content': 'left', 'font-weight': 'bold'})

    if selected_drug is None:
        colors = [
            legend_box(c_not_selected, 'Consommateurs de drogues'),
            legend_box(c_sober, 'Répondants sobres')
        ]
    else:
        alias = 'Consommateurs '
        if DRUG_INFO[selected_drug]['french'][0] in 'aeiouy':
            alias += "d'"
        else:
            alias += 'de '
        colors = [
            legend_box(c_selected, alias + DRUG_INFO[selected_drug]['french']),
            legend_box(c_not_selected, 'Consommateurs des autres drogues'),
            legend_box(c_sober, 'Répondants sobres')
        ]
    return html.Div(children=colors)
