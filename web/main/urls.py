from django.urls import path
from .views import weekly_report


urlpatterns = [
    path('weekly_report/', weekly_report, name='weekly_report'),
]