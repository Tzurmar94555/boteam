import json
from Bot import bot
# 載入玩家資料
def 讀取玩家資料(json_path="player.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

# 根據序位修改玩家狀態
@bot.command()
async def 修改玩家狀態(ctx,序位:int, 新狀態="死亡", json_path="player.json"):
    # 讀取玩家資料
    玩家資料 = 讀取玩家資料(json_path)

    # 找到指定序位的玩家
    player_found = False
    for player_id, data in 玩家資料.items():
        if data["序位"] == 序位:  # 根據序位匹配
            玩家資料[player_id]["狀態"] = 新狀態
            player_found = True
            break  # 找到就退出循環

    if not player_found:
        print(f"找不到序位為 {序位} 的玩家")
        return False
    
    # 儲存回 JSON 文件
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(玩家資料, f, ensure_ascii=False, indent=4)

    print(f"序位 {序位} 的玩家狀態已改為 {新狀態}")
    return True

# 測試函式
# 修改序位為 1 的玩家狀態為 "存活"
# 修改玩家狀態_by_序位(1, "存活")
