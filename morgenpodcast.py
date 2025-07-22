#%% 
# Teaser von tagesschau.de zu podcast verarbeiten

import requests
from bs4 import BeautifulSoup
import pandas as pd





# %%


# Ziel-URL
url = "https://www.tagesschau.de"

# HTTP-Request
response = requests.get(url)
response.raise_for_status()

# HTML parsen
soup = BeautifulSoup(response.text, "html.parser")

# Ergebnisliste
data = []

# Alle relevanten Teaser-Links
for link_tag in soup.find_all("a", class_="teaser__link"):
    href = link_tag.get("href")
    full_url = url + href if href and href.startswith("/") else href

    # Topline und Headline extrahieren
    headline_wrapper = link_tag.find("h3")
    topline = headline_wrapper.find("span", class_="teaser__topline").get_text(strip=True) if headline_wrapper and headline_wrapper.find("span", class_="teaser__topline") else ""
    headline = headline_wrapper.find("span", class_="teaser__headline").get_text(strip=True) if headline_wrapper and headline_wrapper.find("span", class_="teaser__headline") else ""

    # Teaser-Text extrahieren
    teaser_p = link_tag.find("p", class_="teaser__shorttext")
    teaser_text = teaser_p.get_text(strip=True) if teaser_p else ""

    # Hinzufügen zur Datenliste
    data.append({
        "Topline": topline,
        "Headline": headline,
        "Teaser": teaser_text,
        "Link": full_url
    })

# DataFrame erzeugen
df = pd.DataFrame(data)

# Anzeigen
print(df)

# %%
df



# %%
import os
from openai import OpenAI

# AP-Key laden
api_key = os.getenv("API_KEY")
print("API-Key wurde geladen, Länge:", len(api_key))

# Client mit Key initialisieren
client = OpenAI(api_key=api_key)

# Kombiniere die Texte der ersten 10 Einträge
combined_text = ""
for index, row in df.head(10).iterrows():
    combined_text += f"{row['Topline']}: {row['Headline']}. {row['Teaser']}\n"

# Prompt definieren
prompt = (
    "Erstelle bitte ein ca. 5-minütiges Podcast-Skript auf Deutsch für Kinder im Alter von etwa 12 Jahren. "
    "Der Podcast soll unterhaltsam, einfach erklärt und spannend sein. "
    "Nutze die folgenden Nachrichten als Grundlage:\n\n"
    f"{combined_text}"
)

# Anfrage an ChatGPT mit neuer API
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Du bist ein professioneller Podcast-Autor für Kinder."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    max_tokens=1200
)

# Antwort extrahieren und anzeigen
podcast_script = response.choices[0].message.content

#%%
print(podcast_script)

#%%


# OpenAI-Client initialisieren
client = OpenAI(api_key=api_key)

# Podcast-Text (z. B. aus vorheriger Chat-Antwort)
text = podcast_script  # ← dein generierter Podcast-Text

# TTS-Anfrage an OpenAI
response = client.audio.speech.create(
    model="tts-1",
    voice="nova",  # Alternativen: "shimmer", "echo", "fable", "onyx", "alloy"
    input=text
)

# MP3-Datei speichern
with open("podcast_episode.mp3", "wb") as f:
    f.write(response.content)

print("🎧 Audio gespeichert als podcast_episode.mp3")
# %%
