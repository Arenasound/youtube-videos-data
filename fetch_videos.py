import os
import json
import requests

# Clé API YouTube (fausse clé donnée précédemment)
API_KEY = "AIzaSyCBWF3nogzvkfVL5Ujj7dHBFUju6lG5glg"
CHANNEL_ID = "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Remplace par l'ID de ta chaîne YouTube

def get_uploads_playlist_id():
    """Récupère l'ID de la playlist contenant toutes les vidéos uploadées."""
    url = f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={CHANNEL_ID}&key={API_KEY}"
    response = requests.get(url).json()

    try:
        return response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    except (KeyError, IndexError):
        print("❌ Impossible de récupérer la playlist des uploads.")
        return None

def fetch_all_videos(playlist_id):
    """Récupère toutes les vidéos de la playlist d'uploads, en supprimant les doublons et les vidéos non publiques."""
    all_videos = {}
    next_page_token = None
    base_url = "https://www.googleapis.com/youtube/v3/playlistItems"

    while True:
        params = {
            "key": API_KEY,
            "playlistId": playlist_id,
            "part": "snippet",
            "maxResults": 50,  # Maximum autorisé par requête
            "pageToken": next_page_token
        }

        response = requests.get(base_url, params=params).json()

        # Vérifier si l'API a retourné une erreur
        if "error" in response:
            print(f"❌ Erreur API : {response['error']['message']}")
            break

        # Extraire uniquement les vidéos uniques
        for item in response.get("items", []):
            snippet = item.get("snippet", {})
            video_id = snippet.get("resourceId", {}).get("videoId")
            title = snippet.get("title")
            published_at = snippet.get("publishedAt")

            # Vérifier que la vidéo n'est PAS un live, un short ou une playlist
            if video_id and video_id not in all_videos:
                if "LIVE" in title.upper() or "Shorts" in title or "Premiere" in title:
                    continue  # Ignore les lives et shorts
                all_videos[video_id] = {
                    "title": title,
                    "videoId": video_id,
                    "publishedAt": published_at
                }

        # Vérifier s'il y a une page suivante
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break  # Fin de la pagination

    return list(all_videos.values())

if __name__ == "__main__":
    playlist_id = get_uploads_playlist_id()
    
    if playlist_id:
        videos = fetch_all_videos(playlist_id)

        # Sauvegarder les vidéos dans un fichier JSON
        with open("videos.json", "w", encoding="utf-8") as f:
            json.dump(videos, f, indent=4, ensure_ascii=False)

        print(f"✅ {len(videos)} vidéos récupérées et enregistrées dans videos.json !")
    else:
        print("❌ Aucune vidéo récupérée.")
