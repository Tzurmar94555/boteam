import os
import json

def save_to_json(title, url, json_file):
    # 檢查是否已有 JSON 檔案
    if os.path.exists(json_file):
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
    else:
        data = []

    # 新增影片資訊
    data.append({"title": title, "url": url})

    # 寫回 JSON 檔案
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"已將影片資訊儲存至 {json_file}")


def check_in_json(query, json_file):
    """檢查影片名稱或網址是否存在於 JSON 檔案中"""
    if os.path.exists(json_file):
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        
        # 檢查是否有符合名稱或網址
        for entry in data:
            if entry["title"] == query or entry["url"] == query:
                return True  # 找到影片
    return False  # 未找到影片
