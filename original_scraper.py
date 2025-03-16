# pylint: disable=astroid-error

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
import time
import json

# Redis 設置
r = redis.Redis(
    host='redis-15041.c299.asia-northeast1-1.gce.redns.redis-cloud.com',
    port=15041,
    decode_responses=True,
    username="default",
    password="Z7XLsg9aymGF0NWwLqWW43OwLu3AfmFx",
)
# options建立不開啟瀏覽器搜尋模式，並模擬瀏覽器行為避免被網站阻擋爬蟲
chrome_options = Options()  # initialize options object
chrome_options.add_argument("--headless")  # 不開啟瀏覽器(無頭模式)
chrome_options.add_argument("--disable-gpu")  # 禁用GPU加速
chrome_options.add_argument("--no-sandbox")  # 禁用沙盒模式
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # 防止被網站檢測出自動化工具
chrome_options.add_argument("--disable-dev-shm-usage")  # Reduce memory usage
chrome_options.add_argument("--disable-extensions")  # Disable extensions
# 模擬一般瀏覽器行為
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

# 連結google driver，path放入你的google driver絕對路徑
# ex: "C:\\Your_driver_path\\chromedriver.exe"
service = Service(
    "/Users/tzuhuangyen/Desktop/flaskWeb/chromedriver-mac-arm64/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

# redis 設置(這是我新開的應該只能維持1個月)
import redis
redis_client = redis.Redis(
    host='redis-15041.c299.asia-northeast1-1.gce.redns.redis-cloud.com',
    port=15041,
    decode_responses=True,
    username="default",
    password="Z7XLsg9aymGF0NWwLqWW43OwLu3AfmFx",
)

def find_element_text(element, css_selector):  # 抓取標籤當中的文字內容
    try:
        return element.find_element(By.CSS_SELECTOR, css_selector).text
    except NoSuchElementException:  # 若無法抓取到內容則回傳None避免程式中斷
        return None

def find_element_href(element, css_selector):  # 抓取標籤當中的href內容
    try:
        return element.find_element(
            By.CSS_SELECTOR, css_selector).get_attribute("href")
    except NoSuchElementException:  # 若無法抓取到內容則回傳None避免程式中斷
        return None
    
def click_show_more_btn(selector):  # 點擊show more button
    try:
        btn = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, selector)))
        btn.click()
        print("已點擊Show more")
        time.sleep(1)  # 確認點擊後有時間抓取新增數據
        time.sleep(wait_time)  # 確認點擊後有時間抓取新增數據
    except TimeoutException:
        print("找不到按鈕")
    except Exception as e:
        print(e)



def search(query):
    # redis快取
    redis_key = query  # 輸入查詢關鍵字作為redis key
    article_list = r.get(redis_key)
    if article_list:
        # deserialized list
        article_list = json.loads(article_list)
        print("使用redis快取")
        # print(article_list)
        return article_list
    else:
      # 連結medium
      base_url = f"https://medium.com/search?q={query}"
      driver.get(base_url)
      # 確認頁面已成功加載
      WebDriverWait(driver, 1).until(
          EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.a.b.c")))
      # 點擊show more button 最大化數據加載數量
      click_show_more_btn("//button[text()='Show more']")
      # 存放文章list
      article_list = []
      # 抓取整塊文章
      articles = driver.find_elements(
          By.CSS_SELECTOR, "div.ab.co .l div.bh.cm div.bh.l")

      # # 抓取每個文章底下的標題、簡介、作者及連結網址
      try:
          for i, article in enumerate(articles):
              if (i+1 > 10):  # 限制抓取10筆資料
                  break
              title = find_text(
                  article, ".ab a.af.ag.ah.ai.as.at h2.bf")
              introduction = find_text(
                  article, ".ab a.af.ag.ah.ai.as.at .bf.b")
              author = find_text(
                  article, ".ab p.bf.b.ik.z.ef.hl.eg.eh")
              href = find_href(
                  article, ".ab a.af.ag.ah.ai.as.at")
              res = {
                  "ID": i+1,
                  "title": title,
                  "introduction": introduction,
                  "author": author,
                  "href": href
              }
              article_list.append(res)
      except Exception as e:
          print(e)
      finally:
          driver.quit()
          #序列化數據以便儲存於redis
          serialized_article_list = json.dumps(article_list)
          #設置redis key-value pair，儲存10min自動刪除
          r.set(redis_key, serialized_article_list, ex=3600)
          print("已儲存結果至redis")
          #print(article_list)
          return article_list
        return article_list
        
    except Exception as e:
        print(f"Error during search: {e}")
        return []
    finally:
        driver.quit()
