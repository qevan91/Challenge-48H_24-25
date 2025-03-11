import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

# --- Charger les données ---
fichier_csv = "sanitized_tweets_sentiment.csv"

@st.cache_data
def load_data():
    return pd.read_csv(fichier_csv, sep=",", on_bad_lines="skip", encoding="utf-8")

df = load_data()

if df is not None:
    st.title("☁️ Nuage de Mots des Tweets")

    # --- Sélection de la colonne texte ---
    if "full_text" in df.columns:
        text = " ".join(df["full_text"].dropna())

        # --- Définir les mots à exclure ---
        mots_a_exclure = {"à", "de", "pour", "https", "la", "le", "les", "je", "sur", "ne", "ce", "pas", "et", "vous", "en", "faire", "fait", "dans", "moi", "c'est", "plus", "sans", "un", "des", "au", "par", "c est", "t", "c  est"
                          ,"co", "est", "alors", "que", "il", "nous", "ça", "n", "mon", "même", "suis", "ou", "m", "d", "ma", "mes", "êtes", "qu", "ils"
                          , "son", "vos", "du", "j'ai", "va", "ont", "car", "là", "nje", "l", "se", "n'est", "donc", "ni", "mais", "voir", "nvous", "une", "avez", "n'ai", "cette", "y", "dites", "plusieurs", "cher", 
                          "bonjour", "aucune", "aucun", "toute", "tout", "très", "tu", "peux", "entre", "sont", "j ai", "avoir", "quand", "c", "cela", "notre", "elle",
                          "peut", "sous", "aux", "chez", "votre", "part", "avec", "j  ai", "d'un", "tous", "tout", "toutes", "sa", "bon", "vais", "merde", "depuis", "dernière", "avant",
                          "soit", "mère", "parle", "non", "qu' il", "quel", "juste", "dit", "moins", "nj'ai", "j", "ai", "après", "qu'il", "où", "voulez", "comme", "engie", "engiepart", "engieconso", "engiepartsav"
                          , "engiepartfr", "engiegroup", "qui", "jour", "mois", "jamais", "rien", "été", "normal", "faut", "jours", "dire", "semaine", "deux", "si"}
        stopwords = STOPWORDS.union(mots_a_exclure)  # Ajouter à la liste par défaut

        # --- Générer le nuage de mots ---
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color="white",
            colormap="coolwarm",
            stopwords=stopwords  # Exclure les mots définis
        ).generate(text)

        # --- Afficher le nuage de mots ---
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")  # Masquer les axes
        st.pyplot(fig)

    else:
        st.error("⚠️ La colonne 'full_text' est introuvable dans le fichier.")

else:
    st.error("⚠️ Impossible de charger les données.")



