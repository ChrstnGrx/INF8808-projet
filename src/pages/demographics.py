import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output

dash.register_page(
    __name__, 
    path='/demographics',
    title='Demographics Analysis'
)

layout = html.Div(id='demographics-page', children=[
    html.Div(children=[
        html.Label('Tranche d\'âge'),
        dcc.Dropdown(
            id='dropdown-age',
            options=[
                {'label': '18-24 ans', 'value': '18-24'},
                {'label': '25-34 ans', 'value': '25-34'},
                {'label': '35-44 ans', 'value': '35-44'},
                {'label': '45-54 ans', 'value': '45-54'},
                {'label': '55-64 ans', 'value': '55-64'},
                {'label': '65+ ans', 'value': '65+'},
            ],
            value='18-24',
            className='selector-dropdown',
            placeholder="Sélectionnez une tranche d'âge...",
        )
    ]),
    html.Div(children=[
        html.Label('Sexe', className='selector-label'),
        dcc.Dropdown(
            id='dropdown-gender',
            options=[
                {'label': 'Homme', 'value': 'MAN'},
                {'label': 'Femme', 'value': 'WOMAN'},
            ],
            value='MAN',
            className='selector-dropdown',
            placeholder="Sélectionnez un sexe...",
        )
    ]),
    html.Div(children=[
        html.Label('Niveau d\'éducation'),
        dcc.Dropdown(
            id='dropdown-education',
            options=[
                {'label': 'Quitté l\'école avant 16 ans', 'value': 'BEFORE_16'},
                {'label': 'Quitté l\'école à 16 ans','value': 'AT_16'},
                {'label': 'Quitté l\'école à 17 ans','value': 'AT_17'},
                {'label': 'Quitté l\'école à 18 ans','value': 'AT_18'},
                {'label': 'Fréquenté une université, mais sans diplôme', 'value': 'SOME_COLLEGE_NO_DEGREE'},
                {'label': 'Baccaulauréat','value': 'UNIVERSITY_DEGREE'},
                {'label': 'Maîtrise','value': 'MASTERS_DEGREE'},
                {'label': 'Doctorat','value': 'DOCTORATE_DEGREE'},
            ],
            value='UNIVERSITY_DEGREE',
            placeholder="Sélectionnez un niveau d'éducation...",
        )
    ]),
])


