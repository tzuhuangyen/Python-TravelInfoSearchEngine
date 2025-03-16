# test_nomad.py
from nomad import run_scraper

def test_scraper():
    print("開始測試爬蟲...")
    results = run_scraper()
    
    # 檢查結果是否為字典
    assert isinstance(results, dict), "結果應該是一個字典"
    
    # 檢查是否有網站數據
    sites = ["Medium", "DCard", "PTT", "背包客棧"]
    for site in sites:
        assert site in results, f"結果中應該包含 {site} 的數據"
        print(f"{site}: {results[site][1]}")
    
    print("測試完成！爬蟲運行正常。")
    return results

if __name__ == "__main__":
    test_results = test_scraper()
