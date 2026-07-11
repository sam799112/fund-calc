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
        all_td = soup.find_all('td')
        for td in all_td:
            text = td.text.strip()
            if re.match(r'^\d+\.\d+$', text):
                return text
        return "0.00"
    except:
        return "0.00"

def get_fund_data():
    # 1. 自動抓取區：其他基金保持自動更新
    dsp5_nav = get_data("https://www.moneydj.com/funddj/ya/yp010001.djhtm?a=TLZ64")
    dsp5_div = get_data("https://www.moneydj.com/funddj/yp/wb05.djhtm?a=TLZ64")
    jpm_nav = get_data("https://www.moneydj.com/funddj/ya/yp010001.djhtm?a=jfzn3")
    jpm_div = get_data("https://www.moneydj.com/funddj/yp/wb05.djhtm?a=JFZN3")

    # 2. 手動填寫區：MLE24 專用 (請直接修改下方這兩行數字)
    mle24_nav = "21.63"  # <--- 請在這裡修改最新的淨值
    mle24_div = "0.08"   # <--- 請在這裡修改最新的配息
    
    # 打包數據
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
