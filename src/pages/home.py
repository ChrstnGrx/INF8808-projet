import dash
from dash import dcc, html, dash_table, callback
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
     "Viz": "3",
     "ID": '1'},
    {"Questions": "Quels types de drogues sont les plus populaires?",
     "Priorité": "☆☆☆",
     "Viz": "2",
     "ID": '2'},
    {"Questions": "Comment la consommation de drogues varie-t-elle en fonction du niveau de recherche de sensation d’un individu (Sensation Seeking) ?",
     "Priorité": "☆☆",
     "Viz": "3",
     "ID": '3'},
    {"Questions": "Quelles caractéristiques, au niveau personnalité, distinguent ceux qui ne consomment pas de drogues?",
     "Priorité": "☆☆",
     "Viz": "3",
     "ID": '4'},
    {"Questions": "Selon l’effet passerelle de la drogue (la théorie de l’escalade des drogues), quel est le profil typique le plus corrélé vers la consommation des drogues passerelles (pour la prévention des non-consommateurs) ?",
     "Priorité": "☆☆☆",
     "Viz": "1",
     "ID": '5'},
    {"Questions": "Quelles sont les tendances (de CL0 à CL6) de consommation de chaque type de drogue ?",
     "Priorité": "☆☆",
     "Viz": "2",
     "ID": '6'},
    {"Questions": "Quelles drogues sont souvent consommées conjointement ?",
     "Priorité": "☆☆",
     "Viz": "4",
     "ID": '7'},
    {"Questions": "Quels sont les schémas démographiques généraux des consommateurs de chaque drogue ?",
     "Priorité": "☆☆☆",
     "Viz": "1",
     "ID": '8'},
    {"Questions": "Existe-t-il des différences notables dans les taux de consommation de drogues entre différents groupes démographiques (par ex., hommes vs femmes, différents groupes d'âge, différents niveaux d’études) ?",
     "Priorité": "☆☆☆",
     "Viz": "6/7",
     "ID": '9'},
    {"Questions": "Quelles caractéristiques, au niveau des caractères sociaux, distinguent ceux qui ne consomment pas de drogues?",
     "Priorité": "☆☆",
     "Viz": "1",
     "ID": '10'}
]

questions_viz_1 = [q for q in questions if q['ID'] in ['5', '8', '10']]
questions_viz_2 = [q for q in questions if q['ID'] in ['2', '6']]
questions_viz_3 = [q for q in questions if q['ID'] in ['1', '3', '4']]
questions_viz_4 = [q for q in questions if q['ID'] in ['7']]
questions_viz_5_6_7 = [q for q in questions if q['ID'] in ['9']]

