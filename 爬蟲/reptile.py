import time
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
def test1():
    driver = webdriver.Chrome(options=Options())
    driver.get("https://kma.kkbox.com/charts/hourly?terr=tw&lang=tc")
    # print(driver.page_source)
    tags = driver.find_elements(By.CLASS_NAME, 'charts-list-song')
    count = 1
    aaa = ""
    for tag in tags:
        song_name = tag.text.strip()
        if song_name:  # 確保歌曲名稱不是空的
            print(f"第{count}名 {song_name}")
            aaa = aaa + f"第{count}名 {song_name}" + "\n"
            count += 1
            
        if count >= 6:
            break
    driver.close()
    return aaa
