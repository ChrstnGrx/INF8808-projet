# Projet INF8808

Ce projet est une analyse pour la prévention et l'éducation à la consommation de drogues. Les données unilisées pour ce projet peuvent être retrouvées à l'adresse suivante : `https://archive.ics.uci.edu/dataset/373/drug+consumption+quantified`.
Le projet propose plusieurs visualisations qui permettent une analyse des différentes drogues considérées mais aussi une analyse démographique des consommateurs.

Le projet est fait en python et utilise plotly/dash.

## Développement local

### Prérequis

- Python >= 3.8

### Lancement du projet

À la racine du projet :

- Installer virtualenv : `python -m pip install --user virtualenv`
- Créer un environnement virtuel : `python -m venv venv`.
- Activer l'environnement virtuel
  - sur Windows : `venv/Scripts/activate`
  - sur macOS et Linux : `source venv/bin/activate`
- Installer les dépendances
  - sur Windows : `pip install -r requirements.windows.txt`
  - sur macOS et Linux : `pip install -r requirements.txt`
- Lancer le projet : `python server.py`. Le serveur est accessible à travers `localhost:8050/`.
* Il est aussi possible de lancer le projet via le script `./start.sh`