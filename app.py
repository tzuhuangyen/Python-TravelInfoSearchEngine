"""
旅遊部落格搜尋引擎的 Flask 應用。

這個模塊實現了一個 Web 應用，允許用戶搜尋來自不同平台的旅遊相關文章，
包括基於關鍵字的搜尋和預定義國家標籤的快速搜尋。
"""
import os

from flask import Flask, render_template, redirect, url_for, request
from nomad import run_scraper  # 導入 run_scraper 函數

app = Flask(__name__)

@app.route('/')
def index():
    """
    渲染並返回應用首頁。
    
    Returns:
        HTML模板: index.html的渲染結果
    """
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    """
    處理用戶提交的搜索關鍵字。
    
    從表單中獲取用戶輸入的關鍵字，執行爬蟲，並渲染結果頁面。
    
    Returns:
        HTML模板: result.html的渲染結果，包含搜索關鍵字和結果
    """
    # 從表單或 URL 參數獲取關鍵字
    keyword = request.args.get('keyword', None)
    if request.method == 'POST':
        keyword = request.form.get('keyword', None)
    
    # 如果沒有提供關鍵字，使用預設值
    if not keyword:
        keyword = "日本"
    
    # 執行爬蟲
    results = run_scraper(keyword)
    
    # 將爬蟲結果轉換為適合 result.html 的格式
    res_list = []
    
    # 設定要處理的網站列表
    sites = ["Medium", "DCard", "PTT", "背包客棧"]
    
    # 為每個網站處理結果
    for site in sites:
        if site in results:
            # 獲取該網站的結果數量
            result_qty = results[site][0]
            
            # 處理每個結果
            for i in range(result_qty):
                article_key = f"{site}{str(i).zfill(2)}"
                if article_key in results:
                    title, url = results[article_key]
                    
                    # 創建文章對象
                    article = {
                        'ID': f"{site}-{i+1}",
                        'title': title,
                        'introduction': f"來自 {site} 的旅遊文章",  # 簡介
                        'author': "未知",  # 爬蟲未提供作者信息
                        'source': site,
                        'date': "未知",  # 爬蟲未提供日期信息
                        'href': url
                    }
                    
                    res_list.append(article)
    
    # 渲染結果頁面
    return render_template('result.html', res_list=res_list, keyword=keyword)

@app.route('/search/tag/<tag>')
def tag_search(tag):
    """
    處理通過標籤進行的搜索。
    
    檢查提供的標籤是否有效，若有效則執行爬蟲並返回相關搜索結果，
    若無效則重定向到首頁。
    
    Args:
        tag (str): 用戶選擇的搜索標籤
        
    Returns:
        HTML模板或重定向: 若標籤有效則返回搜索結果頁面，
        若標籤無效則重定向到首頁
    """
    # 可以添加一些驗證
    valid_tags = ['日本', '韓國', '泰國', '英國', '西班牙']
    if tag not in valid_tags:
        return redirect(url_for('index'))
    
    # 執行爬蟲
    results = run_scraper(tag)
    
    # 將爬蟲結果轉換為適合 result.html 的格式
    res_list = []
    
    # 設定要處理的網站列表
    sites = ["Medium", "DCard", "PTT", "背包客棧"]
    
    # 為每個網站處理結果
    for site in sites:
        if site in results:
            # 獲取該網站的結果數量
            result_qty = results[site][0]
            
            # 處理每個結果
            for i in range(result_qty):
                article_key = f"{site}{str(i).zfill(2)}"
                if article_key in results:
                    title, url = results[article_key]
                    
                    # 創建文章對象
                    article = {
                        'ID': f"{site}-{i+1}",
                        'title': title,
                        'introduction': f"來自 {site} 的旅遊文章",  # 簡介
                        'author': "未知",  # 爬蟲未提供作者信息
                        'source': site,
                        'date': "未知",  # 爬蟲未提供日期信息
                        'href': url
                    }
                    
                    res_list.append(article)
    
    return render_template('result.html', res_list=res_list, keyword=tag)

if __name__ == '__main__':
    # 使用不同的端口，避免與 AirPlay 衝突
    port = int(os.environ.get("PORT", 8080))  # 改為 8080 端口
    app.run(host='0.0.0.0', port=port)
