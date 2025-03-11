import pandas as pd
from collections import Counter
import re

data = pd.read_csv("filtered_tweets_engie.csv", on_bad_lines='skip', delimiter=';')
data_sentiment = pd.read_csv("sanitized_tweets_sentiment.csv", on_bad_lines='skip', delimiter=',')

# Nettoyer les données
data['full_text'] = data['full_text'].str.lower()  # Convertir en minuscules
data['full_text'] = data['full_text'].str.replace(r'[^\w\s]', '')  # Enlever les caractères spéciaux

# Nettoyer les données
data['full_text'] = data['full_text'].str.lower()  # Convertir en minuscules
data['full_text'] = data['full_text'].str.replace(r'[^\w\s]', '')  # Enlever les caractères spéciaux

emoji_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # Emoticônes
    "\U0001F300-\U0001F5FF"  # Symboles & pictogrammes
    "\U0001F680-\U0001F6FF"  # Transport & cartes
    "\U0001F700-\U0001F77F"  # Symboles alchimiques
    "\U0001F780-\U0001F7FF"  # Divers symboles supplémentaires
    "\U0001F800-\U0001F8FF"  # Suppléments divers
    "\U0001F900-\U0001F9FF"  # Suppléments supplémentaires
    "\U0001FA00-\U0001FA6F"  # Objets divers
    "\U0001FA70-\U0001FAFF"  # Suppléments divers
    "\U00002702-\U000027B0"  # Dingbats
    "\U000024C2-\U0001F251"  # Autres symboles
    "]+", flags=re.UNICODE
)
pd.set_option('display.max_colwidth', None)

# Vérifier si la colonne 'full_text' existe avant de procéder
if "full_text" in data.columns:
    # Appliquer la suppression des emojis sur chaque ligne
    data["full_text"] = data["full_text"].astype(str).apply(lambda x: emoji_pattern.sub(r'', x))

# Extraction des plaintes
def extract_complaints(text):
    # Rechercher des mots-clés typiques de plaintes
    keywords = {
        'problèmes de facturation': ['facture', 'prélèvement', 'montant', 'erreur', 'régularisation', 'régularité', 'tarif', 'prix', 'augmentation', 'mensualisation', 'réduction', 'électricité', 'gaz', 'abonnement', 'kwh', 'consommation', 'régul', 'paiement', 'prelevement'],
        'pannes et urgences': ['gaz', 'électricité', 'eau chaude', 'urgent', 'urgence', 'panne', 'chauffage', 'chaudière', 'dépannage', 'intervention', 'coupure', 'courant', 'énergie', 'consommation', 'technicien', 'chauffe', 'eau', 'chaude', 'froid'],
        'service client injoignable': ['réponse', 'relance', 'appeler', 'plate-forme', 'téléphone', 'contact', 'demande', 'rappel', 'injoignable', 'disponible', 'disponibilité', 'service client', 'support', 'assistance', 'demande', 'rappel', 'rappel', 'contact', 'service', 'clients', 'injoignable'],
        'problèmes avec l’application': ['bug', 'appli', 'indisponibilité', 'application', 'connexion', 'déconnexion', 'erreur', 'planté', 'plante', 'serveur', 'fonctionne', 'fonctionner', 'accès', 'accéder', 'app', 'appli', 'connexion', 'serveur'],
        'délai d’intervention': ['attente', 'retard', 'demeure', 'semaines', 'jours', 'mois', 'délai', 'intervention', 'rendez-vous', 'rdv', 'rappel', 'traitement', 'traiter', 'rendez', 'vous', 'rdv', 'intervention', 'traitement']
    }
    complaints = []
    for category, kws in keywords.items():
        if any(kw in text for kw in kws):
            complaints.append(category)
    return complaints

data['complaints'] = data['full_text'].apply(extract_complaints)

# Calcul du score d'inconfort
def calculate_discomfort_score(complaints):
    scores = {
        'problèmes de facturation': 30,
        'pannes et urgences': 50,
        'service client injoignable': 40,
        'problèmes avec l’application': 20,
        'délai d’intervention': 60
    }
    total_score = sum(scores[complaint] for complaint in complaints if complaint in scores)
    return min(total_score, 100)  # Limiter le score à 100%

data['discomfort_score'] = data['complaints'].apply(calculate_discomfort_score)

# Analyse des plaintes
complaint_counts = Counter([category for categories in data['complaints'] for category in categories])

# Analyse du pourcentage de pl aintes par catégories
def pourcentage_complaints_by_category(category):
    return (complaint_counts[category] / len(data)) * 100

