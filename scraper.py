import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

def get_data(url):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    # 搜尋頁面上所有可能的 td 欄位
    all_td = soup.find_all('td')
    
    # 遍歷尋找：我們需要看起來像數字的 (例如：包含小數點，且長度適中)
    for td in all_td:
        text = td.text.strip()
        # 正規表達式：匹配數字與小數點，排除日期格式(如 2026/06/15)
        if re.match(r'^\d+\.\d+$', text):
            return text
    return "0.00"

def get_fund_data():
    # 抓取淨值
    nav = get_data("https://www.moneydj.com/funddj/ya/yp010001.djhtm?a=TLZ64")
    # 抓取配息 (如果頁面結構不同，可以針對 URL 單獨處理)
    div = get_data("https://www.moneydj.com/funddj/yp/wb05.djhtm?a=TLZ64")
    
    return {"nav": nav, "div": div, "date": datetime.now().strftime("%Y-%m-%d")}

with open('data.json', 'w') as f:
    json.dump(get_fund_data(), f)
