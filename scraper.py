import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

# 加入反快取 (Cache-Control 等) 標頭，強制抓取最新網頁資料
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
        for td in all_td:
            text = td.text.strip()
            if re.match(r'^\d+\.\d+$', text):
                return text
        return "0.00"
    except:
        return "0.00"

def get_fund_data():
    # 1. 安聯收益成長 (DSP5)
    dsp5_nav = get_data("https://www.moneydj.com/funddj/ya/yp010001.djhtm?a=TLZ64")
    dsp5_div = get_data("https://www.moneydj.com/funddj/yp/wb05.djhtm?a=TLZ64")
    
    # 2. 摩根多重收益 (JFP11)
    jpm_nav = get_data("https://www.moneydj.com/funddj/ya/yp010001.djhtm?a=jfzn3")
    jpm_div = get_data("https://www.moneydj.com/funddj/yp/wb05.djhtm?a=JFZN3")

    # 3. 富蘭克林坦伯頓全球債 (FRP4)
    frp4_nav = get_data("https://www.moneydj.com/funddj/ya/yp010001.djhtm?a=FLZ92")
    frp4_div = get_data("https://www.moneydj.com/funddj/yp/wb05.djhtm?a=FLZ92")

    # 4. 貝萊德世界科技 (MLE24)
    mle24_nav = get_data("https://www.moneydj.com/funddj/ya/yp010001.djhtm?a=SHZV9")
    mle24_div = get_data("https://www.moneydj.com/funddj/yp/wb05.djhtm?a=SHZV9")
    
    return {
        "nav": dsp5_nav, 
        "div": dsp5_div, 
        "jpm_nav": jpm_nav, 
        "jpm_div": jpm_div,
        "frp4_nav": frp4_nav,
        "frp4_div": frp4_div,
        "mle24_nav": mle24_nav,
        "mle24_div": mle24_div,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

with open('data.json', 'w') as f:
    json.dump(get_fund_data(), f)
