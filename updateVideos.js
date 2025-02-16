const fs = require('fs');
const fetch = require('node-fetch');

const API_KEY = "AIzaSyCBWF3nogzvkfVL5Ujj7dHBFUju6lG5glg";  // 🔥 Clé API de test
const CHANNEL_ID = "UCH52AxYg8ZIJimd_vXDsZyQ";  // 🔥 ID de la chaîne Arena Sound
const MAX_RESULTS = 50;  // Nombre max de vidéos par requête
const API_URL = "https://www.googleapis.com/youtube/v3/search";

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
                ).map(item => ({
                    id: item.id.videoId,
                    title: item.snippet.title,
                    thumbnail: item.snippet.thumbnails.high.url,
                    publishedAt: item.snippet.publishedAt
                }));

                videos = videos.concat(filteredVideos);
            }

            // Vérifier s'il y a une page suivante
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
