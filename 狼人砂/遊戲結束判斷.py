import json
from Bot import bot

# 載入玩家資料
def 讀取玩家資料(json_path="player.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

# 判斷是否所有狼人或非狼人的玩家都死亡
@bot.command()
async def 判斷遊戲結束(ctx, 狀態="死亡", json_path="player.json"):
    """判斷所有狼人的玩家是否全部死亡，或者非狼人的玩家是否全部死亡"""
    # 讀取玩家資料
    玩家資料 = 讀取玩家資料(json_path)

    狼人死亡 = True
    非狼人死亡 = True

    # 檢查所有玩家的狀態
    for data in 玩家資料.values():
        if data["職業"] == "狼人" and data["狀態"] != 狀態:
            狼人死亡 = False  # 有狼人尚未死亡
        elif data["職業"] != "狼人" and data["狀態"] != 狀態:
            非狼人死亡 = False  # 有非狼人尚未死亡

    if 狼人死亡:
        await ctx.send("所有狼人的玩家都已死亡，遊戲結束！狼人輸")
    elif 非狼人死亡:
        await ctx.send("所有非狼人的玩家都已死亡，遊戲結束！狼人勝利")
    else:
        await ctx.send("遊戲繼續中，還有玩家存活")
