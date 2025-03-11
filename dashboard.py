# import streamlit as st
# import pandas as pd

# # --- Charger un fichier CSV directement depuis son nom ---
# fichier_csv = "sanitized_tweets_sentiment.csv"  # Remplacez par le nom de votre fichier

# try:
#     df = pd.read_csv(fichier_csv, sep=";", on_bad_lines="skip", encoding="utf-8")  # ou sep="\t" si c'est un fichier TSV

#     # --- Afficher un aperçu des données ---
#     st.title("📂 Visualisation du fichier CSV")
#     st.subheader("📊 Aperçu des données :")
#     st.dataframe(df)  # Affiche le tableau interactif

#     # --- Statistiques de base ---
#     st.subheader("📈 Statistiques descriptives :")
#     st.write(df.describe())

#     # --- Sélection d'une colonne pour afficher un graphique ---
#     columns = df.columns.tolist()
#     selected_column = st.selectbox("Choisissez une colonne à visualiser", columns)

#     st.subheader(f"📉 Graphique de la colonne : {selected_column}")
#     st.line_chart(df[selected_column])  # Affiche un graphique de la colonne sélectionnée

#     st.success("✅ Fichier chargé avec succès !")

# except FileNotFoundError:
#     st.error(f"⚠️ Le fichier `{fichier_csv}` n'a pas été trouvé. Vérifiez son emplacement.")

import streamlit as st
import pandas as pd

# --- Charger le fichier CSV ---
fichier_csv = "sanitized_tweets_sentiment.csv"

df = pd.read_csv(fichier_csv, sep=",", on_bad_lines="skip", encoding="utf-8")

# --- Afficher un aperçu des données ---
st.title("📂 Dashboard interactif des tweets")

st.subheader("📊 Aperçu des données :")
st.dataframe(df.head())

# --- Sélectionner une colonne numérique pour le graphique ---
numeric_cols = df["sentiment"]
selected_numeric_col = st.selectbox("Choisissez une colonne numérique à visualiser", numeric_cols)

# --- Choisir le type de graphique ---
chart_type = st.radio(
    "Sélectionnez le type de graphique :",
    ('Graphique en ligne', 'Histogramme', 'Barres'))

st.subheader(f"📉 {chart_type} pour la colonne : {selected_numeric_col}")

# --- Afficher le graphique choisi ---
if chart_type == 'Graphique en ligne':
    st.line_chart(df["sentiment"])
elif chart_type == 'Histogramme':
    st.histogram_chart(df["sentiment"])
elif chart_type == 'Barres':
    st.bar_chart(df["sentiment"])

st.success("✅ Visualisation réussie !")

