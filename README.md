# Travel Blog Search Engine

A Flask-based search engine that allows users to search for travel-related articles from various platforms.

## Project Overview

This web application built with Python Flask provides a centralized platform for searching travel content from Medium, Dcard, PTT, and Backpackers. It focuses on popular travel destinations like Japan, Korea, Thailand, UK, and Spain.

## Key Features

- Keyword-based travel article search
- Quick tag search for specific countries
- Search results display with title, introduction, author, source, and date
- Links to original articles for complete content
- **Caching**: Stores query results to improve response time for repeated searches

## Technical Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Web Scraping**: Selenium WebDriver
- **Browser Automation**: ChromeDriver
- **Data Caching**: Flask-Caching with in-memory dictionary cache

## Installation Guide

1. Clone this project

```bash
git clone https://github.com/tzuhuangyen/Python-TravelInfoSearchEngine.git
cd Python-TravelInfoSearchEngine
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Ensure ChromeDriver is properly installed
   - Project includes mac-arm64 version
   - Download other versions from [official website](https://chromedriver.chromium.org/downloads) if needed

## Usage

1. Start the Flask application

```bash
python app.py
```

2. Visit `http://127.0.0.1:8080/` in your browser (Note: Port changed to 8080 to avoid conflicts with AirPlay)

3. Enter keywords or click on country tags to search

4. View results and click "Read full article" to view the original content

## Project Structure

- `app.py`: Main application entry and route handling
- `nomad.py`: Web scraping functionality
- `templates/`: HTML templates
- `static/`: Static assets like images and CSS
- `chromedriver-mac-arm64/`: ChromeDriver executable

## Search Mechanism

The application uses Selenium WebDriver to search and scrape travel-related content from:

1. **Medium**: Articles related to keywords and travel
2. **Dcard**: Travel-related posts from Taiwanese social media platform
3. **PTT**: Travel content from Taiwan's largest bulletin board system
4. **Backpackers**: Travel guides and experiences from backpackers.com.tw

## Troubleshooting

If you encounter search timeout errors:
- Try using different keywords
- Check your internet connection
- Ensure your ChromeDriver version matches your Chrome browser
- Adjust the timeout settings in the scraper code

If you get a "Port 5000 is in use" error:
- Use a different port by modifying the port number in app.py
- On macOS, disable AirPlay Receiver from System Preferences > General > AirDrop & Handoff

## Important Notes

- This application is for learning and research purposes only
- Please respect the terms of service and scraping policies of target websites
- Web scrapers may fail due to website structure changes and require maintenance

## Future Plans

- Add more travel content sources
- Implement more accurate content relevance ranking
- Add user favorites and sharing features
- Optimize mobile display
- Expand caching functionality for larger deployments

## Deployed Version

A live version of this application is deployed at [https://travel-search-engine.onrender.com](https://travel-search-engine.onrender.com)

# 旅遊部落格搜尋引擎

一個基於 Flask 的旅遊部落格搜尋引擎，允許用戶搜尋來自不同平台的旅遊相關文章和內容。

## 專案概述

這個專案是一個網頁應用程式，使用 Python Flask 框架構建，旨在為用戶提供一個集中式平台，搜尋來自 Medium、Dcard、PTT 和背包客棧等網站的旅遊相關內容。

## 主要功能

- 透過關鍵字搜尋旅遊相關文章
- 使用快速標籤直接搜尋特定國家的旅遊文章
- 顯示搜尋結果，包括文章標題、簡介、作者、來源和發布日期
- 提供原始文章鏈接，方便用戶閱讀完整內容
- **快取功能**：儲存查詢結果以提高重複搜尋的響應速度

## 技術架構

- **後端**: Python Flask
- **前端**: HTML, CSS, JavaScript
- **網頁爬蟲**: Selenium WebDriver
- **瀏覽器自動化**: ChromeDriver
- **資料快取**:
  - Flask-Caching 擴展
  - 記憶體內字典式快取 (SimpleCache)
  - 基於時間的快取失效策略
  - 關鍵字索引搜尋結果儲存

## 安裝指南

1. git clone 複製此專案到本地環境

```bash
git clone https://github.com/tzuhuangyen/Python-TravelInfoSearchEngine.git
cd Python-TravelInfoSearchEngine
```

2. 安裝所需依賴

```bash
pip install -r requirements.txt
```

3. 確保 ChromeDriver 已正確安裝
   - 專案包含 mac-arm64 版本的 ChromeDriver
   - 如需其他平台版本，請從[官方網站](https://chromedriver.chromium.org/downloads)下載

## 使用方法

1. 啟動 Flask 應用

```bash
python app.py
```

2. 在瀏覽器中訪問 `http://127.0.0.1:8080/`

3. 使用搜尋欄輸入關鍵字，或點擊預設國家標籤進行搜尋

4. 查看搜尋結果並點擊「閱讀完整文章」查看原始內容

## 專案結構

- `app.py`: 主應用程式入口和路由處理
- `nomad.py`: 網頁爬蟲功能，負責抓取各平台的內容
- `templates/`: HTML 模板
  - `index.html`: 首頁和搜尋介面
  - `result.html`: 搜尋結果頁面
- `static/`: 靜態資源，包括圖片和CSS
- `chromedriver-mac-arm64/`: ChromeDriver 執行檔

## 搜尋原理

該應用程式使用 Selenium WebDriver 自動化瀏覽器，搜尋並抓取以下來源的旅遊相關內容：

1. **Medium**: 搜尋與關鍵字相關的旅遊文章
2. **Dcard**: 搜尋台灣社交媒體平台 Dcard 上的旅遊相關貼文
3. **PTT**: 搜尋台灣最大的電子佈告欄系統中的旅遊內容
4. **背包客棧**: 搜尋背包客棧網站上的旅遊指南和經驗分享

## 故障排除

如果遇到搜尋超時錯誤：
- 嘗試使用不同的關鍵字
- 檢查您的網路連接
- 確保您的 ChromeDriver 版本與 Chrome 瀏覽器版本匹配
- 調整爬蟲代碼中的超時設置

如果遇到「Port 5000 is in use」錯誤：
- 通過修改 app.py 中的端口號使用不同的端口
- 在 macOS 上，從系統偏好設置 > 通用 > AirDrop 和 Handoff 中禁用 AirPlay 接收器

## 注意事項

- 本應用程式僅用於學習和研究目的
- 請尊重各網站的使用條款和爬蟲政策
- 爬蟲可能會因目標網站結構變化而失效，需要定期維護

## 未來計劃

- 增加更多旅遊內容來源
- 實現更準確的內容相關性排名
- 添加用戶收藏和分享功能
- 優化移動端顯示
- 擴展快取功能以支持更大規模部署

## 線上版本

本應用程式的線上版本已部署在 [https://travel-search-engine.onrender.com](https://travel-search-engine.onrender.com)