from django.shortcuts import render
from django.conf import settings

# Create your views here.
from cwa.CWA_weatherAPI import WeatherAPI
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("api_key")


def weekly_report(request):
    weather_api = WeatherAPI(api_key)
    location = request.GET.get('location', 'Taipei')
    print(location)
    data = weather_api.get_weekly_forcast_weather_data(location)

    return render(request,'weekly.html',data)
