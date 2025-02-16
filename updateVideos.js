const fs = require("fs");
const fetch = require("node-fetch");

const API_KEY = "AIzaSyCBWF3nogzvkfVL5Ujj7dHBFUju6lG5glg"; // Ta clé API YouTube
const CHANNEL_ID = "UCH52AxYg8ZIJimd_vXDsZyQ"; // ID de ta chaîne YouTube
const MAX_RESULTS = 6;
const JSON_FILE = "videos.json"; // Fichier JSON à mettre à jour

async function fetchYouTubeVideos() {
    try {
        const response = await fetch(`https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=${CHANNEL_ID}&maxResults=${MAX_RESULTS}&order=date&type=video&key=${API_KEY}`);
        const data = await response.json();

        if (!data.items) throw new Error("Aucune vidéo trouvée");

        let videos = data.items.map(video => ({
            id: video.id.videoId,
            title: video.snippet.title,
            thumbnail: video.snippet.thumbnails.high.url,
            link: `https://www.arenasound.tv/video/${video.id.videoId}`
        }));

        // Mettre à jour le fichier JSON
        fs.writeFileSync(JSON_FILE, JSON.stringify({ videos }, null, 2));

        console.log("✅ Fichier videos.json mis à jour avec succès !");
    } catch (error) {
        console.error("❌ Erreur lors de la récupération des vidéos :", error);
    }
}

fetchYouTubeVideos();
