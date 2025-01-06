import os
from openai import AzureOpenAI
import json
import requests
from utils.file_utils import save_image
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中读取密钥
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")

class AzureClient:
    def __init__(self):
        self.client = AzureOpenAI(
            api_version=AZURE_API_VERSION,
            api_key=AZURE_API_KEY,
            azure_endpoint=AZURE_ENDPOINT
        )

    def generate_image(self, prompt):
        # 调用 DALL-E 生成图像
        result = self.client.images.generate(
            model="dall-e-3",  # the name of your DALL-E 3 deployment
            prompt=prompt,
            n=1
        )

        json_response = json.loads(result.model_dump_json())
        image_url = json_response["data"][0]["url"]

        # 保存生成的图像
        return save_image(image_url, 'static/generated_image.png')
