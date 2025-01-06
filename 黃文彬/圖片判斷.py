import google.generativeai as genai
from PIL import Image
import os

# 請替換成您實際的 API 金鑰
GOOGLE_API_KEY = ""

# 設定 API 金鑰
genai.configure(api_key=GOOGLE_API_KEY)

# 設定模型 (使用 gemini-pro-vision 來處理圖片)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

def ask_bot_with_image(image_path, prompt="如果這張圖的角色是原神的角色，請以這是原神的某某來回答，如果不是的話，請不要提到原神這兩個字，我會用if '原神' in x:判斷你的回答。"):
    """向模型提問並附帶圖片，返回回應。"""
    try:
        if not os.path.exists(image_path):
           return "圖片路徑錯誤，找不到該圖片。"

        image = Image.open(image_path)
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"發生錯誤：{e}"

if __name__ == "__main__":
    print("歡迎使用 Google Generative AI 圖片機器人!")
    while True:
        image_path = input("請輸入圖片路徑 (或輸入 exit 結束): ")
        if image_path.lower() in ["exit", "quit", "結束"]:
            print("機器人: 再見！")
            break
        prompt = input("請輸入針對圖片的提問: ")
        bot_response = ask_bot_with_image(image_path, prompt)
        print("機器人:", bot_response)