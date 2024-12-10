import mouse  # 用來監聽滑鼠事件
import time
from 偵測與點擊 import trigger_on_image_detection  # 從偵測與點擊.py 引入函數

def main():
    print(1)
    time.sleep(3)
    print("ok")
    trigger_on_image_detection("image/test.png", action_type='mouse', mouse_button='left')
    print("2")
if __name__ == "__main__":
    main()
