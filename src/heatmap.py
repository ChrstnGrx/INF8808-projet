import plotly.graph_objects as go
import pandas as pd
import numpy as np
from ucimlrepo import fetch_ucirepo
import utils.preprocess as preprocess
import sys
from pathlib import Path

base_path = Path(__file__).resolve().parent.parent
sys.path.append(str(base_path))

# Fetch the dataset and preprocess
dataframe = fetch_ucirepo(id=373).data.original
dataframe = preprocess.drop_columns(dataframe)
dataframe = preprocess.fix_errors(dataframe)
drug_corr_df = preprocess.drug_correlation(dataframe)

# Define color palettes
neutral_palette = ['#f5f5f5', '#e0e0e0', '#bdbdbd',
                   '#9e9e9e', '#757575', '#616161', '#424242']
active_palette = ['#e1f5fe', '#b3e5fc', '#81d4fa',
                  '#29b6f6', '#039be5', '#0277bd', '#01579b']

# Convert the correlation DataFrame to a matrix
drug_corr_matrix = drug_corr_df.pivot_table(
    index='source', columns='target', values='weight', aggfunc='sum')
# Fill NaN with 0s
drug_corr_matrix = drug_corr_matrix.fillna(0)

# Symmetrize the matrix by adding the transpose and subtracting the diagonal
symmetric_matrix = drug_corr_matrix + drug_corr_matrix.T - pd.DataFrame(np.diag(np.diag(
    drug_corr_matrix)), index=drug_corr_matrix.index, columns=drug_corr_matrix.columns)

# Define the active drug
active_drug = 'alcohol'

# Normalize the weights and apply color palettes
max_weight = symmetric_matrix.max().max()
normalized_matrix = symmetric_matrix / max_weight

color_matrix = normalized_matrix.applymap(lambda x: active_palette[int(
    x * (len(active_palette) - 1))] if x > 0 else neutral_palette[0])

# Convert color matrix to color list accepted by Plotly
color_list = []
for column in color_matrix:
    color_list.extend(color_matrix[column].values)

# Create a heatmap with Plotly
fig = go.Figure(data=go.Heatmap(
    z=symmetric_matrix.to_numpy(),
    x=symmetric_matrix.columns,
    y=symmetric_matrix.index,
    colorscale=color_list,
    colorbar=dict(title='Fréquence de co-consommation'),
    hoverongaps=False
))

# Update the layout for a better presentation
fig.update_layout(
    title_text=f"Carte de chaleur de la co-consommation des drogues avec '{active_drug}' mis en évidence",
    xaxis_title="Drogue A",
    yaxis_title="Drogue B",
    xaxis=dict(side='bottom'),
    yaxis=dict(autorange='reversed'),
    plot_bgcolor='white',
)

fig.show()
