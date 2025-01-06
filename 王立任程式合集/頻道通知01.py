import discord
import feedparser
import asyncio
from GPT  import test
# YouTube 頻道的 RSS URL
rss_url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCvg7f18afqzDIRTj3VMhWkA"
# rss_url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCRrImi1CRog9dttI2nM8nPg"
last_published = None

# 檢查是否有新影片的協程函數
async def check_new_video(client, channel_id):
    global last_published
    await client.wait_until_ready()
    channel = client.get_channel(channel_id)

    while not client.is_closed():
        feed = feedparser.parse(rss_url)
        if feed.entries:
            latest_entry = feed.entries[0]
            # print(latest_entry.title)
            # 如果有新影片，且發布時間不同於前次記錄
            if latest_entry.published != last_published:
                last_published = latest_entry.published
                # print(latest_entry.author)
                # x=test('幫我介紹'+latest_entry.title+'，這是'+latest_entry.author+'最新的影片，幫我根據標題，寫一串文本推薦給其他觀眾'+latest_entry.link)
                x=""
                await channel.send(f"📢 新影片發布！\n{latest_entry.title}\n觀看影片：{latest_entry.link}\n{x}")
        await asyncio.sleep(10)  # 每 5 分鐘檢查一次