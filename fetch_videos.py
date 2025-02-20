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

def get_video_status(video_ids):
    """Récupère le statut de visibilité (public, privé, non répertorié) des vidéos."""
    base_url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "key": API_KEY,
        "id": ",".join(video_ids),  # Liste des videoIds séparés par une virgule
        "part": "status"
    }
    response = requests.get(base_url, params=params).json()

    video_statuses = {}
    for item in response.get("items", []):
        video_id = item["id"]
        privacy_status = item["status"]["privacyStatus"]  # public, private, unlisted
        video_statuses[video_id] = privacy_status

    return video_statuses

def fetch_all_videos(playlist_id):
    """Récupère toutes les vidéos d'une playlist spécifique sur YouTube, en excluant les vidéos privées, non répertoriées et planifiées."""
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

        # Récupérer les IDs des vidéos pour vérifier leur statut
        video_ids = []
        videos_data = []
        for item in response.get("items", []):
            snippet = item.get("snippet", {})
            video_id = snippet.get("resourceId", {}).get("videoId")
            title = snippet.get("title")
            published_at = snippet.get("publishedAt")

            if video_id and title:
                video_ids.append(video_id)
                videos_data.append({
                    "title": title,
                    "videoId": video_id,
                    "publishedAt": published_at
                })

        # Vérifier le statut de chaque vidéo
        if video_ids:
            video_statuses = get_video_status(video_ids)
            for video in videos_data:
                status = video_statuses.get(video["videoId"], "unknown")
                if status == "public":
                    all_videos.append(video)  # Ajouter uniquement les vidéos publiques

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

        print(f"✅ {len(videos)} vidéos publiques récupérées et enregistrées dans videos.json !")
    else:
        print(f"❌ La playlist '{playlist_name}' n'a pas été trouvée.")
