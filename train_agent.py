import os
import pandas as pd
import numpy as np
from mistralai import Mistral
import time

data = pd.read_csv("sanitized_tweets.csv", on_bad_lines='skip')
# initialisation du client Mistral
api_key = "avgxRmy1TsKOnsZXh75nuie5jDizDEEr"
model = "mistral-large-latest"

# I
client = Mistral(api_key=api_key)


csv = open("sanitized_tweets.csv", "r", encoding="utf-8")
csv_lines = csv.readlines()
csv_header = csv_lines.pop(0)
csv.close()

csv_content = ""
for tweet in csv_lines:
    while True:
        try:

            chat_response = client.agents.complete(
                agent_id="ag:e59f61ca:20250310:sentiment-de-tweet:797e5583",
                max_tokens=131072,
                messages=[{"role": "user", "content": tweet}]
            )

            csv_content += f"{chat_response.choices[0].message.content}\n"
            print(chat_response.choices[0].message.content)
            
            time.sleep(3)
            break  # Sort de la boucle en cas de succès

        except Exception as e:
            if "429" in str(e):  # Vérifie si l'erreur est bien une rate limit
                print("Rate limit atteinte. Pause...")
                time.sleep(120)  # Attend 2 minutes avant de réessayer
            else:
                print("Autre erreur :", e)
                break  # Si l'erreur est autre chose qu'un 429, arrête l'exécution
csv_sentiment = open("sanitized_tweets_sentiment.csv", "w", encoding="utf-8")
csv_sentiment.write(csv_header)
csv_sentiment.write(csv_content)
csv_sentiment.close()