import cv2
import numpy as np
import pyautogui
import random
import time
from template_matching import multi_scale_template_matching

def click_target_image(target_image_path, scale_range=(0.5, 1.5), step=0.1, threshold=0.8, click_offset_range=(-5, 5)):
    # 加載要檢測的目標圖像
    target_image = cv2.imread(target_image_path, cv2.IMREAD_GRAYSCALE)
    
    if target_image is None:
        raise FileNotFoundError(f"Cannot load image from path: {target_image_path}")
    
    while True:
        # 截圖
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

        # 多尺度模板匹配
        res, loc, w, h = multi_scale_template_matching(screenshot, target_image, scale_range, step, threshold)

        # 如果找到匹配圖像，則點擊
        if loc is not None:
            top_left = loc
            click_x = top_left[0] + w // 2
            click_y = top_left[1] + h // 2

            # 添加隨機偏移
            offset_x = random.randint(*click_offset_range)  # 根據需要調整偏移範圍
            offset_y = random.randint(*click_offset_range)  # 根據需要調整偏移範圍
            click_position = (click_x + offset_x, click_y + offset_y)

            # 點擊目標位置
            pyautogui.click(click_position)
            print(f"Clicked at position: {click_position}")

            # 停止檢測（根據需求進行調整）
            break

        # 每秒檢測一次
        time.sleep(1)
