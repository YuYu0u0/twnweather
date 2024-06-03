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
        date = datetime.now().strftime("%y_%m_%d")
        filename = f"{date}_{category}.json"
        with open(f"jsondata/{filename}", 'w+', encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    category = ["earthquake_report",
                "36hr_weather_forcast", "weekly_weather_forcast"]
    api_key = os.getenv("api_key")
    weatherAPI = WeatherAPI(api_key)
    data = weatherAPI.get_earthquake_data()
    data2 = weatherAPI.get_36hr_weather_forecast_data("台北市")
    data3 = weatherAPI.get_typhoon_warning()
    data4 = weatherAPI.get_weather_warning()
    data5 = weatherAPI.get_instant_weather_data()
    weatherAPI.save_data(data2, category[1])
    print(data5)
