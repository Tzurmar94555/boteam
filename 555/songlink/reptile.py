import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test2():
    # 初始化 WebDriver
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.get("https://kma.kkbox.com/charts/hourly?terr=tw&lang=tc")

    # 等待排行榜元素加載完成
    wait = WebDriverWait(driver, 10)
    tags = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'charts-list-song')))

    # 抓取 KKBOX 每小時排行榜中的前 5 首歌曲名稱
    song_names = []
    count = 1
    for tag in tags:
        song_name = tag.text.strip()
        if song_name:  # 確保歌曲名稱不是空的
            song_names.append(song_name)
            count += 1
            if count > 5:
                break

    # 在 YouTube 上查詢歌曲並回傳網址
    youtube_urls = []
    for song_name in song_names:
        driver.get("https://www.youtube.com")
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "search_query")))
        search_box.clear()
        search_box.send_keys(song_name)
        search_box.submit()

        try:
            wait.until(EC.presence_of_element_located((By.ID, "video-title")))

            # 找到包含搜尋中歌曲名稱的結果
            video_elements = driver.find_elements(By.ID, "video-title")
            for video in video_elements:
                if song_name.lower() in video.get_attribute("title").lower():
                    video.click()
                    break


            # 等待影片頁面加載完成並獲取當前網址
            time.sleep(2)  # 等待影片頁面加載
            youtube_urls.append(driver.current_url)
        except Exception as e:
            print(f"無法點擊影片: {e}")
            youtube_urls.append(f"https://www.youtube.com/results?search_query={song_name}")

    # 關閉瀏覽器
    driver.quit()

    # 回傳 YouTube 影片網址
    return youtube_urls
