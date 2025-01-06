import os
import requests

def save_image(image_url, save_path):
    # 如果目录不存在，创建它
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # 下载图像
    image_data = requests.get(image_url).content

    # 将图像保存到本地
    with open(save_path, "wb") as image_file:
        image_file.write(image_data)

    return save_path