layout = html.Div([
    html.Div(id='header', children=[
        html.Div(id='nav', children=[
                html.Button('Vers l\'analyse des drogues',
                            id='forward-forward-button', n_clicks=0),
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
            html.Div(className="toc-subitem", children=[
                html.Span("6.1. ", className="toc-number"),
                html.Span(html.A("Viz #1 – Icônes SVG", href="#viz-1"),
                          className="toc-link"),
            ]),
            html.Div(className="toc-subitem", children=[
                html.Span("6.2. ", className="toc-number"),
                html.Span(html.A("Viz #2 – Diagramme à barres empilées", href="#viz-2"),
                          className="toc-link"),
            ]),
            html.Div(className="toc-subitem", children=[
                html.Span("6.3. ", className="toc-number"),
                html.Span(html.A("Viz #3 – Diagramme de coordonnées parallèles", href="#viz-3"),
                          className="toc-link"),
            ]),
            html.Div(className="toc-subitem", children=[
                html.Span("6.4. ", className="toc-number"),
                html.Span(html.A("Viz #4 – Diagramme de cordes", href="#viz-4"),
                          className="toc-link"),
            ]),
            html.Div(className="toc-subitem", children=[
                html.Span("6.5. ", className="toc-number"),
                html.Span(html.A("Viz #5 – Diagrammes à barres horizontales", href="#viz-5"),
                          className="toc-link"),
            ]),
            html.Div(className="toc-subitem", children=[
                html.Span("6.6. ", className="toc-number"),
                html.Span(html.A("Viz #6 – Diagrammes à barres groupées (âge)", href="#viz-6"),
                          className="toc-link"),
            ]),
            html.Div(className="toc-subitem", children=[
                html.Span("6.7. ", className="toc-number"),
                html.Span(html.A("Viz #7 – Diagrammes à barres groupées (éducation)", href="#viz-7"),
                          className="toc-link"),
            ]),
        ]),
        html.Div(className="toc-item", children=[
            html.Span("7. ", className="toc-number"),
            html.Span(html.A("Références", href="#references"),
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
            html.Span(
                "Pour chaque répondant, le jeu de données contient 12 attributs dont l'âge (1), le genre [note: nous avons choisi de représenter cette variable comme 'sexe'] (2), le niveau d'éducation (3), le pays de résidence (4) et l'ethnicité (5) et d’autres qui métriques issues des modèles suivants:"),
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
        html.P(children=[
            html.Span(
                "Cette section contient la maquette des visualisations qui répondent aux questions de la "),
            html.A("section 4",
                   href="#questions-cibles"),
            html.Span("."),
        ]),
        html.H3("6.1. Viz #1 – Icônes SVG", id='viz-1'),
        html.P(children=[
            html.Span(
                "La visualisation 1 cherche à répondre aux questions ci-dessous : "),
            dash_table.DataTable(
                columns=[
                    {'name': '#', 'id': 'ID'},
                    {"name": "Questions", "id": "Questions"},
                    {"name": "Priorité (/3)", "id": "Priorité"},
                    {"name": "Viz", "id": "Viz"}
                ],
                data=questions_viz_1,
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
                    {'if': {'filter_query': '{ID} = 5'},
                     'backgroundColor': '#0288d1', 'color': 'white'},
                    {'if': {'filter_query': '{ID} = 8'},
                     'backgroundColor': '#81d4fa', 'color': 'black'},
                    {'if': {'filter_query': '{ID} = 10'},
                     'backgroundColor': '#81d4fa', 'color': 'black'},
                ],
            ),
        ]),
        html.P(children=[
            html.Span("Les caractéristiques démographiques des consommateurs sont représentées dans cette visualisation grâce à un ensemble d'icônes en SVG « "),
            html.A("Scalable Vector Graphics",
                   href='https://fr.wikipedia.org/wiki/Scalable_Vector_Graphics',
                   target="_blank"),
            html.Span(" » récoltées du "),
            html.A("domaine public",
                   href='https://www.svgrepo.com',
                   target="_blank"),
            html.Span(
                " [3] et accompagnées de sous-titres, afin de décrire précisément la catégorie visée."),
        ]),
        html.P("Pour la drogue sélectionnée avec le menu déroulant, on retrouve dans la zone de d’affichage 1 trois icônes représentant la tranche d’âge, le niveau d’éducation et le sexe consommant le plus le type de drogue sélectionné en noir, répondant ainsi la question 8. Pour répondre à la question 10, il suffit alors de retirer la drogue (aucune drogue sélectionnée) pour montrer les trois caractères sociaux qui distinguent un individu non-consommateur."),
        html.Div(children=[
            html.Img(src='/assets/static/1.png', className='icon'),
            html.P(children=[
                html.B("Figure 1."),
                html.Span(
                    " Échantillion d’une démographie : 55-65 ans, premier cycle universitaire achevé, femme.")
            ], className='figure-title'),
        ]),
        html.P("Les icônes servent à attirer l’attention du lecteur pour lui permettre une lecture rapide, et se basent sur ses connaissances a priori des symboles indiqués. Le justificatif pour ces icônes est que les images sont un bon canal pour véhiculer une idée si elles représentent quelque chose d'évocateur au public cible. De ce fait, ces icônes ont été choisies de manière à être le moins ambiguës possible et à exploiter le bagage culturel en visualisation d'un consommateur lambda."),
        html.P("Le sous-titrage, quant à lui, se justifie par le besoin de différencier certaines catégories de la variable éducation qui sont trop proches (exemple: Ayant quitté.e l'école avant 16 ans; Ayant quitté.e l'école avant 17 ans; Ayant quitté.e l'école avant 18 ans) et pour représenter des catégories de la variable de la tranche d'âge qui ne sont pas instinctivement déchiffrables (comme 45-55, 55-65, etc.)."),
        html.P("L'interaction principale de cette visualisation est la mise à jour automatique des trois icônes afin de correspondre à la drogue sélectionnée par l’utilisateur. Si aucune drogue n’est sélectionnée, les icônes sont grisées et l'icône des drogues passerelles disparaît."),
        html.P("La surface sous le menu déroulant permet d’afficher l'icône des drogues passerelles (Figure 2), répondant ainsi à la question 5. Si une drogue est une drogue passerelle, l'icône sera affichée. S’il n’y a pas de drogue passerelle sélectionnée, l’espace est vide."),
        html.Div(children=[
            html.Img(src='/assets/static/2.png', className='icon'),
            html.P(children=[
                html.B("Figure 2."),
                html.Span(
                    " Surface d’affichage de l'icône des drogues passerelles.")
            ], className='figure-title'),
        ]),
        html.H3("6.2. Viz #2 – Diagramme à barres empilées", id='viz-2'),
        html.P(children=[
            html.Span(
                "La visualisation 2 cherche à répondre aux questions ci-dessous : "),
            dash_table.DataTable(
                columns=[
                    {'name': '#', 'id': 'ID'},
                    {"name": "Questions", "id": "Questions"},
                    {"name": "Priorité (/3)", "id": "Priorité"},
                    {"name": "Viz", "id": "Viz"}
                ],
                data=questions_viz_2,
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
                    {'if': {'filter_query': '{ID} = 2'},
                     'backgroundColor': '#004ba0', 'color': 'white'},
                    {'if': {'filter_query': '{ID} = 6'},
                     'backgroundColor': '#0288d1', 'color': 'white'},
                ],
            ),
        ]),
        html.P("Chaque barre dans l'axe horizontal du graphique représente une drogue. L'axe vertical, soit la hauteur de la barre, représente le cumul de la fréquence de consommation de chaque drogue. En regardant cette visualisation, l’utilisateur va rapidement pouvoir observer quels types de drogues sont les plus populaires et ceux à la consommation la plus faible, puisque l’on peut facilement comparer la fréquence de la consommation de chaque drogue entre elles. En effet, les barres dans les graphiques seront placées en ordre décroissant de consommation (consommée dans le dernier jour) pour y faciliter la compréhension."),
        html.P("À l'intérieur de chaque barre, différentes classes représentent la proportion de chaque fréquence de consommation. Le montant de la consommation est divisé en sous sous-classes qui vont de « jamais consommée » (CL0) à « consommée dans le dernier jour » (CL6). Ce graphique interactif permet à l'utilisateur de cliquer sur une ou plusieurs de ces 7 sous-classes de consommation répertoriées dans la section légende pour visualiser uniquement les sections liées à la ou aux mêmes classes pour chaque drogue. Cette fonctionnalité permet à l'utilisateur de visualiser un schéma plus simple en fonction de ses besoins et obtenir des informations plus détaillées en supprimant les détails inutiles. De plus, en cliquant sur les classes dans les barres, les valeurs pertinentes sont affichées. Par défaut, tous les éléments de légende sont actifs, en cliquant sur n'importe quel nombre d'éléments de légende, leur texte deviendra gris clair et les classes consommées seront supprimées de la barre de drogue, ce qui peut être fait jusqu'à ce que toutes les classes soient supprimées. Bien entendu, en cliquant à nouveau sur le titre de chaque classe, le texte du titre de la classe dans la légende reviendra à l'état par défaut (gris gras) et la classe elle-même sera ajoutée au graphique."),
        html.P("Le graphique est présenté sous deux formes. La première est la présentation générale, soit quand l’utilisateur n’a pas sélectionné de drogue pour l’analyse. La seconde apparaît à la suite de la sélection d’une drogue quelconque pour l’analyse."),
        html.Div(children=[
            html.Img(src='/assets/static/3.webp', className='icon'),
            html.P(children=[
                html.B("Figure 3."),
                html.Span(
                    " Viz 2 sans drogue sélectionnée.")
            ], className='figure-title'),
        ]),
        html.Div(children=[
            html.Img(src='/assets/static/4.webp', className='icon'),
            html.P(children=[
                html.B("Figure 4."),
                html.Span(
                    " Viz 2 avec drogue sélectionnée.")
            ], className='figure-title'),
        ]),
    ]),
    html.H3("6.3. Viz #3 – Diagramme de coordonnées parallèles", id='viz-3'),
    html.P(children=[
        html.Span(
            "La visualisation 3 cherche à répondre aux questions ci-dessous : "),
        dash_table.DataTable(
            columns=[
                {'name': '#', 'id': 'ID'},
                {"name": "Questions", "id": "Questions"},
                {"name": "Priorité (/3)", "id": "Priorité"},
                {"name": "Viz", "id": "Viz"}
            ],
            data=questions_viz_3,
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
                {'if': {'filter_query': '{ID} = 1'},
                 'backgroundColor': '#004ba0', 'color': 'white'},
                {'if': {'filter_query': '{ID} = 3'},
                 'backgroundColor': '#004ba0', 'color': 'white'},
                {'if': {'filter_query': '{ID} = 4'},
                 'backgroundColor': '#004ba0', 'color': 'white'},
            ],
        ),
    ]),
    html.P("La visualisation 3 est un graphe de coordonnées parallèles. Les axes parallèles contiennent une échelle représentant l’indice de chaque trait de personnalité. Lorsque l’utilisateur survole un axe de personnalité, une info-bulle va apparaître et définir ce trait de personnalité, ce qui est nécessaire puisque la signification des traits de personnalité n’est pas évidente. Les lignes connectées représentent chacune une drogue. Elles traversent les axes parallèles à la moyenne de l’indice de personnalité de leurs consommateurs. Pour répondre à la quatrième question, on ajoute une ligne représentant les traits de personnalité moyens pour les répondants ne consommant pas de drogue. Un graphique de coordonnées parallèles a été choisi, car il permet de montrer des tendances connectées sur plusieurs échelles ordinales."),
    html.P("Le graphique est présenté sous deux formes. La première est la présentation générale, soit quand l’utilisateur n’a pas sélectionné de drogue pour l’analyse. Dans cette version, toutes les lignes représentant les drogues sont de la même couleur grise. Dans la seconde forme, la ligne représentant la drogue sélectionnée est colorée et légèrement plus épaisse. Les valeurs des indices de chaque personnalité sont affichées sur le graphique, pour la drogue sélectionnée. Toutes les autres sont dans la même teinte de gris."),
    html.Div(children=[
        html.Img(src='/assets/static/4.webp', className='icon'),
        html.P(children=[
            html.B("Figure 4."),
            html.Span(
                " Viz 3 sans drogue sélectionnée.")
        ], className='figure-title'),
    ]),
    html.Div(children=[
        html.Img(src='/assets/static/5.webp', className='icon'),
        html.P(children=[
            html.B("Figure 5."),
            html.Span(
                " Viz 3 avec drogue sélectionnée.")
        ], className='figure-title'),
    ]),
    html.H3("6.4. Viz #4 – Diagramme de cordes", id='viz-4'),
    html.P(children=[
        html.Span(
            "La visualisation 4 correspond à un diagramme de cordes (diagramme de Gauss, « chord diagram ») (voir Figure 6). Un tel diagramme sert à représenter des relations entre différentes entités. En ce qui nous concerne, dans le contexte de l’usage des drogues, ledit diagramme sera particulièrement adapté pour montrer les différentes combinaisons de drogues consommées ensemble. Il permettra sans aucun doute de répondre à la question suivante :"),
        dash_table.DataTable(
            columns=[
                {'name': '#', 'id': 'ID'},
                {"name": "Questions", "id": "Questions"},
                {"name": "Priorité (/3)", "id": "Priorité"},
                {"name": "Viz", "id": "Viz"}
            ],
            data=questions_viz_4,
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
                {'if': {'filter_query': '{ID} = 7'},
                 'backgroundColor': '#0288d1', 'color': 'white'},
            ],
        ),
    ]),
    html.P("La raison pour laquelle ce type de diagramme est l’un des meilleurs pour répondre à la question des combinaisons de drogues est qu’il permet de visualiser la complexité et l’intensité des interactions entre différentes catégories de manière intuitive. En effet, les liens ou « cordes » qui connectent les différents groupes de drogues révélera les tendances de consommation croisée et peuvent mettre en évidence des motifs et associations qui ne seraient pas évidents autrement."),
    html.Div(children=[
        html.Img(src='/assets/static/6.webp', className='icon'),
        html.P(children=[
            html.B("Figure 6."),
            html.Span(
                " Viz 4 avec drogue sélectionnée (alcool).")
        ], className='figure-title'),
    ]),
    html.P("À travers la première page de l’application, l'utilisateur peut sélectionner une drogue spécifique à partir d'un menu déroulant. Lorsqu'une drogue est sélectionnée, le diagramme à cordes est automatiquement mis à jour pour mettre en évidence les connexions entre la drogue choisie et les autres substances. Cette mise à jour dynamique permet d'analyser les tendances de consommation conjointe de drogues, révélant des associations et des motifs qui pourraient autrement rester cachés."),
    html.P("Le diagramme est accompagné d'une légende qui explique l'indice de consommation conjointe, échelonnée de « Extrêmement faible » à « Extrêmement élevée ». Chaque niveau de l'indice est associé à une couleur spécifique, allant du bleu clair au bleu foncé (gradation descendante de teintes selon la sévérité ascendante). La largeur du trait augmente également de quelques pixels selon la sévérité ascendante. La légende est générée dynamiquement (les indices de consommation conjointes qui ne sont pas visualisés en fonction de la drogue sélectionnée ne sont également pas affichés pour amoindrir la charge visuelle et cognitive). Cette légende est en fonction des poids des connexions entre les drogues, qui sont eux-même ajustés pour refléter la fréquence relative des associations de consommation conjointe, en pourcentage du total des associations observées."),
    html.P("Cette approche est particulièrement utile pour les organisations non gouvernementales (ONG) axées sur la santé publique, la réduction des méfaits et le soutien social pour comprendre les dynamiques de consommation de plusieurs substances, qui est une dimension complexe et souvent sous-estimée de la consommation de drogues."),
    html.H3("6.5. Viz #5 – Diagrammes à barres horizontales", id='viz-5'),
    html.P(children=[
        html.Span(
            "La visualisation 5 cherche à répondre à la question suivante :"),
        dash_table.DataTable(
            columns=[
                {'name': '#', 'id': 'ID'},
                {"name": "Questions", "id": "Questions"},
                {"name": "Priorité (/3)", "id": "Priorité"},
                {"name": "Viz", "id": "Viz"}
            ],
            data=questions_viz_4,
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
                {'if': {'filter_query': '{ID} = 9'},
                 'backgroundColor': '#81d4fa', 'color': 'black'},
            ],
        ),
    ]),
    html.P("Un graphe de deux diagrammes à barres horizontales côte à côte est le choix le plus approprié pour représenter les schémas démographiques généraux des consommateurs de chaque drogue en fonction du sexe, car il permet une comparaison directe et efficace entre les deux catégories, pour chaque catégorie de drogue. La valeur de chaque barre correspond à la proportion de consommateur de cette drogue parmi tous les consommateurs de son sexe. On considère qu'une personne est consommatrice si elle a consommé de cette drogue au moins dans le dernier mois. Voici un exemple de calcul utilisé :"),
    html.Div(children=[
        html.Img(src='/assets/static/7.webp', className='icon'),
        html.P(children=[
            html.B("Figure 7."),
            html.Span(
                " Exemple de calcul utilisé.")
        ], className='figure-title'),
    ]),
    html.P("De plus, lorsque l'utilisateur précise son sexe, le graphique correspondant affiche les barres horizontales pour ce sexe en bleu, tandis que l'autre sexe est représenté en gris. Cette coloration permet une visualisation claire et intuitive des différences entre les genres dans les schémas de consommation de drogues."),
    html.Div(children=[
        html.Img(src='/assets/static/8.webp', className='icon'),
        html.P(children=[
            html.B("Figure 8."),
            html.Span(
                " Viz 5 lorsque le sexe « Femme » est selectionné.")
        ], className='figure-title'),
    ]),
    html.H3("6.6. Viz #6 – Diagrammes à barres groupées (âge)", id='viz-6'),
    html.P(children=[
        html.Span(
            "La visualisation 6 cherche à répondre à la question suivante :"),
        dash_table.DataTable(
            columns=[
                {'name': '#', 'id': 'ID'},
                {"name": "Questions", "id": "Questions"},
                {"name": "Priorité (/3)", "id": "Priorité"},
                {"name": "Viz", "id": "Viz"}
            ],
            data=questions_viz_4,
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
                {'if': {'filter_query': '{ID} = 9'},
                 'backgroundColor': '#81d4fa', 'color': 'black'},
            ],
        ),
    ]),
    html.P("La visualisation 6 est un graphique à barres groupées (clustered barchart) qui offre un aperçu des taux de consommation pour chaque drogues au sein de différents groupes démographiques, ici différentes tranches d’âges. "),
    html.P("Chaque groupe représente une drogue, avec trois barres correspondantes à différentes tranches d'âge. La barre située au centre du groupe représente le taux de consommation de la drogue pour la tranche d’âge sélectionnée par l’utilisateur. La barre de gauche représente le taux de consommation pour des âges inférieurs à la tranche d’âge de la barre du centre et la barre de droite représente le taux de consommation pour des âges supérieurs à ceux de la barre du centre."),
    html.P("Cela permet une comparaison directe des taux de consommation de drogues pour différentes tranches d’âges, facilitant ainsi l’identification des tendances et des disparités dans les comportements de consommation."),
    html.P("Lorsque l’utilisateur choisit une tranche d’âge, la barre du centre dans chaque groupe est mise en bleu tandis que le reste est gris. La tranche d’âge de la barre du centre est celle qui correspond à la tranche d’âge de l’utilisateur, ainsi il obtient des informations qui le concernent directement."),
    html.Div(children=[
        html.Img(src='/assets/static/9.webp', className='icon'),
        html.P(children=[
            html.B("Figure 9."),
            html.Span(
                " Viz 6 lorsque la tranche d’âge 35-44 ans est sélectionnée.")
        ], className='figure-title'),
    ]),
    html.H3(
        "6.7. Viz #7 – Diagrammes à barres groupées (éducation)", id='viz-7'),
    html.P(children=[
        html.Span(
            "La visualisation 7 cherche à répondre à la question suivante :"),
        dash_table.DataTable(
            columns=[
                {'name': '#', 'id': 'ID'},
                {"name": "Questions", "id": "Questions"},
                {"name": "Priorité (/3)", "id": "Priorité"},
                {"name": "Viz", "id": "Viz"}
            ],
            data=questions_viz_4,
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
                {'if': {'filter_query': '{ID} = 9'},
                 'backgroundColor': '#81d4fa', 'color': 'black'},
            ],
        ),
    ]),
    html.P("La visualisation 7 est un graphique à barres groupées (clustered barchart) qui offre un aperçu des taux de consommation pour chaque drogue au sein de différents groupes démographiques, ici les différents niveaux d’éducation."),
    html.P("Il fonctionne exactement comme la visualisation 6 sauf qu’ici, il s’agit des différents niveaux d’éducation et non des différentes tranches d’âge. Ce sont donc les mêmes intéractions (mettre la barre du niveau d’étude concerné en couleur) et les mêmes justifications (visibilité, comparaison) que pour la visualisation 6."),
    html.Div(children=[
        html.Img(src='/assets/static/10.webp', className='icon'),
        html.P(children=[
            html.B("Figure 10."),
            html.Span(
                " Viz 7 lorsque le niveau d’étude « diplôme de certificat professionnel » est sélectionné.")
        ], className='figure-title'),
    ]),
    html.Div([
        html.H2("7. Références", id='references'),
        html.P(children=[
            html.Span(
                "[1] Fehrman, Elaine, Egan,Vincent, and Mirkes,Evgeny. (2016). Drug consumption (quantified). UCI Machine Learning Repository. "),
            html.A("https://doi.org/10.24432/C5TC7S",
                   href='https://doi.org/10.24432/C5TC7S',
                   target="_blank"),
            html.Span(". [Online]. Available: "),
            html.A("https://archive.ics.uci.edu/dataset/373/drug+consumption+quantified",
                   href='https://archive.ics.uci.edu/dataset/373/drug+consumption+quantified',
                   target="_blank"),
        ]),
        html.P("[2] Zuckerman, M., Kuhlman, D. M., Teta, P., Joireman, J., & Kraft, M. (1993). A comparison of three structural models of personality: the big three, the big five, and the alternative five. Journal of Personality and Social Psychology, 65, 757-768."),
        html.P(children=[
            html.Span(
                "[3] “SVG Repo - Free SVG Vectors and Icons,” SVG Repo. Accessed: Mar. 18, 2024. [Online]. Available: "),
            html.A("https://www.svgrepo.com",
                   href='https://www.svgrepo.com',
                   target="_blank"),
        ]),
    ]),
    dcc.Link('Découvrir les visualisations', href='/visualizations'),
    html.Div([
        html.Div([html.Div(author, className="typewrite")
                  for author in authors], style={'font-size': '12px', 'font-family': 'Courier New', 'textAlign': 'center'})
    ])
])


@callback(
    Output('url-forward-forward', 'pathname'),
    Input('forward-forward-button', 'n_clicks'),
    prevent_initial_call=True
)
def navigate_to_drugs(n_clicks):
    if n_clicks > 0:
        return '/drugs'
