import os
import json
import requests

# Clé API YouTube (fausse clé pour l'exemple)
API_KEY = "AIzaSyCBWF3nogzvkfVL5Ujj7dHBFUju6lG5glg"
CHANNEL_ID = "UCH52AxYg8ZIJimd_vXDsZyQ"  # ID de la chaîne ArenaSoundTV

def get_playlist_id_by_name(channel_id, playlist_name):
    """Récupère l'ID d'une playlist spécifique en fonction de son nom."""
    url = f"https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId={channel_id}&key={API_KEY}&maxResults=50"
    response = requests.get(url).json()

    for playlist in response.get("items", []):
        if playlist["snippet"]["title"].lower() == playlist_name.lower():
            return playlist["id"]

    return None  # Retourne None si la playlist n'est pas trouvée

def fetch_all_videos(playlist_id):
    """Récupère toutes les vidéos d'une playlist spécifique sur YouTube."""
    all_videos = []
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

        # Extraire uniquement les vidéos de la playlist
        for item in response.get("items", []):
            snippet = item.get("snippet", {})
            video_id = snippet.get("resourceId", {}).get("videoId")
            title = snippet.get("title")
            published_at = snippet.get("publishedAt")

            if video_id:
                all_videos.append({
                    "title": title,
                    "videoId": video_id,
                    "publishedAt": published_at
                })

        # Vérifier s'il y a une page suivante
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break  # Fin de la pagination

    return all_videos

if __name__ == "__main__":
    playlist_name = "ARENA LIVE SETS"  # Nom exact de la playlist

    # Récupérer l'ID de la playlist
    playlist_id = get_playlist_id_by_name(CHANNEL_ID, playlist_name)

    if playlist_id:
        videos = fetch_all_videos(playlist_id)

        # Sauvegarder les vidéos dans un fichier JSON
        with open("videos.json", "w", encoding="utf-8") as f:
            json.dump(videos, f, indent=4, ensure_ascii=False)

        print(f"✅ {len(videos)} vidéos récupérées et enregistrées dans videos.json !")
    else:
        print(f"❌ La playlist '{playlist_name}' n'a pas été trouvée.")
