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
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # MoneyDJ 淨值與配息表通常數字會出現在 td 中
        all_td = soup.find_all('td')
        
        for td in all_td:
            text = td.text.strip()
            # 過濾出包含小數點的數字，排除掉日期或其他無關文字
            if re.match(r'^\d+\.\d+$', text):
                return text
        return "0.00"
    except:
        return "0.00"

def get_fund_data():
    # 1. 安聯收益成長 (DSP5) - 原始網址保持不變
    dsp5_nav = get_data("https://www.moneydj.com/funddj/ya/yp010001.djhtm?a=TLZ64")
    dsp5_div = get_data("https://www.moneydj.com/funddj/yp/wb05.djhtm?a=TLZ64")
    
    # 2. 摩根多重收益 (JFZN3) - 使用你剛提供的網址
    jpm_nav = get_data("https://www.moneydj.com/funddj/ya/yp010001.djhtm?a=jfzn3")
    jpm_div = get_data("https://www.moneydj.com/funddj/yp/wb05.djhtm?a=JFZN3")
    
    # 打包數據
    return {
        "nav": dsp5_nav, 
        "div": dsp5_div, 
        "jpm_nav": jpm_nav, 
        "jpm_div": jpm_div, 
        "date": datetime.now().strftime("%Y-%m-%d")
    }

# 將結果寫入 data.json
with open('data.json', 'w') as f:
    json.dump(get_fund_data(), f)
