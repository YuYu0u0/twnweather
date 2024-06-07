from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from cwa.CWA_weatherAPI import WeatherAPI
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("api_key")

@csrf_exempt
def weekly_report(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        weather_api = WeatherAPI(api_key)
        data = weather_api.get_weekly_forcast_weather_data(city)
        weatherdatas = data["records"]["locations"][0]["location"][0]["weatherElement"]

        PoP12h = weatherdatas[0]["time"]
        Wx = weatherdatas[6]["time"]
        minT = weatherdatas[8]["time"]
        maxT = weatherdatas[12]["time"]
        
        

        from collections import defaultdict
        from datetime import datetime

        def get_period(time):
            hour = datetime.fromisoformat(time).hour
            return 'night' if hour == 18 else 'day'

        grouped_data = defaultdict(lambda: {'day': {'minT': '', 'maxT': '', 'weather': '', 'PoP12h': ''}, 'night': {'minT': '', 'maxT': '', 'weather': '', 'PoP12h': ''}})

        for entry in minT:
            start_time = entry['startTime']
            date = start_time.split(' ')[0]
            period = get_period(start_time)
            grouped_data[date][period]['minT'] = entry['elementValue'][0]["value"]

        for entry in maxT:
            start_time = entry['startTime']
            date = start_time.split(' ')[0]
            period = get_period(start_time)
            grouped_data[date][period]['maxT'] = entry['elementValue'][0]["value"]

        for entry in Wx:
            start_time = entry['startTime']
            date = start_time.split(' ')[0]
            period = get_period(start_time)
            grouped_data[date][period]['weather'] = entry['elementValue'][0]["value"]

        for entry in PoP12h:
            start_time = entry['startTime']
            date = start_time.split(' ')[0]
            period = get_period(start_time)
            grouped_data[date][period]['PoP12h'] = entry['elementValue'][0]["value"]

        # 將 defaultdict 轉換為字典
        grouped_data = dict(grouped_data)
        return render(request, 'weekly.html', {'data': grouped_data,"city":city} )
    return render(request, 'weekly.html')
