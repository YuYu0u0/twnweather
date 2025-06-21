from django.urls import path
from .views import index, weekly_report, current_weather, recent_earthquake,check_cwb


urlpatterns = [
    path('', index, name='index'),
    path('weekly_report/', weekly_report, name='weekly_report'),
    path('current_weather/', current_weather, name='current_weather'),
    path('earthquakes_report/', recent_earthquake, name="recent_earthquake"),
    path('check_cwb/', check_cwb, name="check_cwb")
]
