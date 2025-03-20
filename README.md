# Travel Blog Search Engine

https://tzuhuangyen.github.io/Python-TravelInfoSearchEngine/

A Flask-based search engine that allows users to search for travel-related articles from various platforms.

## Project Overview

This web application built with Python Flask provides a centralized platform for searching travel content from Medium and Dcard. It focuses on popular travel destinations like Japan, Korea, Thailand, UK, and Spain.

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
git clone <repository-url>
cd <project-directory>
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

2. Visit `http://127.0.0.1:5000/` in your browser

3. Enter keywords or click on country tags to search

4. View results and click "Read full article" to view the original content

## Project Structure

- `app.py`: Main application entry and route handling
- `scraper.py`: Web scraping functionality
- `templates/`: HTML templates
- `chromedriver-mac-arm64/`: ChromeDriver executable
- `cache/`: Caching implementation and configuration

## Search Mechanism

The application uses Selenium WebDriver to search and scrape travel-related content from:

1. **Medium**: Articles related to keywords and travel
2. **Dcard**: Travel-related posts from Taiwanese social media platform

## Caching System

The project implements result caching to improve efficiency:

- Uses Flask-Caching extension with in-memory cache
- Stores search results by keyword
- Implements TTL (Time To Live) mechanism for content freshness
- Pre-warms cache for popular keywords

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

# 旅遊部落格搜尋引擎

一個基於 Flask 的旅遊部落格搜尋引擎，允許用戶搜尋來自不同平台的旅遊相關文章和內容。

## 專案概述

這個專案是一個網頁應用程式，使用 Python Flask 框架構建，旨在為用戶提供一個集中式平台，搜尋來自 Medium 和 Dcard 等網站的旅遊相關內容。

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
git clone <repository-url>
cd <project-directory>
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

2. 在瀏覽器中訪問 `http://127.0.0.1:5000/`

3. 使用搜尋欄輸入關鍵字，或點擊預設國家標籤進行搜尋

4. 查看搜尋結果並點擊「閱讀完整文章」查看原始內容

## 專案結構

- `app.py`: 主應用程式入口和路由處理
- `scraper.py`: 網頁爬蟲功能，負責抓取 Medium 和 Dcard 的內容
- `original_scraper.py`: 原始爬蟲實現
- `nomad.py`: 輔助爬蟲功能
- `templates/`: HTML 模板
  - `index.html`: 首頁和搜尋介面
  - `result.html`: 搜尋結果頁面
- `src/components/`: 前端組件
- `chromedriver-mac-arm64/`: ChromeDriver 執行檔
- `cache/`: 快取相關實現和配置

## 搜尋原理

該應用程式使用 Selenium WebDriver 自動化瀏覽器，搜尋並抓取以下來源的旅遊相關內容：

1. **Medium**: 搜尋與關鍵字相關的旅遊文章
2. **Dcard**: 搜尋台灣社交媒體平台 Dcard 上的旅遊相關貼文

爬蟲會抓取文章標題、內容摘要、作者、發布日期和原始連結，並在搜尋結果頁面中呈現。

## 快取機制

為了提高應用程式的效率和減少對目標網站的請求負擔，本專案實現了搜尋結果快取功能：

### 技術實現

- **Flask-Caching**: 使用 Flask-Caching 擴展來管理快取，簡化快取操作和配置
- **SimpleCache**: 基於字典的記憶體內快取，適合單機部署
- **快取鍵生成**: 使用搜尋關鍵字作為快取鍵，確保相同搜尋條件能夠命中快取
- **TTL 機制**: 設定快取過期時間 (Time To Live)，定期更新以確保內容新鮮度

### 工作流程

1. 接收用戶搜尋請求時，首先檢查關鍵字是否存在於快取中
2. 如果快取命中，直接返回快取的搜尋結果，避免重複爬取
3. 如果快取未命中，執行爬蟲獲取搜尋結果，並將結果存入快取
4. 根據設定的 TTL 參數，自動管理快取的生命週期

### 效能優化

- 預熱機制: 對熱門關鍵字 (如 '日本', '韓國' 等) 預先執行爬蟲並存入快取
- 快取統計: 記錄快取命中率和未命中次數，優化快取策略
- 差異化 TTL: 為不同類型的搜尋關鍵字設定不同的快取過期時間

## 注意事項

- 本應用程式僅用於學習和研究目的
- 請尊重各網站的使用條款和爬蟲政策
- 爬蟲可能會因目標網站
