import os
import json
import requests

# Clé API YouTube (fausse clé pour l'exemple)
API_KEY = "AIzaSyD-FALSE-API-KEY-EXAMPLE123456789"
CHANNEL_ID = "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Remplace par l'ID de ta chaîne YouTube

def fetch_videos():
    url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults=10"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        videos = [
            {
                "title": item["snippet"]["title"],
                "videoId": item["id"]["videoId"],
                "publishedAt": item["snippet"]["publishedAt"]
            }
            for item in data.get("items", []) if "videoId" in item["id"]
        ]

        with open("videos.json", "w", encoding="utf-8") as f:
            json.dump(videos, f, indent=4, ensure_ascii=False)
        
        print("✅ Fichier videos.json mis à jour avec succès !")

    else:
        print(f"❌ Erreur API : {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    fetch_videos()
