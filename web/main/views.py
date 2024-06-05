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
        data = data["records"]
        return render(request, 'weekly.html', {'data': data})
    return render(request, 'weekly.html')
