const fs = require('fs');
const fetch = require('node-fetch');

const API_KEY = "AIzaSyCBWF3nogzvkfVL5Ujj7dHBFUju6lG5glg";  // 🔥 Clé API de test
const CHANNEL_ID = "UCH52AxYg8ZIJimd_vXDsZyQ";  // 🔥 ID de la chaîne Arena Sound
const MAX_RESULTS = 50;  // Nombre max de vidéos par requête
const API_URL = "https://www.googleapis.com/youtube/v3/search";
const COMMENT_API_URL = "https://www.googleapis.com/youtube/v3/commentThreads";
const VIDEO_STATS_URL = "https://www.googleapis.com/youtube/v3/videos";

// Fonction pour récupérer les commentaires d'une vidéo
async function fetchComments(videoId) {
    const url = `${COMMENT_API_URL}?part=snippet&videoId=${videoId}&maxResults=100&key=${API_KEY}`;
    const response = await fetch(url);
    const data = await response.json();
    return data.items.map(item => item.snippet.topLevelComment.snippet.textDisplay);  // Récupérer les commentaires
}

// Fonction pour récupérer les statistiques de la vidéo (y compris les likes)
async function fetchVideoStats(videoId) {
    const url = `${VIDEO_STATS_URL}?part=statistics&id=${videoId}&key=${API_KEY}`;
    const response = await fetch(url);
    const data = await response.json();
    const videoStats = data.items[0]?.statistics;
    return videoStats ? {
        likes: videoStats.likeCount,
        views: videoStats.viewCount,
    } : { likes: 0, views: 0 };
}

// Fonction pour récupérer toutes les vidéos
async function fetchAllVideos() {
    let videos = [];
    let nextPageToken = '';

    try {
        do {
            // 🔗 URL pour récupérer les vidéos
            const url = `${API_URL}?part=snippet&channelId=${CHANNEL_ID}&maxResults=${MAX_RESULTS}&order=date&type=video&pageToken=${nextPageToken}&key=${API_KEY}`;
            const response = await fetch(url);
            const data = await response.json();

            if (data.items) {
                // 📌 Filtrer les Shorts en excluant les vidéos dont le titre ou la description contient "Shorts"
                const filteredVideos = data.items.filter(item => 
                    !item.snippet.title.toLowerCase().includes("shorts") &&
                    !item.snippet.description?.toLowerCase().includes("shorts")
                ).map(async (item) => {
                    const comments = await fetchComments(item.id.videoId);  // Récupérer les commentaires
                    const stats = await fetchVideoStats(item.id.videoId);  // Récupérer les statistiques (likes)
                    return {
                        id: item.id.videoId,
                        title: item.snippet.title,
                        thumbnail: item.snippet.thumbnails.high.url,
                        description: item.snippet.description,  // Ajouter la description
                        comments: comments,  // Ajouter les commentaires
                        likes: stats.likes,  // Ajouter le nombre de likes
                        views: stats.views,  // Ajouter le nombre de vues
                        publishedAt: item.snippet.publishedAt
                    };
                });

                // Résoudre toutes les promesses d'asynchrone dans filteredVideos
                const resolvedVideos = await Promise.all(filteredVideos);
                videos = videos.concat(resolvedVideos);
            }

            nextPageToken = data.nextPageToken || '';
        } while (nextPageToken);  // 🔄 Boucle jusqu'à ce qu'il n'y ait plus de vidéos

        // 📁 Sauvegarde dans le fichier videos.json
        fs.writeFileSync('videos.json', JSON.stringify(videos, null, 2));
        console.log("✅ Fichier videos.json mis à jour avec toutes les vidéos !");
    } catch (error) {
        console.error("❌ Erreur lors de la récupération des vidéos :", error);
    }
}

// Lancer la récupération des vidéos
fetchAllVideos();
