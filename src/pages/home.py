import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output

dash.register_page(
    __name__,
    path='/',
    redirect_from=['/home'],
    title='Page d\'accueil',)

layout = html.Div([
    html.Div(id='header', children=[
        html.Div(id='nav', children=[
                html.Button('Vers l\'analyse des drogues',
                            id='forward-button', n_clicks=0),
        ]),
        html.H1('Page d\'accueil'),
    ]),
    html.Div([
        html.H2("Table des matières"),
        html.Ol(id="main-table-of-contents", children=[
            html.Li([
                html.A("Mise en contexte", href="#mise-en-contexte"),
                html.Ol([
                    html.Li(html.A("Contexte", href="#contexte")),
                    html.Li(html.A("Objectif", href="#objectif")),
                    html.Li(html.A("Public cible", href="#public-cible")),
                ])
            ]),
            html.Li([
                html.A("Jeu de données", href="#jeu-de-donnees"),
                html.Ol([
                    html.Li(html.A("Métadonnées", href="#metadonnees")),
                    html.Li(html.A("Données", href="#donnees")),
                ])
            ]),
            html.Li(html.A("Utilisateurs cibles", href="#utilisateurs-cibles")),
            html.Li(html.A("Questions cibles", href="#questions-cibles")),
            html.Li(html.A("Design général", href="#design-general")),
            html.Li(html.A("Maquette", href="#maquette")),
        ])
    ]),
    html.Div([
        html.H2("1. Mise en Contexte"),
        html.P("La consommation de drogues est une problématique majeure de santé publique et sociale. Cette étude vise à comprendre les facteurs influençant cette consommation pour mieux cibler les efforts de prévention."),
        html.H3("1.1. Contexte"),
        html.P("La consommation de drogues est une problématique sociale et de santé publique majeure qui intéresse un large éventail de personnes, des décideurs politiques aux professionnels de la santé en passant par les membres de la société civile. Cette préoccupation découle de l'impact significatif que la consommation de drogues peut avoir sur la santé individuelle, le bien-être social et la stabilité communautaire. En effet, la consommation de drogues peut entraîner des conséquences néfastes telles que des problèmes de santé mentale et physique, des dépendances, des comportements à risque, des conflits familiaux, des accidents de la route et des incidences sur la productivité au travail."),
        html.P("Une analyse sur la consommation de drogues est cruciale pour justifier les efforts de prévention et de sensibilisation. En effet, la prévention de la consommation de drogues vise à réduire les dommages potentiels pour les individus et la collectivité en promouvant des comportements sains et en réduisant les risques liés à la consommation de substances psychoactives. En comprenant mieux les facteurs qui influencent la consommation de drogues et ses conséquences, on peut adopter différents moyens de préventions plus efficaces et plus ciblés et la société peut s’engager dans des initiatives visant à promouvoir la santé et son bien-être."),
        html.H3("1.2. Objectif"),
        html.P("Identifier les facteurs principaux liés à la consommation de drogues et fournir des données pour soutenir les initiatives de prévention."),
        html.H3("1.3. Public Cible"),
        html.P(
            "ONGs, décideurs politiques, professionnels de santé, et membres de la société civile."),
    ]),
    html.Div([
        html.H2("2. Jeu de Données"),
        html.H3("2.1. Métadonnées"),
        html.P("Données collectées et approuvées par l'École de Psychologie de l'Université de Leicester, couvrant un échantillon de 1885 participants."),
        html.H3("2.2. Données"),
        html.P("Informations sur la personnalité, les antécédents sociodémographiques et les habitudes de consommation des participants."),
    ]),
    html.Div([
        html.H2("3. Utilisateurs Cibles"),
        html.P("L'étude cible un large spectre de consommateurs pour maximiser l'impact des initiatives de prévention."),
    ]),
    html.Div([
        html.H2("4. Questions Cibles"),
        html.P("Analyse des données axée sur la comparaison entre groupes sociaux, traits de personnalité, et types de drogues consommées."),
    ]),
    html.Div([
        html.H2("5. Design Général"),
        html.P("Présentation sous forme de deux tableaux de bord interactifs, facilitant la navigation entre différentes visualisations des données."),
    ]),
    html.Div([
        html.H2("6. Maquette"),
        html.P("Détails des visualisations proposées, avec description et justification de leur conception pour répondre aux questions de l'étude."),
    ]),
    dcc.Link('Découvrir les visualisations', href='/visualizations')
])

# @callback(
#     Output('url-forward', 'pathname'),
#     Input('forward-button', 'n_clicks'),
#     prevent_initial_call=True
# )
# def navigate_to_demographics(n_clicks):
#     if n_clicks > 0:
#         return '/demographics'
