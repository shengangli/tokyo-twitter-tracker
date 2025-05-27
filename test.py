import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

# 1. suginami from city page
url_suginami = 'https://suumo.jp/ms/chuko/tokyo/city/'
res1 = requests.get(url_suginami, headers=headers)
res1.encoding = res1.apparent_encoding
soup1 = BeautifulSoup(res1.text, 'html.parser')

suginami_label = soup1.find('label', {'for': 'sa04_sc115'})
suginami_count = suginami_label.find('span', class_='searchitem-list-value').text.strip('()') if suginami_label else '0'

# 2. nishiogikita from search page
url_nishiogi = 'https://suumo.jp/jj/bukken/kensaku/JJ010FB009/?ar=030&bs=011&ta=13&jspIdFlg=patternShikugun&sc=13115&kb=1&kt=9999999&mb=0&mt=9999999&ekTjCd=&ekTjNm=&tj=0&cnb=0&cn=9999999'
res2 = requests.get(url_nishiogi, headers=headers)
res2.encoding = res2.apparent_encoding
soup2 = BeautifulSoup(res2.text, 'html.parser')

nishiogi_label = soup2.find('label', {'for': '13115026'})
nishiogi_count = nishiogi_label.find('span', class_='searchitem-list-value').text.strip('()') if nishiogi_label else '0'

# ✅ Final Output
print(f"suginami {suginami_count}")
print(f"nishiogikita {nishiogi_count}")
