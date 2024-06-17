from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
# Create your views here.
from datetime import datetime
from collections import defaultdict
from dotenv import load_dotenv
import os

from cwa.CWA_weatherAPI import WeatherAPI
load_dotenv()
api_key = os.getenv("api_key")


def index(request):
    return render(request, "index.html")

@login_required
@csrf_exempt
def weekly_report(request):
    def get_period(time):
        hour = datetime.fromisoformat(time).hour
        return 'night' if hour == 18 else 'day'

    city = request.POST.get('city') if request.method == 'POST' else request.session.get('last_city', '')
    if not city:
        return render(request, 'weekly.html')

    weather_api = WeatherAPI(api_key)
    data = weather_api.get_weekly_forcast_weather_data(city)
    weatherdatas = data["records"]["locations"][0]["location"][0]["weatherElement"]

    PoP12h = weatherdatas[0]["time"]
    Wx = weatherdatas[6]["time"]
    minT = weatherdatas[8]["time"]
    maxT = weatherdatas[12]["time"]

    grouped_data = defaultdict(lambda: {'day': {'minT': '', 'maxT': '', 'weather': '', 'PoP12h': ''}, 'night': {
        'minT': '', 'maxT': '', 'weather': '', 'PoP12h': ''}})

    for data_type, weather_data in zip(['minT', 'maxT', 'Wx', 'PoP12h'], [minT, maxT, Wx, PoP12h]):
        for entry in weather_data:
            start_time = entry['startTime']
            date = start_time.split(' ')[0]
            period = get_period(start_time)
            grouped_data[date][period][data_type] = entry['elementValue'][0]["value"]

    grouped_data = dict(grouped_data)
    request.session['last_city'] = city
    return render(request, 'weekly.html', {'data': grouped_data, "city": city})


@login_required
@csrf_exempt
def current_weather(request):
    weather_api = WeatherAPI(api_key)
    data = weather_api.get_instant_weather_data()
    data = data["records"]['Station']

    current = dict()
    for v in data:
        cities = v['GeoInfo']['CountyName']
        town = v['GeoInfo']['TownName']
        weather = v["WeatherElement"]['Weather']
        station = v['StationName']
        temperature = v["WeatherElement"]['AirTemperature']
        if v["WeatherElement"]['Weather'] == '-99':
            weather = '-'

        # 如果 city 不在 current 字典中，則初始化為一個空列表
        if cities not in current:
            current[cities] = []

        # 將當前記錄添加到對應的城市列表中
        current[cities].append({
            "town": town,
            "station": station,
            "weather": weather,
            "temperature": temperature
        })
    if request.method == 'POST':
        city = request.POST.get('city')
        if "台" in city:
            city = city.replace("台", "臺")
        if city in current:
            request.session['last_city'] = city
            return render(request, 'now.html', {"data": current[city], "city": city})
    
    last_city = request.session.get('last_city', '')
    if last_city and last_city in current:
        return render(request, 'now.html', {"data": current[last_city], "city": last_city})
    
    return render(request, 'now.html', {"data": " "})


@login_required
def recent_earthquake(request):
    weatherAPI = WeatherAPI(api_key)
    data = weatherAPI.get_earthquake_data()
    reports = data["records"]["Earthquake"]
    earthquake_info = list()
    for report in reports:
        report_time = datetime.strptime(
            report["EarthquakeInfo"]["OriginTime"], "%Y-%m-%d %H:%M:%S")
        formatted_time = report_time.strftime("%Y-%m-%d %I:%M %p")
        location = report["EarthquakeInfo"]["Epicenter"]["Location"]
        dept = report["EarthquakeInfo"]["FocalDepth"]
        magnitude = report["EarthquakeInfo"]["EarthquakeMagnitude"]["MagnitudeValue"]
        earthquake_info.append([formatted_time, location, dept, magnitude])
    return render(request, "earthquake.html", {"data": earthquake_info[:5]})
