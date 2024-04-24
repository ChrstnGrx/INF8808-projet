import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output

dash.register_page(
    __name__,
    path='/',
    redirect_from=['/home'],
    title='Accueil',)

authors = [
    "Charles DE LAFONTAINE", "Dieynaba DIALLO", "Erika FOSSOUO",
    "Christine GROUX", "Samira YAZDANPOURMOGHADAM", "Aymen-Alaeddine ZEGHAIDA"
]

questions = [
    {"Questions": "Quelles caractéristiques de personnalité sont les plus associées à la consommation de chaque type de drogue ?",
     "Priorité": "☆☆☆",
     "Viz": "V3",
     "ID": '1'},
    {"Questions": "Quels types de drogues sont les plus populaires?",
     "Priorité": "☆☆☆",
     "Viz": "V2",
     "ID": '2'},
    {"Questions": "Comment la consommation de drogues varie-t-elle en fonction du niveau de recherche de sensation d’un individu (Sensation Seeking) ?",
     "Priorité": "☆☆",
     "Viz": "V3",
     "ID": '3'},
    {"Questions": "Quelles caractéristiques, au niveau personnalité, distinguent ceux qui ne consomment pas de drogues?",
     "Priorité": "☆☆",
     "Viz": "V3",
     "ID": '4'},
    {"Questions": "Selon l’effet passerelle de la drogue (la théorie de l’escalade des drogues), quel est le profil typique le plus corrélé vers la consommation des drogues passerelles (pour la prévention des non-consommateurs) ?",
     "Priorité": "☆☆☆",
     "Viz": "V1",
     "ID": '5'},
    {"Questions": "Quelles sont les tendances (de CL0 à CL6) de consommation de chaque type de drogue ?",
     "Priorité": "☆☆",
     "Viz": "V2",
     "ID": '6'},
    {"Questions": "Quelles drogues sont souvent consommées conjointement ?",
     "Priorité": "☆☆",
     "Viz": "V4",
     "ID": '7'},
    {"Questions": "Quels sont les schémas démographiques généraux des consommateurs de chaque drogue ?",
     "Priorité": "☆☆☆",
     "Viz": "V1",
     "ID": '8'},
    {"Questions": "Existe-t-il des différences notables dans les taux de consommation de drogues entre différents groupes démographiques (par ex., hommes vs femmes, différents groupes d'âge, différents niveaux d’études) ?",
     "Priorité": "☆☆☆",
     "Viz": "V6/V7",
     "ID": '9'},
    {"Questions": "Quelles caractéristiques, au niveau des caractères sociaux, distinguent ceux qui ne consomment pas de drogues?",
     "Priorité": "☆☆",
     "Viz": "V1",
     "ID": '10'}
]

