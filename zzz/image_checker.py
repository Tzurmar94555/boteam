import cv2
import numpy as np
import pyautogui
from template_matching import multi_scale_template_matching

def is_image_on_screen(target_image_path, scale_range=(0.5, 1.5), step=0.1, threshold=0.8):
    # 加載要檢測的目標圖像
    target_image = cv2.imread(target_image_path, cv2.IMREAD_GRAYSCALE)
    
    if target_image is None:
        raise FileNotFoundError(f"Cannot load image from path: {target_image_path}")

    # 截圖
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    # 多尺度模板匹配
    res, loc, w, h = multi_scale_template_matching(screenshot, target_image, scale_range, step, threshold)

    # 判斷是否找到匹配圖像
    if loc is not None:
        return 1
    else:
        return 0
