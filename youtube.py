import yt_dlp
from youtubesearchpython import VideosSearch
import os

class YouTubeAPI:
    def __init__(self):
        self.download_path = "downloads"
        self.cookies = "cookies.txt"  # Ensure this file exists
        os.makedirs(self.download_path, exist_ok=True)

    async def track(self, query: str):
        # Resolve query to video ID
        if "youtube.com/watch?v=" in query or "youtu.be/" in query:
            video_id = query.split("v=")[-1].split("&")[0] if "v=" in query else query.split("/")[-1]
        else:
            search = VideosSearch(query, limit=1)
            result = (await search.next())["result"][0]
            video_id = result["id"]

        info = await self.download_audio(video_id)

        track_data = {
            "title": info.get("title"),
            "link": f"https://www.youtube.com/watch?v={video_id}",
            "thumb": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
            "filepath": info.get("filepath"),
            "vidid": video_id,
        }
        return track_data, video_id

    async def download_audio(self, video_id):
        filename = f"{video_id}.webm"  # We'll get high quality .webm audio
        out_path = os.path.join(self.download_path, filename)

        if os.path.exists(out_path):
            return {"title": video_id, "filepath": out_path}

        ydl_opts = {
            'format': 'bestaudio[ext=webm]/bestaudio/best',
            'outtmpl': out_path,
            'noplaylist': True,
            'quiet': True,
            'cookiefile': self.cookies,
            'postprocessors': [],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=True)
            return {
                "title": info_dict.get("title"),
                "filepath": out_path
            }
