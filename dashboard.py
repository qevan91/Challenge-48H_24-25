import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter

# --- Charger les données ---
data = pd.read_csv("filtered_tweets_engie.csv", delimiter=';', on_bad_lines='skip')
data_sentiment = pd.read_csv("sanitized_tweets_sentiment.csv", delimiter=',', on_bad_lines='skip')

# Convertir les dates
if 'created_at' in data.columns:
    data['created_at'] = pd.to_datetime(data['created_at'], utc=True)
    data['date'] = data['created_at'].dt.date

st.title("📊 Dashboard des tweets")

# --- Graphique : Nombre de tweets par jour ---
st.subheader("📆 Nombre de tweets par mois")
data['month'] = data['created_at'].dt.to_period('M')
tweets_per_month = data['month'].value_counts().sort_index()
fig, ax = plt.subplots()
ax.plot(tweets_per_month.index.astype(str), tweets_per_month.values, marker='o', linestyle='-')
ax.set_xlabel("Mois")
ax.set_ylabel("Nombre de tweets")
ax.set_title("Nombre de tweets par mois")
plt.xticks(rotation=45)
st.pyplot(fig)
# --- Graphique : Répartition des sentiments ---
st.subheader("😊 Répartition des sentiments")
sentiments = ['Positif', 'Négatif', 'Neutre']
sentiment_counts = [sum(data_sentiment['sentiment'] == sentiment) for sentiment in sentiments]
fig, ax = plt.subplots()
ax.pie(sentiment_counts, labels=sentiments, startangle=90, colors=['green', 'red', 'gray'])
ax.set_title("Répartition des tweets par sentiment")
st.pyplot(fig)

# --- Graphique : Mots les plus utilisés dans les plaintes ---


# --- Graphique : Pourcentage de tweets avec des mots-clés critiques ---
st.subheader("⚠️ Pourcentage de tweets critiques")
keywords_critiques = ['délai', 'panne', 'urgence', 'scandale', 'arnaque', 'fraude', 'problème', 'grave', 'critique']
critical_tweets = data[data['full_text'].apply(lambda x: any(kw in str(x) for kw in keywords_critiques))]
critical_percentage = (len(critical_tweets) / len(data)) * 100
st.metric(label="Tweets critiques", value=f"{critical_percentage:.2f}%")

# --- Graphique : Volume de plaintes par utilisateur ---
st.subheader("👥 Volume de plaintes par utilisateur")
if 'user_screen_name' in data.columns:
    top_complainers = data['user_screen_name'].value_counts().nlargest(10)
    fig, ax = plt.subplots()
    ax.bar(top_complainers.index, top_complainers.values, color='blue')
    ax.set_xlabel("Utilisateur")
    ax.set_ylabel("Nombre de plaintes")
    ax.set_title("Top 10 des utilisateurs ayant déposé le plus de plaintes")
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.success("✅ Dashboard mis à jour avec succès !")