layout = html.Div([
    html.Div(id='header', children=[
        html.Div(id='nav', children=[
                html.Button('Vers l\'analyse des drogues',
                            id='forward-button', n_clicks=0),
        ]),
        html.H1(
            'Une analyse pour la prévention et l\'éducation à la consommation de drogues'),
    ]),
    html.H2("Table des matières"),
    html.Div(className="table-of-contents", children=[
        html.Div(className="toc-item", children=[
            html.Span("1. ", className="toc-number"),
            html.Span(html.A("Mise en contexte", href="#mise-en-contexte"),
                      className="toc-link"),
            html.Div(className="toc-subitem", children=[
                html.Span("1.1. ", className="toc-number"),
                html.Span(html.A("Contexte", href="#contexte"),
                          className="toc-link"),
            ]),
            html.Div(className="toc-subitem", children=[
                html.Span("1.2. ", className="toc-number"),
                html.Span(html.A("Objectif", href="#objectif"),
                          className="toc-link"),
            ]),
            html.Div(className="toc-subitem", children=[
                html.Span("1.3. ", className="toc-number"),
                html.Span(html.A("Public cible", href="#public-cible"),
                          className="toc-link"),
            ]),
        ]),
        html.Div(className="toc-item", children=[
            html.Span("2. ", className="toc-number"),
            html.Span(html.A("Jeu de données", href="#jeu-de-donnees"),
                      className="toc-link"),
            html.Div(className="toc-subitem", children=[
                html.Span("2.1. ", className="toc-number"),
                html.Span(html.A("Métadonnées", href="#metadonnees"),
                          className="toc-link"),
            ]),
            html.Div(className="toc-subitem", children=[
                html.Span("2.2. ", className="toc-number"),
                html.Span(html.A("Données", href="#donnees"),
                          className="toc-link"),
            ]),
        ]),
        html.Div(className="toc-item", children=[
            html.Span("3. ", className="toc-number"),
            html.Span(html.A("Utilisateurs cibles",
                      href="#utilisateurs-cibles"), className="toc-link"),
        ]),
        html.Div(className="toc-item", children=[
            html.Span("4. ", className="toc-number"),
            html.Span(html.A("Questions cibles",
                      href="#questions-cibles"), className="toc-link"),
        ]),
        html.Div(className="toc-item", children=[
            html.Span("5. ", className="toc-number"),
            html.Span(html.A("Design général", href="#design-general"),
                      className="toc-link"),
        ]),
        html.Div(className="toc-item", children=[
            html.Span("6. ", className="toc-number"),
            html.Span(html.A("Visualisations", href="#viz"),
                      className="toc-link"),
        ]),
    ]),
    html.Div([
        html.H2("1. Mise en contexte", id='mise-en-contexte'),
        html.P("La consommation de drogues est une problématique majeure de santé publique et sociale. Cette étude vise à comprendre les facteurs influençant cette consommation pour mieux cibler les efforts de prévention."),
        html.H3("1.1. Contexte", id='contexte'),
        html.P("La consommation de drogues est une problématique sociale et de santé publique majeure qui intéresse un large éventail de personnes, des décideurs politiques aux professionnels de la santé en passant par les membres de la société civile. Cette préoccupation découle de l'impact significatif que la consommation de drogues peut avoir sur la santé individuelle, le bien-être social et la stabilité communautaire. En effet, la consommation de drogues peut entraîner des conséquences néfastes telles que des problèmes de santé mentale et physique, des dépendances, des comportements à risque, des conflits familiaux, des accidents de la route et des incidences sur la productivité au travail."),
        html.P("Une analyse sur la consommation de drogues est cruciale pour justifier les efforts de prévention et de sensibilisation. En effet, la prévention de la consommation de drogues vise à réduire les dommages potentiels pour les individus et la collectivité en promouvant des comportements sains et en réduisant les risques liés à la consommation de substances psychoactives. En comprenant mieux les facteurs qui influencent la consommation de drogues et ses conséquences, on peut adopter différents moyens de préventions plus efficaces et plus ciblés et la société peut s’engager dans des initiatives visant à promouvoir la santé et son bien-être."),
        html.H3("1.2. Objectif", id='objectif'),
        html.P("L`objectif principal de cette étude consiste à identifier et à faire ressortir les principaux facteurs liés à la consommation de drogues grâce à l'analyse approfondie d'un riche ensemble de données regroupant des informations sur 1885 individus, leur personnalité, leurs antécédents sociodémographiques et leurs habitudes de consommation de 18 substances psychoactives différentes. Grâce à cette recherche, nous visons à apporter des éléments probants susceptibles d'orienter les efforts de prévention et d'éducation en matière de mauvaise utilisation de substances psychoactives."),
        html.H3("1.3. Public cible", id='public-cible'),
        html.P(
            "Le public cible principal de cette étude est composé d'organismes non gouvernementales (ONG) actifs dans le domaine de la prévention et de l'éducation relativement à la consommation de drogues. Souvent mandatés pour soutenir les initiatives communautaires et assurer une meilleure coordination entre les secteurs public et privé, ces organismes jouent un rôle crucial dans la mise en place de services et de programmes destinés aux personnes touchées par la toxicomanie et aux membres de leur famille."),
    ]),
    html.Div([
        html.H2("2. Jeu de données", id='jeu-de-donnees'),
        html.H3("2.1. Métadonnées", id='metadonnees'),
        html.P(children=[
            html.Span(
                "La base de données a été collectée par Elaine Fehrman, Vincent Egan et Evgeny Mirkes entre mars 2011 et mars 2012. Elle a également été approuvée pour une étude sur le risque de consommation de drogues par des chercheurs de l'"),
            html.A(
                "École de Psychologie et des Sciences de la Vision de l'Université de Leicester; les données sont disponibles en ligne",
                href="https://le.ac.uk/psychology-vision-sciences",
                target="_blank"
            ),
            html.Span(
                " [2]."
            ),
        ]),
        html.P(children=[
            html.Span(
                "Les données d'entrée ont été recueillis en utilisant la version espagnole du "),
            html.A("Questionnaire de Personnalité de Zuckerman-Kuhlman (ZKPQ)",
                   href="https://www.psytoolkit.org/survey-library/zkpq-50-cc.html",
                   target="_blank"),
            html.Span(
                ", qui est un questionnaire psychométrique visant à évaluer les traits de base de la personnalité en demandant aux participants de répondre à items « Vrai » ou « Faux » [1]. Ce questionnaire a été distribué grâce à un outil de sondage en ligne de Survey Gizmo (maintenant "),
            html.A("Alchemer",
                   href='https://www.alchemer.com/',
                   target="_blank"),
            html.Span(") afin de maximiser l'anonymat, compte tenu de la nature sensible de l'usage de drogues. Tous les participants devaient se déclarer âgés d'au moins 18 ans avant que le consentement éclairé ne soit donné."),
        ]),
        html.P("L'étude a recruté 2051 participants sur une période de recrutement de 12 mois. Parmi ces personnes, 166 n'ont pas répondu correctement à un contrôle de validité intégré au milieu de l'échelle, donc ont été présumées inattentives aux questions posées."),
        html.P("Neuf de ces personnes ont également été trouvées ayant déclaré utiliser une drogue récréative fictive (Semeron), qui était incluse précisément pour identifier les répondants qui exagèrent, comme l'ont fait d'autres études de ce type."),
        html.P("Au final, cela a conduit à un échantillon utilisable de 1885 participants (homme/femme = 943/942) dans un fichier .data de 32 colonnes."),
        html.H3("2.2. Données", id='donnees'),
        html.P(children=[
            html.Span("Pour chaque répondant, le jeu de données contient 12 attributs dont l'âge (1), le genre (2), le niveau d'éducation (3), le pays de résidence (4) et l'ethnicité (5) et d’autres qui métriques issues des modèles suivants:"),
            html.Ol(id='main-sources', children=[
                html.Li(
                    "L'Inventaire révisé des cinq facteurs NEO (« Revised NEO Five-Factor Inventory » (NEO-FFI-R))"),
                html.Li(
                    "L’échelle d'impulsivité de Barratt (« Barratt Impulsiveness Scale v11 » (BIS-11))"),
                html.Li(
                    "L’échelle de recherche de sensation et d'impulsivité (« Impulsivity Sensation-Seeking scale » (ImpSS))"),
            ]),
            html.Span("Ces métriques sont le névrosisme (6), l’extraversion (7), l’ouverture à l'expérience (8), l’agréabilité (9), la conscience (10), l'impulsivité (11) et la recherche de sensations (12). "),
            html.Span("Dans le sondage, les participants ont été interrogés concernant leur utilisation de 18 drogues légales et illégales (alcool (13), amphétamines (14), nitrite d'amyle (15), benzodiazépine (16), caféine (17), cannabis (18), chocolat (19), cocaïne (20), crack (21), ecstasy (22), héroïne (23), kétamine (24), legal highs (25), LSD (26), méthadone (27), champignons (28), nicotine (29), une drogue fictive (Semeron) (30) qui a été introduite pour identifier les surdéclarants et abus de substance volatile (VSA) (31)). "),
        ]),
    ]),
    html.Div([
        html.H2("3. Utilisateurs cibles", id='utilisateurs-cibles'),
        html.P("Le projet cible tous les types de consommateurs, y compris les non-consommateurs, les consommateurs occasionnels, et ceux cherchant à réduire ou cesser leur consommation, dans le but d’élargir l’impact des ONG en prévention et éducation sur la drogue. Ce projet instaure, en première page, une culture de sensibilisation aux risques de la consommation de drogues. En ciblant tout type de consommateur pouvant être intéressé aux visualisations, notre projet s’arrime à la mission des ONG de prévenir efficacement la toxicomanie et à soutenir la communauté dans son ensemble dans la lutte contre les répercussions liées aux drogues."),
    ]),
    html.Div([
        html.H2("4. Questions cibles", id='questions-cibles'),
        html.P("Cette section détaille les questions cibles envisagées pour la visualisation des données, structurées autour de trois principaux angles de vue : la comparaison entre les groupes sociaux, la comparaison entre les traits de personnalité et la comparaison entre différentes drogues. Chaque question cible se voit attribuer une priorité basée sur sa pertinence supposée pour les utilisateurs ciblés, avec une notation allant de trois (3) étoiles (☆☆☆) pour les plus prioritaires à une (1) étoile (☆) pour les moins critiques."),
        html.H3("Angles de vue"),
        html.Ul(id='view-angles', children=[
            html.Li("Comparaison entre les groupes sociaux", id='view-angle-1'),
            html.Li("Comparaison entre les traits de personnalité",
                    id='view-angle-2'),
            html.Li("Comparaison entre les différentes drogues",
                    id='view-angle-3')
        ]),
        html.P(children=[
            html.B("Tableau 1."),
            html.Span(" Questions cibles et priorités subjectives de notre jeu de données, classées par angle de vue et sous-classées par priorité, avec référence vers leurs visualisations respectives.")
        ], className='table-title'),
        dash_table.DataTable(
            columns=[
                {'name': '#', 'id': 'ID'},
                {"name": "Questions", "id": "Questions"},
                {"name": "Priorité (/3)", "id": "Priorité"},
                {"name": "Viz", "id": "Viz"}
            ],
            # Make sure 'questions' is defined properly as a list of dictionaries.
            data=questions,
            style_table={
                'maxWidth': '80%',
                'marginLeft': '10%',
            },
            style_cell={
                'textAlign': 'center',
                'whiteSpace': 'normal',
                'height': 'auto',
                'minWidth': '20%',
                'maxWidth': '40%',
                'fontSize': '1rem',
            },
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold',
                'fontSize': '1.15rem',
            },
            style_data_conditional=[
                {'if': {'filter_query': '{Priorité} contains "☆☆☆"'},
                 'fontWeight': 'bold'},
                {'if': {'filter_query': '{ID} contains "1"'},
                 'backgroundColor': '#004ba0', 'color': 'white'},
                {'if': {'filter_query': '{ID} = 2'},
                    'backgroundColor': '#004ba0', 'color': 'white'},
                {'if': {'filter_query': '{ID} = 3'},
                    'backgroundColor': '#004ba0', 'color': 'white'},
                {'if': {'filter_query': '{ID} = 4'},
                    'backgroundColor': '#004ba0', 'color': 'white'},
                {'if': {'filter_query': '{ID} = 5'},
                 'backgroundColor': '#0288d1', 'color': 'white'},
                {'if': {'filter_query': '{ID} = 6'},
                    'backgroundColor': '#0288d1', 'color': 'white'},
                {'if': {'filter_query': '{ID} = 7'},
                    'backgroundColor': '#0288d1', 'color': 'white'},
                {'if': {'filter_query': '{ID} = 8'},
                 'backgroundColor': '#81d4fa', 'color': 'black'},
                {'if': {'filter_query': '{ID} = 9'},
                    'backgroundColor': '#81d4fa', 'color': 'black'},
                {'if': {'filter_query': '{ID} = 10'},
                    'backgroundColor': '#81d4fa', 'color': 'black'}
            ]
        ),
    ]),
    html.Div([
        html.H2("5. Design général", id='design-general'),
        html.P("Le résultat final est présenté sous forme de deux tableaux de bord (précisémnent en Analyse des drogues et en Analyse démographique), avec des boutons de navigation pour faciliter le changement d’une vue à une autre."),
        html.P("La vision bas-niveau est guidée par le contraste entre des nuances grises et les nuances bleu, des parties parties neutres (non sélectionnées) vers les parties actives (drogue sélectionnée) du tableau de bord, ce qui attire l'attention des utilisateurs vers les visualisations."),
        html.P("Au sein de l'Analyse des drogues, on trouve un menu déroulant pour sélectionner une drogue parmi la liste disponible dans les données. Le menu déroulant permet d’interagir avec le reste des visualisations. L’utilisateur doit sélectionner la drogue qui l'intéresse afin de réorganiser la représentation des visualisations 1 à 4."),
        html.P("Par défaut (ou si aucune drogue n’est sélectionnée), les visualisations portent toutes la même couleur, et la lecture des données est faite grâce à la surface et le volume d’encre. En sélectionnant une drogue dans la liste déroulante, la drogue est mise en évidence dans toutes les visualisations. Les autres drogues seront grisées."),
        html.P("Lorsque ledit menu déroulant est étendu, il cache la surface permettant d’afficher l'icône des drogues passerelles, répondant ainsi à la question 5. Si une drogue est une drogue passerelles, l'icône sera affichée. S’il n’y a pas de drogue passerelle sélectionnée, l’espace est vide. La liste des options du menu est la même que les catégories de drogues dans notre jeu de données (en ajout : une option pour retirer la sélection)."),
        html.P("La seconde page, soit l'Analyse démographique, contient les visualisation 5 à 7. Comme ces visualisations permettent de faire des comparaison entre les groupes sociaux, il est dépendent du groupe social (âge/sexe/éducation) du consommateur. Pour sélectionner son groupe social, l’utilisateur devra interagir avec trois menus déroulants. L'utilisateur est alors invité à sélectionner son groupe social pour qu’il puisse faire une auto-évaluation à titre préventif."),
    ]),
    html.Div([
        html.H2("6. Visualisations", id='viz'),
        html.P("Détails des visualisations proposées, avec description et justification de leur conception pour répondre aux questions de l'étude."),
    ]),
    dcc.Link('Découvrir les visualisations', href='/visualizations'),
    html.Div([
        html.Div([html.Div(author, className="typewrite")
                  for author in authors], style={'font-size': '12px', 'font-family': 'Courier New', 'textAlign': 'center'})
    ])
])

# @callback(
#     Output('url-forward', 'pathname'),
#     Input('forward-button', 'n_clicks'),
#     prevent_initial_call=True
# )
# def navigate_to_demographics(n_clicks):
#     if n_clicks > 0:
#         return '/demographics'
