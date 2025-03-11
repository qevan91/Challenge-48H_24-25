# Hackathon : Analyse des tweets clients d'Engie et paramétrage d'Agents IA

## 1. Introduction

Ce projet a été réalisé dans le cadre d'un hackathon visant à analyser les tweets adressés au service client d'Engie. L'objectif principal est d'extraire des indicateurs clés de performance (KPI), de réaliser une analyse de sentiment, et de paramétrer des agents IA (Mistral/Gemini) pour automatiser la classification des plaintes. Enfin, un tableau de bord interactif a été mis en place pour visualiser les résultats.

## 2. Méthodologie

### Prétraitement des données

Utilisation de filtres regex sur la colonne full_text pour exclure les contenus indésirables.

Conversion des formats de date et d'identifiants pour assurer la cohérence des données.

Extraction des mots-clés critiques afin de determiner quelles plaintes sont les plus incapacitantes

### Calcul des KPI

Fréquence des tweets (à partir de la colonne created_at).

Détection des tweets contenant des mots-clés critiques ("délai", "panne", "urgence", "scandale", "arnaque", etc.).

### Analyse de sentiment

Mise en place d'un agent IA pour classifier les tweets en Positif, Neutre ou Négatif.

Visualisation de la répartition des sentiments.

### Paramétrage des agents IA

Deux agents IA ont été paramétrés :

Agent d'analyse de sentiment : pour classifier les tweets selon leur tonalité.

Agent de catégorisation des plaintes : pour identifier le type de problème (facturation, pannes, service client, application, délais d'intervention, etc.).

Attribution d'un score d'inconfort (0-100%) en fonction de la gravité des plaintes et de leurs catégories.

### Création du tableau de bord

Une fois les KPI calculés et les tweets classifiés, un tableau de bord interactif a été développé avec Streamlit.

Visualisation des KPI sous forme de graphiques dynamiques.

## 3. Technologies utilisées

Agent IA : API Mistral + fichiers Jupyter Notebook.

Stockage des données : Fichiers CSV.

Traitement de texte : Regex pour le filtrage et l'extraction d'informations.

Dashboard : Streamlit pour l'affichage interactif des données.

## 4. Exécuter le projet

### Prérequis

Assurez-vous d'avoir installé les dépendances nécessaires via :

pip install -r requirements.txt

### Lancer le tableau de bord

Pour exécuter le dashboard avec Streamlit :

streamlit run dashboard.py

## 5. Résultats attendus

Identification des tendances et des problèmes récurrents des clients Engie.

Classification automatique des tweets en fonction des catégories de plaintes.

Analyse de sentiment pour comprendre la perception des clients.

Restitution claire des données via un tableau de bord interactif.

## 6. Auteurs et contributions

Merci à tous les participants du hackathon pour leur contribution à ce projet ! Si vous souhaitez améliorer le projet ou poser des questions, n'hésitez pas à ouvrir une issue sur le dépôt GitHub.