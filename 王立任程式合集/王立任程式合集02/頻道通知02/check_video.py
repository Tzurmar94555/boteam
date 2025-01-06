import feedparser
from ask_bot import ask_bot

# YouTube 頻道的 RSS URL
rss_url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCvg7f18afqzDIRTj3VMhWkA"
last_published = None

@bot.command()
async def check_new_video(ctx, channel_id: int = 1241269097396834304):
    global last_published

    # 獲取 Discord 頻道物件
    channel = bot.get_channel(channel_id)
    if not channel:
        await ctx.send(f"找不到頻道 ID：{channel_id}")
        return

    # 解析 RSS Feed
    feed = feedparser.parse(rss_url)
    if feed.entries:
        latest_entry = feed.entries[0]
        if latest_entry.published != last_published:
            # 如果有新影片，記錄發布時間並發送通知
            last_published = latest_entry.published
            x = ask_bot(latest_entry.title + "，這是我的影片標題，請依照這標題，幫我寫一串介紹詞")  # 根據需要生成推薦文本
            await channel.send(
                f"📢 新影片發布！\n{latest_entry.title}\n觀看影片：{latest_entry.link}\n{x}"
            )
            # await ctx.send("新影片通知已發送！")
    else:
        await ctx.send("無法從 RSS 中獲取影片資訊，請檢查 RSS URL。")
