import pandas as pd
from collections import Counter


data = pd.read_csv("filtered_tweets_engie.csv", on_bad_lines='skip', delimiter=';')

# Nettoyer les données
data['full_text'] = data['full_text'].str.lower()  # Convertir en minuscules
data['full_text'] = data['full_text'].str.replace(r'[^\w\s]', '')  # Enlever les caractères spéciaux

# Extraction des plaintes
def extract_complaints(text):
    # Rechercher des mots-clés typiques de plaintes
    keywords = {
        'problèmes de facturation': ['facture', 'prélèvement', 'montant', 'erreur'],
        'pannes et urgences': ['gaz', 'électricité', 'eau chaude', 'urgent'],
        'service client injoignable': ['réponse', 'relance', 'appeler', 'plate-forme'],
        'problèmes avec l’application': ['bug', 'appli', 'indisponibilité'],
        'délai d’intervention': ['attente', 'retard', 'demeure', 'semaines']
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

# Catégorisation des plaintes
categories = {
    'délais de réponse': ['attente', 'demeure'],
    'problèmes techniques': ['bug', 'problème'],
    'service client': ['comprendre', 'scandaleux'],
    'urgent': ['urgent', 'honte']
}

def categorize_complaints(complaints):
    categorized = []
    for category, keywords in categories.items():
        if any(keyword in complaints for keyword in keywords):
            categorized.append(category)
    return categorized

data['complaint_categories'] = data['complaints'].apply(categorize_complaints)

# Analyse des plaintes
complaint_counts = Counter([category for categories in data['complaint_categories'] for category in categories])

# Afficher les résultats
print("Nombre de plaintes par catégorie:")
for category, count in complaint_counts.items():
    print(f"{category}: {count}")

# Optionnel: Analyse des tendances
# Par exemple, analyser les plaintes par date
data['created_at'] = pd.to_datetime(data['created_at'])
data['month'] = data['created_at'].dt.to_period('M')
complaint_trends = data.groupby('month')['complaint_categories'].apply(lambda x: Counter([item for sublist in x for item in sublist])).reset_index()
print("Tendances des plaintes par mois:")
print(complaint_trends)