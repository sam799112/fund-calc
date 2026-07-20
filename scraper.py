import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/115.0.0.0',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'If-None-Match': '',
    'If-Modified-Since': '0'
}

def get_data(url):
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.content, 'html.parser')
        all_td = soup.find_all('td')
        
        found_date = ""
        for td in all_td:
            text = td.text.strip()
            
            # 1. 先嘗試抓取網頁上的日期 (格式可能是 2024/07/14 或 07/14)
            if not found_date and re.match(r'^(\d{4}[-/])?\d{2}[-/]\d{2}$', text):
                found_date = text
                
            # 2. 再抓取淨值/配息的數字
            elif re.match(r'^\d+\.\d+$', text):
                # 一旦找到淨值數字，就把「淨值」跟「剛剛記下來的日期」一起回傳
                return {"value": text, "date": found_date}
                
        return {"value": "0.00", "date": ""}
    except:
        return {"value": "0.00", "date": ""}

def get_fund_data():
    dsp5_nav = get_data("https://www.moneydj.com/funddj/ya/yp010001.djhtm?a=TLZ64")
    dsp5_div = get_data("https://www.moneydj.com/funddj/yp/wb05.djhtm?a=TLZ64")
    
    jpm_nav = get_data("https://www.moneydj.com/funddj/ya/yp010001.djhtm?a=jfzn3")
    jpm_div = get_data("https://www.moneydj.com/funddj/yp/wb05.djhtm?a=JFZN3")

    # 🌟 這裡已修改成標準境外基金歷史淨值表網址 (wb02.djhtm)
    frp4_nav = get_data("https://www.moneydj.com/funddj/yp/wb02.djhtm?a=FLZ92")
    frp4_div = get_data("https://www.moneydj.com/funddj/yp/wb05.djhtm?a=FLZ92")

    mle24_nav = get_data("https://www.moneydj.com/funddj/ya/yp010001.djhtm?a=SHZV9")
    mle24_div = get_data("https://www.moneydj.com/funddj/yp/wb05.djhtm?a=SHZV9")
    
    # 取出安聯(DSP5)網頁上真實的淨值日期，如果沒抓到才用今天的日期當備案
    real_nav_date = dsp5_nav["date"]
    if not real_nav_date:
        real_nav_date = datetime.now().strftime("%Y-%m-%d")
        
    return {
        "nav": dsp5_nav["value"], 
        "div": dsp5_div["value"], 
        "jpm_nav": jpm_nav["value"], 
        "jpm_div": jpm_div["value"],
        "frp4_nav": frp4_nav["value"],
        "frp4_div": frp4_div["value"],
        "mle24_nav": mle24_nav["value"],
        "mle24_div": mle24_div["value"],
        
        # 這裡從「現在時間」改成了「真實網頁上的淨值日期」
        "date": real_nav_date 
    }

with open('data.json', 'w') as f:
    json.dump(get_fund_data(), f)
