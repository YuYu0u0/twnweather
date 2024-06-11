from django.urls import path
from .views import index,weekly_report,current_weather


urlpatterns = [
    path('',index,name='index'),
    path('weekly_report/', weekly_report, name='weekly_report'),
    path('current_weather/',current_weather, name='current_weather'),
]