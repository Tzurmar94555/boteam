from Bot import bot
from 特定語音頻道刪除 import 刪除頻道
from 創建職業語音頻道 import 創建職業語音頻道
from 語音頻道轉移 import 傳送到職業頻道
from 大廳創建 import 創建大廳,移動玩家,刪除大廳 # type: ignore
from 大廳發言 import 大廳發言
from 大廳投票 import 大廳投票
from 禁音與解除 import 禁音大廳所有人, 解除禁音
from 輪流禁音 import 輪流禁音,計算玩家數量,解除所有人禁音
from 語音人數 import 語音頻道狀態
from 玩家死亡 import 修改玩家狀態
from 遊戲結束判斷 import 判斷遊戲結束
from 通用頻道開關 import 切換玩家頻道可見
from 按鈕投票邏輯 import 投票
import os
import time
import asyncio
import random
@bot.command()
async def 開始遊戲(ctx):
    await 刪除頻道(ctx,1)
    await 切換玩家頻道可見(ctx,"關")
    await 語音頻道狀態(ctx,1311589920632209438)
    await 創建大廳(ctx)
    while (await 判斷遊戲結束(ctx)==True):
        await 投票(ctx)
        await 創建職業語音頻道(ctx)
        await 大廳發言(ctx,"天黑請閉眼")
        await asyncio.sleep(15)
        print("45秒已過")
        if(await 判斷遊戲結束(ctx)==False):
            break
        await 移動玩家(ctx)
        await 刪除頻道(ctx)
        await 大廳發言(ctx,"投票時間已過")
        await 大廳發言(ctx,"天亮請睜眼")
        await 輪流禁音(ctx,random.randint(1,計算玩家數量()))
        await 大廳投票(ctx)
        await 解除所有人禁音(ctx,0)
        await asyncio.sleep(15)
    print("遊戲結束")
    await 解除所有人禁音(ctx)
    await 移動玩家(ctx)
    await 刪除頻道(ctx)
    await 切換玩家頻道可見(ctx,"開")
    await 大廳發言(ctx,"遊戲結束，30秒後刪除大廳")
    await asyncio.sleep(30)
    await 刪除大廳(ctx)


