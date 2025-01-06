import discord
from 禁音與解除 import 禁音大廳所有人, 解除禁音
import json
import asyncio
from Bot import bot
def 讀取玩家資料(json_path="player.json"):
    """讀取 player.json 檔案並返回玩家資料"""
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def 計算玩家數量(json_path="player.json"):
    """計算 player.json 中玩家的數量"""
    玩家資料 = 讀取玩家資料(json_path)
    return len(玩家資料)  # 玩家數量為鍵的數量

def 根據序位取得玩家(玩家資料, 序位):
    for 玩家ID, 資料 in 玩家資料.items():
        if 資料["序位"] == 序位:
            return 玩家ID, 資料
    return None, None

@bot.command()
async def 輪流禁音(ctx, x=1):
    玩家資料 = 讀取玩家資料()
    total_players = 計算玩家數量()
    for i in range(1, total_players + 1):  # 由於序號是從1開始，所以從1開始迴圈
        await 禁音大廳所有人(ctx)
        # 解除禁音（根據循環進行的邏輯）
        target_index = (i + x - 1) % total_players + 1 # 調整為1開始的索引  
        玩家ID,資料 = 根據序位取得玩家(玩家資料, target_index)
        if 玩家資料[玩家ID]["狀態"] == "存活":
            await 解除禁音(ctx, target_index)

        # 等待 10 秒
        await asyncio.sleep(3)

    # 完成後再次禁音所有人
    await 禁音大廳所有人(ctx)

@bot.command()
async def 解除所有人禁音(ctx, x=1):
    玩家資料 = 讀取玩家資料()
    total_players = 計算玩家數量()

    if x == 1:
        for i in range(1, total_players + 1):  # 由於序號是從1開始，所以從1開始迴圈
            await 解除禁音(ctx, i)
    else:
        for i in range(1, total_players + 1):  # 由於序號是從1開始，所以從1開始迴圈
            玩家資料 = 讀取玩家資料()
            玩家ID,資料 = 根據序位取得玩家(玩家資料, i)
            if 玩家資料[玩家ID]["狀態"] == "存活":
                await 解除禁音(ctx, i)
