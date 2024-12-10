import pyautogui
import time

def click_left_mouse():
    print("將在3秒後模擬滑鼠左鍵點擊...")
    time.sleep(3)  # 等待3秒
    pyautogui.click()  # 模擬點擊左鍵
    print("左鍵點擊完成。")

if __name__ == "__main__":
    click_left_mouse()
