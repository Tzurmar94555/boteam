import json
import random
from dotenv import load_dotenv
import os
from Bot import bot

# 讀取 player.json 的資料，如果檔案不存在則創建
def load_player_data():
    player_file = 'player.json'
    if os.path.exists(player_file):
        with open(player_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# 寫入資料到 player.json
def save_player_data(data):
    player_file = 'player.json'
    with open(player_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)



# 抓取 player.json 資料並隨機分配職業
def assign_random_jobs():
    player_data = load_player_data()  # 讀取現有資料
    updated_data = {}  # 儲存更新後的資料
    # 隨機職業列表
    職業選項 = ["預言家", "守衛", "平民1", "平民2", "狼人", "狼人"]
    for player_id, player_info in player_data.items():
        # 隨機選擇職業
        x = random.randint(0, len(職業選項)-1)
        player_info["職業"] = 職業選項[x]
        職業選項.pop(x)
        updated_data[player_id] = player_info  # 更新資料

    # 儲存更新後的資料回 player.json
    save_player_data(updated_data)

# # 示範使用
# assign_random_jobs()
# print("已隨機分配職業並儲存至 player.json")
