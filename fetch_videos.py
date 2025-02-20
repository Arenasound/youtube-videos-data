import os
import json
import requests

# Clé API YouTube (fausse clé donnée précédemment)
API_KEY = "AIzaSyCBWF3nogzvkfVL5Ujj7dHBFUju6lG5glg"
CHANNEL_ID = "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Remplace par l'ID de ta chaîne YouTube

def fetch_all_videos():
    all_videos = []
    next_page_token = None
    base_url = "https://www.googleapis.com/youtube/v3/search"

    while True:
        # Construire l'URL avec la pagination
        params = {
            "key": API_KEY,
            "channelId": CHANNEL_ID,
            "part": "snippet,id",
            "order": "date",
            "maxResults": 50,  # Maximum autorisé par requête
            "pageToken": next_page_token
        }

        response = requests.get(base_url, params=params)

        if response.status_code != 200:
            print(f"❌ Erreur API : {response.status_code}")
            print(response.text)
            break  # Sort de la boucle en cas d'erreur API

        data = response.json()

        # Extraire les vidéos de la réponse
        videos = [
            {
                "title": item["snippet"]["title"],
                "videoId": item["id"]["videoId"],
                "publishedAt": item["snippet"]["publishedAt"]
            }
            for item in data.get("items", []) if "videoId" in item["id"]
        ]

        all_videos.extend(videos)  # Ajouter les vidéos récupérées

        # Vérifier s'il y a une page suivante
        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break  # Sort de la boucle si toutes les vidéos sont récupérées

    # Sauvegarder toutes les vidéos dans un fichier JSON
    with open("videos.json", "w", encoding="utf-8") as f:
        json.dump(all_videos, f, indent=4, ensure_ascii=False)

    print(f"✅ {len(all_videos)} vidéos récupérées et enregistrées dans videos.json !")

if __name__ == "__main__":
    fetch_all_videos()
