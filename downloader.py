import yt_dlp
import os
from json_handler import save_to_json
from YT網址轉標題 import get_video_title
def download_youtube_as_mp3(video_url, output_folder="music", json_file="download_history.json"):
    # 確保資料夾存在
    os.makedirs(output_folder, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_folder}/{get_video_title(video_url)}.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        video_title2 = info.get("title", "Unknown Title")
        video_title = get_video_title(video_url)
    
    # 呼叫 JSON 儲存函式
    save_to_json(video_title2, video_url, json_file)
    print(f"已下載影片: {video_title}")
    return video_title
