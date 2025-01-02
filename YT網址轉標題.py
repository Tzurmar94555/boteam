import yt_dlp
from Change斜線 import change
def get_video_title(url):
    # 設定 yt-dlp 參數，僅提取影片的元數據
    ydl_opts = {
        'quiet': True,  # 不顯示過多的訊息
        'extract_flat': True,  # 僅提取元數據，不下載影片
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 獲取影片元數據
            info_dict = ydl.extract_info(url, download=False)
            # 取得影片標題
            video_title = info_dict.get('title', '未知影片名稱')
            return change(video_title)
    except Exception as e:
        print(f"發生錯誤: {e}")
        return None

# # 範例使用：
# url = "https://youtu.be/jF0Jm80Tsc4"
# title = get_video_title(url)
# if title:
#     print(f"影片名稱: {title}")
# else:
#     print("無法獲取影片名稱")
