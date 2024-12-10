from Bot import bot
from 特定語音頻道刪除 import 刪除特定語音頻道
from 創建職業語音頻道 import 創建職業語音頻道
from 語音頻道轉移 import 傳送到職業頻道
from 大廳創建 import 創建大廳 # type: ignore
from 禁音與解除 import 禁音大廳所有人, 解除禁音
from 輪流禁音 import 輪流禁音
from 語音人數 import 語音頻道狀態
from 玩家死亡 import 修改玩家狀態
from 遊戲結束判斷 import 判斷遊戲結束
from 通用頻道開關 import 切換玩家頻道可見
import os
import time
@bot.command()
async def 開始遊戲(ctx):
    await 語音頻道狀態(ctx,1311589920632209438)
    await 創建職業語音頻道(ctx)
    time.sleep(5)
    await 創建大廳(ctx)
    await 輪流禁音(ctx)
    await 傳送到職業頻道(ctx)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(DISCORD_TOKEN)

