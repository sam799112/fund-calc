import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

# 通用抓取函數
def get_data(url):
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.content, 'html.parser')
        # MoneyDJ 網頁的數字通常在 td 中，且格式較標準
        all_td = soup.find_all('td')
        for td in all_td:
            text = td.text.strip()
            # 確保是數字格式
            if re.match(r'^\d+\.\d+$', text):
                return text
        return "0.00"
    except:
        return "0.00"

def get_fund_data():
    # 1. 自動抓取其他基金
    dsp5_nav = get_data("https://www.moneydj.com/funddj/ya/yp010001.djhtm?a=TLZ64")
    dsp5_div = get_data("https://www.moneydj.com/funddj/yp/wb05.djhtm?a=TLZ64")
    jpm_nav = get_data("https://www.moneydj.com/funddj/ya/yp010001.djhtm?a=jfzn3")
    jpm_div = get_data("https://www.moneydj.com/funddj/yp/wb05.djhtm?a=JFZN3")

    # 2. 自動抓取 MLE24 (您提供的 MoneyDJ 連結)
    # 這邊直接改成自動抓取，省去您每天手動改的麻煩
    mle24_nav = get_data("https://www.moneydj.com/funddj/ya/yp010001.djhtm?a=SHZV9")
    mle24_div = get_data("https://www.moneydj.com/funddj/yp/wb05.djhtm?a=SHZV9")
    
    return {
        "nav": dsp5_nav, 
        "div": dsp5_div, 
        "jpm_nav": jpm_nav, 
        "jpm_div": jpm_div,
        "mle24_nav": mle24_nav,
        "mle24_div": mle24_div,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

# 將結果寫入 data.json
with open('data.json', 'w') as f:
    json.dump(get_fund_data(), f)
