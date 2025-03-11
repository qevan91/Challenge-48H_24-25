import os
import pandas as pd
import numpy as np
from mistralai import Mistral
import time
import json

data = pd.read_csv("sanitized_tweets_sentiment.csv", on_bad_lines='skip')

def empty_complaints():
    return "[]"

def reset_discomfort_score():
    return 0

data["complaints"] = data["complaints"].apply(empty_complaints)
data["discomfort_score"] = data["discomfort_score"].apply(reset_discomfort_score)

data.to_csv("sanitized_tweets_without_complaints_type.csv", index=False)

api_key = "avgxRmy1TsKOnsZXh75nuie5jDizDEEr"
model = "mistral-large-latest"
agent_id = "ag:e59f61ca:20250311:categorisation-de-problemes:19714d72"

client = Mistral(api_key=api_key)

chat_response = client.agents.complete(
                agent_id=agent_id,
                max_tokens=131072,
                response_format={
                    "type": "json_object",
                    },
                messages=[{"role": "user", "content": data.loc[0].to_json()}]
            )

print(chat_response.choices[0].message.content)

json_data_categorized = []

for i in range(len(data.index)):
    while True:
        try:
            chat_response = client.agents.complete(
                        agent_id=agent_id,
                        max_tokens=131072,
                        response_format={
                            "type": "json_object",
                            },
                        messages=[{"role": "user", "content": data.loc[i].to_json()}]
                    )

            json_data_categorized.append(json.loads(chat_response.choices[0].message.content))
            time.sleep(2)
            if i % 100 == 0:
                print(f"Tweet {i} processed")

            break


        except Exception as e:
            if "429" in str(e):  # rate limit
                print("Rate limit atteinte. Pause...")
                time.sleep(120)
            else:
                print("Autre erreur :", e)
                break
            
json_better_categorisation = json.dumps(json_data_categorized, indent=4)
with open("better_categorisation.json", "w") as f:
    f.write(json_better_categorisation)
    f.close()
new_df = pd.read_json("better_categorisation.json")
new_df = pd.DataFrame(json_data_categorized)
new_df.to_csv("better_categorisation.csv", index=False)
