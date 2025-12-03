import os, json
import requests
from bs4 import BeautifulSoup

BERGFEX_URL = "https://www.bergfex.com/schweiz/schneewerte/"
RESORTS_INFO_JSON_PATH = os.path.join(os.path.dirname(__file__), "resort_info.json")

def get_resorts_info():
    with open(RESORTS_INFO_JSON_PATH) as f:
        return json.load(f)
    
def get_bergfex_page():
    response = requests.get(BERGFEX_URL,timeout=20)
    response.raise_for_status()
    return response.text

def get_snow_data():

    resorts_info = get_resorts_info()
    bergfex_page = get_bergfex_page()

    soup = BeautifulSoup(bergfex_page, "html.parser")

    # Find the first table (the main snow report table)
    table = soup.find("table")
    if not table:
        raise Exception("Could not find snow report table on Bergfex page")

    rows = table.find("tbody").find_all("tr")

    resorts = []

    for row in rows:
        
        cols = [c.get_text(strip=True) for c in row.find_all("td")]

        resort = cols[0]
        resort_info = resorts_info.get(resort, {})

        entry = {
            "resort_name": resort,
            "snow_valley_cm": parse_snow_depth(cols[1]),
            "snow_mountain_cm": parse_snow_depth(cols[2]),
            "new_snow_cm": parse_snow_depth(cols[3]),
            "lifts_open": cols[4],
            
            "region": resort_info.get("region"),
            "resort_url": resort_info.get("url")
        }

        resorts.append(entry)

    return resorts

def parse_snow_depth(text):
    if(text == '-'):
        return None
    else:
        return text.replace("cm", "")