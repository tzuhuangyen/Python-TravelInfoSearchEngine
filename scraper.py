import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from urllib.parse import quote


def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-extensions')
    options.add_argument('--start-maximized')
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    return webdriver.Chrome(options=options)

def scroll_page(driver, times=3):
    for _ in range(times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

def get_medium_articles(driver, query):
    articles = []
    try:
        search_query = f"{query} 旅遊 travel"
        medium_url = f"https://medium.com/search?q={quote(search_query)}"
        driver.get(medium_url)
        time.sleep(5)

        article_elements = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "article"))
        )
        scroll_page(driver)
        print(f"Found {len(article_elements)} article elements")  # 除錯用

        
        for i, article in enumerate(article_elements[:10]):
            try:                
                title_element = article.find_element(By.CSS_SELECTOR, "h2,h3")
                title = title_element.text.strip() if title_element else "無標題"
                print(f"Processing article {i+1}: {title}")

                link_element = article.find_element(By.CSS_SELECTOR, "a[aria-label], a[class*='af']")
                link = link_element.get_attribute("href") if link_element else "#"
                
                preview_element = article.find_element(By.CSS_SELECTOR, "h3")
                preview = preview_element.text.strip() if preview_element else "無預覽內容"
                
                try:
                    author_element = article.find_element(
                        By.CSS_SELECTOR, 
                        "a[class*='ae'] p, div[class*='ae'] p"
                    )
                    author = author_element.text.strip()
                except:
                    author = "未知作者"
                    

                try:
                    date_element = article.find_element(By.CSS_SELECTOR, "p[class*='fc-gray'], span[class*='fc-gray']")
                    date = date_element.text.strip()
                except:
                    date = "未知日期"
                
                if title and link != "#" and ("旅" in title or "遊" in title or "travel" in title.lower() or "trip" in title.lower()):
                    articles.append({
                        "ID": i + 1,
                        "title": title,
                        "introduction": preview[:200] + "..." if len(preview) > 200 else preview,
                        "href": link,
                        "source": "Medium",
                        "author":author,
                        "date": date  # 假設的日期，你可以根據需要修改
                    })
            except Exception as e:
                print(f"Error processing Medium article: {str(e)}")
                continue
    except TimeoutException:
        print("Timeout waiting for Medium articles to load")
    except Exception as e:
        print(f"Error fetching Medium articles: {str(e)}")
    return articles

def get_dcard_articles(driver, query):
    articles = []
    try:
        encoded_query = quote(query)
        # https://www.dcard.tw/f/travel
        # https://www.dcard.tw/search?query={encoded_query}=travel
        dcard_url = f"https://www.dcard.tw/search?query={encoded_query}旅遊&forum=travel"
        print(f"Accessing Dcard URL: {dcard_url}")
        driver.get(dcard_url)
        time.sleep(10)

        print("Waiting for articles to load...")
        # 等待文章列表加載
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article"))
        )
        scroll_page(driver)
        posts = driver.find_elements(By.TAG_NAME, "article")
        print(f"Found {len(posts)} posts")
        
        # 使用完整的 XPath 路徑來找尋文章標題
        for i, post in enumerate(posts[:10]):
            try:
                # 獲取標題和連結
                # 使用相對 XPath 找尋標題和連結
                try:
                    title_element = post.find_element(By.CSS_SELECTOR, "h2 a")
                    title = title_element.text.strip()
                    link = title_element.get_attribute("href")
                except NoSuchElementException:
                    continue
                
                # 獲取預覽內容
                try:
                    preview_element = post.find_element(By.XPATH, ".//div[contains(@class, 'd_dj_') and contains(@class, 'm16n7y82')]//div[contains(@class, 'd_d8_')]")
                    # 獲取所有子元素的文字
                    preview_parts = []
                    # 獲取所有子元素（包括 span 和 em）
                    child_elements = preview_element.find_elements(By.XPATH, ".//*")
                    for element in child_elements:
                    # 獲取元素的文字內容
                        text = element.text.strip()
                        if text:
                            preview_parts.append(text)
        
                        # 將所有文字組合起來
                    preview = ' '.join(preview_parts)
    
                    # 清理文字（移除多餘的空格）
                    preview = ' '.join(preview.split())
                except NoSuchElementException:
                    preview = "無預覽內容"
                
                except Exception as e:
                    print(f"Error getting preview: {str(e)}")
                    preview = "預覽內容擷取錯誤"
                
                if title and link != "https://www.dcard.tw":
                    articles.append({
                        "ID": len(articles) + 1,
                        "title": title,
                        "introduction": preview[:200] + "..." if len(preview) > 200 else preview,
                        "href": link,
                        "source": "Dcard"
                    })
                    print(f"Found Dcard article: {title}")
            except Exception as e:
                print(f"Error processing Dcard article: {str(e)}")
                continue
    
    except TimeoutException:
        print("Timeout waiting for Dcard articles to load")
    except Exception as e:
        print(f"Error fetching Dcard articles: {str(e)}")
    
    print(f"Total Dcard articles found: {len(articles)}")
    return articles

def search(keyword):
    results = []
    driver = None
    try:
        driver = initialize_driver()
        print(f"Searching Medium for: {keyword}")
        medium_articles = get_medium_articles(driver, keyword)
        results.extend(medium_articles)
        
        print(f"Searching Dcard for: {keyword}")
        dcard_articles = get_dcard_articles(driver, keyword)
        results.extend(dcard_articles)
    except Exception as e:
        print(f"搜尋過程發生錯誤: {e}")
    finally:
        if driver:
            driver.quit()
    return results