from 禁音與解除 import 禁音大廳所有人, 解除禁音
import time
from Bot import bot
import json

def 讀取玩家資料(json_path="player.json"):
    """讀取 player.json 檔案並返回玩家資料"""
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def 計算玩家數量(json_path="player.json"):
    """計算 player.json 中玩家的數量"""
    玩家資料 = 讀取玩家資料(json_path)
    return len(玩家資料)  # 玩家數量為鍵的數量

@bot.command()
async def 輪流禁音(ctx,x=1):
    for i in range(0,計算玩家數量()):
        await 禁音大廳所有人(ctx)
        if(i+x>計算玩家數量()):
            await 解除禁音(ctx,i+x-計算玩家數量())
        else:
            await 解除禁音(ctx,i+x)
        time.sleep(3)
    await 禁音大廳所有人(ctx)