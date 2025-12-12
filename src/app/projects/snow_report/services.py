import os, json
import requests
from bs4 import BeautifulSoup

class SnowReportService:

    bergfex_url = "https://www.bergfex.com/schweiz/schneewerte/"

    def __init__(self):

        resorts_info_path = os.path.join(os.path.dirname(__file__), "config", "resort_info.json")
        with open(resorts_info_path) as f:
            self.resorts_info = json.load(f)

    def get_snow_data(self):

        bergfex_page = self._get_bergfex_page()

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
            resort_info = self.resorts_info.get(resort, {})

            entry = {
                "resort_name": resort,
                "snow_valley_cm": self._parse_snow_depth(cols[1]),
                "snow_mountain_cm": self._parse_snow_depth(cols[2]),
                "new_snow_cm": self._parse_snow_depth(cols[3]),
                "lifts_open": cols[4],
                
                "region": resort_info.get("region"),
                "resort_url": resort_info.get("url")
            }

            resorts.append(entry)

        return resorts
    
    def _get_bergfex_page(self):
        response = requests.get(self.bergfex_url, timeout=20)
        response.raise_for_status()
        return response.text

    def _parse_snow_depth(self, text):
        if(text == '-'):
            return None
        else:
            return text.replace("cm", "")