import google.generativeai as genai

# 請替換成您實際的 API 金鑰
GOOGLE_API_KEY = "API 金鑰"

# 設定 API 金鑰
genai.configure(api_key=GOOGLE_API_KEY)

# 設定模型
model = genai.GenerativeModel('gemini-pro')

def ask_bot(prompt):
    """向模型提問並返回回應。"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"發生錯誤：{e}"
