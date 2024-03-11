# Load d3blocks
from d3blocks import D3Blocks
import os

def create_chord_diagram(df):
    d3 = D3Blocks(chart='Chord', frame=False)
    d3.chord(
        df, 
        arrowhead=-1,
        title='chord', 
        color='#110000',
        showfig=False,
        overwrite=True,
        save_button=False,
        opacity=0.2,
        )
    for drug in df.source.unique():
        d3.node_properties.get(drug)['color']='#110000'
        d3.node_properties.get(drug)['opacity']=0.2
    d3.node_properties.get('alcohol')['color']='green'
    d3.node_properties.get('alcohol')['opacity']=0.8
    d3.set_edge_properties(df, color='target', opacity='target')
    print(d3.config)
    d3.show(
        filepath=os.path.join('src', 'chord.html'),
        showfig=True
    )
    return None