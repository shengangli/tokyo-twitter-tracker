import requests
from bs4 import BeautifulSoup
from datetime import datetime
import uuid
import os
from dotenv import load_dotenv
load_dotenv()


# Env variables from GitHub secrets
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
SUPABASE_TABLE = "listing_counts"

def insert_to_supabase(area, count):
    data = {
        "id": str(uuid.uuid4()),
        "area": area,
        "count": int(count),
        "timestamp": datetime.utcnow().isoformat()
    }
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    res = requests.post(f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}", json=data, headers=headers)
    if res.status_code not in [200, 201]:
        print(f"Insert failed for {area}: {res.text}")
    else:
        print(f"Inserted {area} {count}")

def get_counts():
    headers = {"User-Agent": "Mozilla/5.0"}

    results = {}

    # 1. suginami (sale)
    res1 = requests.get("https://suumo.jp/ms/chuko/tokyo/city/", headers=headers)
    res1.encoding = res1.apparent_encoding
    soup1 = BeautifulSoup(res1.text, "html.parser")
    label1 = soup1.find("label", {"for": "sa04_sc115"})
    results["suginami_sale"] = label1.find("span", class_="searchitem-list-value").text.strip("()").replace(",", "") if label1 else "0"

    # 2. nishiogikita (sale)
    res2 = requests.get("https://suumo.jp/jj/bukken/kensaku/JJ010FB009/?ar=030&bs=011&ta=13&jspIdFlg=patternShikugun&sc=13115&kb=1&kt=9999999&mb=0&mt=9999999&ekTjCd=&ekTjNm=&tj=0&cnb=0&cn=9999999", headers=headers)
    res2.encoding = res2.apparent_encoding
    soup2 = BeautifulSoup(res2.text, "html.parser")
    label2 = soup2.find("label", {"for": "13115026"})
    results["nishiogikita_sale"] = label2.find("span", class_="searchitem-list-value").text.strip("()").replace(",", "") if label2 else "0"

    # 3. suginami (rent)
    res3 = requests.get("https://suumo.jp/chintai/tokyo/city/", headers=headers)
    res3.encoding = res3.apparent_encoding
    soup3 = BeautifulSoup(res3.text, "html.parser")
    label3 = soup3.find("label", {"for": "la13115"})
    results["suginami_rent"] = label3.find("span", class_="searchitem-list-value").text.strip("()").replace(",", "") if label3 else "0"

    # 4. kamiogi (rent)
    res4 = requests.get("https://suumo.jp/jj/chintai/kensaku/FR301FB002/?ar=030&bs=040&ta=13&sc=13115&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1", headers=headers)
    res4.encoding = res4.apparent_encoding
    soup4 = BeautifulSoup(res4.text, "html.parser")
    label4 = soup4.find("label", {"for": "la13115012"})
    results["kamiogi_rent"] = label4.find("span", class_="searchitem-list-value").text.strip("()").replace(",", "") if label4 else "0"

    return results

if __name__ == "__main__":
    counts = get_counts()
    for area, count in counts.items():
        insert_to_supabase(area, count)