# Calculer le pourcentage pour chaque catégorie
pourcentage_complaints_by_categories = {category: pourcentage_complaints_by_category(category) for category in complaint_counts.keys()}

# Affichage des résultats
print(pourcentage_complaints_by_categories)

# Analyse de la répartition des sentiments
sentiments = ['Positif', 'Négatif', 'Neutre']
sentiment_counts = {sentiment: sum(data_sentiment['sentiment'] == sentiment) for sentiment in sentiments}
sentiment_percentages = {sentiment: (sentiment_counts[sentiment] / len(data_sentiment)) * 100 for sentiment in sentiments}

# Affichage des résultats
print(sentiment_percentages)

# Détection des tweets contenant des mots-clés critiques
keywords_critiques = ['délai', 'panne', 'urgence', 'scandale', 'arnaque', 'escroquerie', 'fraude', "scandaleux", "inacceptable", "impossible", "intolérable", "absurde", "ridicule", "honte", "honteux", "chaos", "chaotique", "catastrophe", "catastrophique", "désastre", "désastreux", "échec", "échoué", "problème", "problématique", "grave", "sérieux", "important", "critique", "difficile", "compliqué", "injuste", "injustice", "injustifié", "injustifiable", "injustifié"]
critical_tweets = data[data['full_text'].apply(lambda x: any(kw in x for kw in keywords_critiques))]
critical_tweets_percentage = (len(critical_tweets) / data['complaints'].count()) * 100

# Affichage des résultats
print(critical_tweets_percentage)

# Optionnel: Analyse des tendances
# Par exemple, analyser les plaintes par date

data['created_at'] = pd.to_datetime(data['created_at'], utc=True)
data['month'] = data['created_at'].dt.to_period('M')
complaint_trends = data.groupby('month')['complaints'].apply(lambda x: Counter([item for sublist in x for item in sublist])).reset_index()
print("Tendances des plaintes par mois:")
print(complaint_trends)

# Traitement de la colonne id
data['id'] = data['id'].apply(lambda x: float(x.replace(',', '.')))
data['id'] = data['id'].apply(lambda x: f'{x:.0f}')
data['id'] = data['id'].apply(lambda x: str(x)[:-13])

# Extraction des arobases mentionnés
data['mentions'] = data['full_text'].str.findall(r'@\w+')

# Suppression des arobase
data['full_text'] = data['full_text'].str.replace(r'@\w+', '', regex=True)

data.to_csv("sanitized_tweets.csv")

### Calcul des KPIs ###
data['date'] = data['created_at'].dt.date
data['month'] = data['created_at'].dt.to_period('M')

# Nombre de tweets par jour/semaine/mois
tweets_per_day = data['date'].value_counts().sort_index()
tweets_per_week = data.resample('W', on='created_at').size()
tweets_per_month = data.groupby('month').size()

# Fréquence des mentions des comptes Engie
mentions_per_day = data[data['full_text'].str.contains('@engie')]['date'].value_counts().sort_index()
mentions_per_week = data[data['full_text'].str.contains('@engie')].resample('W', on='created_at').size()
mentions_per_month = data[data['full_text'].str.contains('@engie')].groupby('month').size()

# Score d'inconfort moyen
average_discomfort_score = data['discomfort_score'].mean()

# Nombre de plaintes par catégorie
complaint_counts = Counter([complaint for complaints in data['complaints'] for complaint in complaints])

# Afficher les résultats
print("Nombre de tweets en moyenne par jour / semaine / mois :")
print(f"{tweets_per_day.mean()} / {tweets_per_week.mean()} / {tweets_per_month.mean()}")

print("\nFréquence des mentions des comptes Engie par jour / semaine / mois :")
print(f"{mentions_per_day.mean()} / {mentions_per_week.mean()} / {mentions_per_month.mean()}")

print("\nNombre de tweets contenant des mots-clés critiques:")
print(f"{len(critical_tweets)}/{data['complaints'].count()}")

print("\nScore d'inconfort moyen:")
print(average_discomfort_score)

print("\nNombre de plaintes par catégorie:")
for category, count in complaint_counts.items():
    print(f"{category}: {count} ({count/len(complaint_counts.keys())} %)")

# Afficher les pourcentages pour vérification
print("Pourcentage des plaintes par catégorie ajouté au CSV:")
for category, percentage in pourcentage_complaints_by_categories.items():
    print(f"{category}: {percentage:.2f}%")