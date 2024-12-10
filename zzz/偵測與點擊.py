import cv2
import numpy as np
import pyautogui
import random
import keyboard  # 用來模擬鍵盤按鍵
import mouse     # 用來模擬滑鼠按鍵
import time
from template_matching import multi_scale_template_matching  # 假設你已經有此函式

def trigger_on_image_detection(target_image_path, action_type='keyboard', key='space', mouse_button='left',
                               scale_range=(0.5, 2.0), step=0.1, threshold=0.6, click_offset_range=(-5, 5)):
    """
    偵測到螢幕上出現指定圖像後，觸發鍵盤或滑鼠按鍵。

    :param target_image_path: 要檢測的目標圖像路徑
    :param action_type: 'keyboard' 或 'mouse'，表示偵測到時要觸發的動作類型
    :param key: 如果是鍵盤動作，這裡指定按下的按鍵名稱
    :param mouse_button: 如果是滑鼠動作，這裡指定要點擊的滑鼠按鍵 ('left' or 'right')
    :param scale_range: 縮放範圍，用於多尺度模板匹配
    :param step: 縮放的步長
    :param threshold: 模板匹配的相似度門檻
    :param click_offset_range: 點擊位置的隨機偏移範圍
    """
    
    # 加載目標圖像
    target_image = cv2.imread(target_image_path, cv2.IMREAD_GRAYSCALE)
    
    if target_image is None:
        raise FileNotFoundError(f"Cannot load image from path: {target_image_path}")

    # 截圖並轉換成灰階
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    # 進行多尺度模板匹配
    res, loc, w, h = multi_scale_template_matching(screenshot, target_image, scale_range, step, threshold)

    if loc is not None:  # 如果找到匹配的圖像
        top_left = loc
        click_x = top_left[0] + w // 2
        click_y = top_left[1] + h // 2

        # 添加隨機偏移
        offset_x = random.randint(*click_offset_range)
        offset_y = random.randint(*click_offset_range)
        click_position = (click_x + offset_x, click_y + offset_y)

        print(f"Image detected! Triggering action at {click_position}")

        # 將滑鼠移動到目標位置
        mouse.move(click_position[0], click_position[1])
        
        # 在點擊前稍微延遲，讓遊戲可以捕捉到事件
        time.sleep(0.1)

        # 根據 action_type 觸發相應動作
        if action_type == 'keyboard':
            # 模擬鍵盤按鍵
            keyboard.press_and_release(key)
            print(f"Pressed key: {key}")

        elif action_type == 'mouse':
            # 模擬滑鼠點擊
            mouse.click(mouse_button)
            print(f"Mouse clicked at {click_position} with {mouse_button} button")

        # 偵測到後暫停
        return  # 結束函數

    # 如果沒有找到圖像，則返回
    print("Image not found.")

# 使用範例：
# 當偵測到指定圖像時，按下空白鍵 (keyboard action)
# trigger_on_image_detection("path/to/image.png", action_type='keyboard', key='space')

# 或者，當偵測到指定圖像時，左鍵點擊滑鼠 (mouse action)
# trigger_on_image_detection("path/to/image.png", action_type='mouse', mouse_button='left')
