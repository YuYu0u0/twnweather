from django.urls import path
from django.urls import re_path as url




urlpatterns = [
    # path("hello/", blog.views.hello, name="hello"),
    url(r'^profile/', TemplateView.as_view(template_name='profile.html')),
    url(r'^saved/', blog.views.SaveProfile, name='SaveProfile'),
    url(r'^show/',blog.views.show,name='show'),
    url(r'^createlog/', blog.views.create_travel_log, name='create_travel_log'),
    url(r'^dailylog/', blog.views.view_travel_logs, name='travel_logs'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
]
