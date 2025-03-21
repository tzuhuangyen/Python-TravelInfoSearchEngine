"""
旅遊文章爬蟲模組。

這個模組使用 Selenium 自動化瀏覽器，透過 Google 搜尋特定網站上的旅遊相關文章，
並抓取搜尋結果的標題和連結。
"""
import time
import logging
from typing import Dict, List, Tuple, Any, Optional

from flask import Flask
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 定義類型別名
ResultDict = Dict[str, List[Any]]
SiteDict = Dict[str, List[str]]

def convert_num(n: int) -> str:
    """
    這個函數用於生成索引鍵：
    將數字轉換為兩位數的字符串，不足兩位前面補0。
    
    Args:
        n: 要轉換的數字
        
    Returns:
        兩位數的字符串表示
    """
    return str(n).zfill(2)

def create_driver(headless: bool = False) -> webdriver.Chrome:
    """
    創建並配置 Chrome WebDriver實例，這個實例將用於自動化控制 Chrome 瀏覽器進行網頁爬蟲。
    
    Args:
        headless: 是否使用無頭模式（不顯示瀏覽器界面）
        
    Returns:
        配置好的 Chrome WebDriver 實例
    """
    options = Options()
    options.add_argument("--incognito")  # 使用無痕模式
    
    if headless:
        options.add_argument("--headless")  # 無頭模式
    
    # 添加其他有用的選項
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    
    # 設定 user-agent 以減少被識別為爬蟲的可能性
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    return webdriver.Chrome(options=options)

def search_google(driver: webdriver.Chrome, keyword: str, site_url: str) -> None:
    """
    在 Google 上搜尋特定網站的關鍵字。
    
    Args:
        driver: Chrome WebDriver 實例
        keyword: 搜尋關鍵字
        site_url: 目標網站的 URL
    """
    # Google 搜尋頁面
    url = "https://www.google.com.tw/"
    
    # 構建搜尋查詢
    search_query = f'allintext: {keyword} 旅遊 心得 "{keyword}" site:{site_url}'
    
    try:
        # 打開 Google 搜尋頁面
        driver.get(url)
        
        # 等待頁面完全加載
        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        
        # 找到搜尋框並輸入查詢
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='q']"))
        )
        search_box.clear()
        search_box.click()
        search_box.send_keys(search_query)
        search_box.submit()
        
        # 等待搜尋結果頁面加載
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//h3'))
        )
        
    except TimeoutException:
        logger.error(f"搜尋超時: {search_query}")
        raise
    except Exception as e:
        logger.error(f"搜尋過程中發生錯誤: {str(e)}")
        raise

def extract_search_results(driver: webdriver.Chrome) -> List[Tuple[str, str]]:
    """
    從 Google 搜尋結果頁面提取標題和連結。
    extract_search_results 函數的主要目的是從 Google 搜尋結果頁面中提取標題和連結。在完成 search_google 函數的搜尋操作後，這個函數負責從結果頁面中擷取有用的信息。
    Args:
        driver: Chrome WebDriver 實例
        
    Returns:
        包含 (標題, 連結) 元組的列表
    """
    results = []
    
    try:
        # 等待搜尋結果加載
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//h3'))
        )
        
        # 獲取所有標題元素
        title_elements = driver.find_elements(By.XPATH, "//h3")
        
        for title_elem in title_elements:
            try:
                # 獲取標題文本
                title = title_elem.text
                
                # 獲取包含 <h3> 的父層元素，然後尋找 <a> 標籤
                parent_element = title_elem.find_element(By.XPATH, "./ancestor::div[contains(@class, 'yuRUbf')]")
                link_element = parent_element.find_element(By.TAG_NAME, "a")
                url = link_element.get_attribute("href")
                
                # 添加到結果列表
                if title and url:
                    results.append((title, url))
                    
            except (NoSuchElementException, Exception) as e:
                logger.warning(f"提取搜尋結果時出錯: {str(e)}")
                continue
                
    except Exception as e:
        logger.error(f"提取搜尋結果時發生錯誤: {str(e)}")
        
    return results

def run_scraper(keyword: Optional[str] = None) -> ResultDict:
    """
    整個爬蟲程序的主要入口點，負責協調整個爬蟲流程，包括初始化、搜尋、提取結果和錯誤處理。
    運行爬蟲，搜尋並提取旅遊相關文章。
    
    Args:
        keyword: 搜尋關鍵字，如果為 None 則使用預設值 "日本"
        
    Returns:
        包含搜尋結果的字典
    """
    # 如果沒有提供關鍵字，使用預設值
    if keyword is None:
        keyword = "日本"
    
    logger.info(f"開始搜尋關鍵字: {keyword}")
    
    # 記錄各網站網域
    site_dict: SiteDict = {
        "site_01": ["Medium", "medium.com"],
        "site_02": ["DCard", "www.dcard.tw"],
        "site_03": ["PTT", "www.ptt.cc"],
        "site_04": ["背包客棧", "www.backpackers.com.tw"]
    }
    
    result_dict: ResultDict = {}
    driver = None
    
    try:
        # 創建 WebDriver
        driver = create_driver(headless=False)  # 設為 True 可以不顯示瀏覽器
        
        # 處理每個目標網站
        for key, (site_name, site_url) in site_dict.items():
            logger.info(f"正在處理網站: {site_name}")
            
            try:
                # 在 Google 上搜尋
                search_google(driver, keyword, site_url)
                
                # 提取搜尋結果
                search_results = extract_search_results(driver)
                
                # 記錄結果數量
                result_qty = len(search_results)
                logger.info(f"網站 {site_name} 抓取到 {result_qty} 筆結果")
                
                # 將結果存入字典
                for i, (title, url) in enumerate(search_results):
                    result_key = f"{site_name}{convert_num(i)}"
                    result_dict[result_key] = [title, url]
                
                # 添加網站摘要信息
                result_dict[site_name] = [result_qty, f"結果有 {result_qty} 筆資料"]
                
                # 短暫暫停，避免過於頻繁的請求
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"處理網站 {site_name} 時發生錯誤: {str(e)}")
                result_dict[site_name] = [0, f"搜尋失敗: {str(e)}"]
                continue
        
        logger.info("搜尋完成")
        return result_dict
        
    except Exception as e:
        logger.error(f"爬蟲過程中發生錯誤: {str(e)}")
        return {"error": [str(e), "爬蟲過程中發生錯誤"]}
        
    finally:
        # 確保 WebDriver 被正確關閉
        if driver:
            driver.quit()
            logger.info("WebDriver 已關閉")

# 如果直接運行此文件，則執行爬蟲並打印結果
if __name__ == "__main__":
    results = run_scraper()
    print("\n搜尋結果摘要:")
    for key, value in results.items():
        if not key.startswith("site_") and not key.endswith(tuple("0123456789")):
            print(f"{key}: {value[1]}")
