from urllib.request import quote
from datetime import datetime
import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()


class WeatherAPI:
    """
    連接中央氣象署開放資料
    取得json格式資料
    """
    def __init__(self, apikey: str) -> None:
        self.api_key = apikey
        self.base_url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/'

    def _get_weather_data(self, dataset_id: str, location=None):
        if location is not None:
            if "台" in location:
                location = location.replace("台", "臺")
            city = '&locationName='+quote(location, encoding="utf-8")

            url = f"{self.base_url}{dataset_id}?Authorization={self.api_key}&format=JSON{city}"
        else:
            url = f"{self.base_url}{dataset_id}?Authorization={self.api_key}&format=JSON"
        # print(url)
        try:
            res = requests.get(url, timeout=20)
            if res.status_code == 200:
                return res.json()
        except Exception as e:
            return e

    def get_earthquake_data(self):
        return self._get_weather_data("E-A0015-001")

    def get_36hr_weather_forecast_data(self, location: str):
        return self._get_weather_data("F-C0032-001", location)

    def get_weekly_forcast_weather_data(self, location: str):
        return self._get_weather_data("F-D0047-091", location)

    def get_weather_warning(self):
        return self._get_weather_data("W-C0033-001")

    def get_typhoon_warning(self):
        return self._get_weather_data("W-C0034-005")

    def get_instant_weather_data(self):
        return self._get_weather_data("O-A0003-001")

    def save_data(self, data, category):
        # Ensure the directory exists
        os.makedirs("jsondata", exist_ok=True)
        date = datetime.now().strftime("%y_%m_%d")
        filename = f"{date}_{category}.json"
        with open(f"jsondata/{filename}", 'w+', encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    category = ["earthquake_report",
                "36hr_weather_forcast", "weekly_weather_forcast"]
    api_key = os.getenv("api_key")
    weatherAPI = WeatherAPI(api_key)
    # data = weatherAPI.get_earthquake_data()
    # data2 = weatherAPI.get_36hr_weather_forecast_data("台北市")
    # data3 = weatherAPI.get_typhoon_warning()
    # data4 = weatherAPI.get_weather_warning()
    # data5 = weatherAPI.get_instant_weather_data()
    # weatherAPI.save_data(data2, category[1])
    
    data = weatherAPI.get_weekly_forcast_weather_data("台北市")
    weatherAPI.save_data(data, category[2])

    weatherdatas = data["records"]["locations"][0]["location"][0]["weatherElement"]

    PoP12h = weatherdatas[0]["time"]
    Wx = weatherdatas[6]["time"]
    minT = weatherdatas[8]["time"]
    maxT = weatherdatas[12]["time"]
    
    

    from collections import defaultdict

    grouped_data = defaultdict(lambda: {'minT': [],'maxT':[], 'weather': [], 'PoP12h': []})

    for entry in minT:
        start_time = entry['startTime']
        grouped_data[start_time]['minT'].append(entry['elementValue'])

    for entry in maxT:
        start_time = entry['startTime']
        grouped_data[start_time]['maxT'].append(entry['elementValue'])

    for entry in Wx:
        start_time = entry['startTime']
        grouped_data[start_time]['weather'].append(entry['elementValue'])
    
    for entry in PoP12h:
        start_time = entry['startTime']
        grouped_data[start_time]['PoP12h'].append(entry['elementValue'])

    # 將 defaultdict 轉換為字典
    grouped_data = dict(grouped_data)

    # 顯示整理後的資料
    print(json.dumps(grouped_data, indent=4, ensure_ascii=False))
