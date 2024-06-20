from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, user_login, user_logout, reset_password


urlpatterns = [
    path('register/', (register), name='register'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='logout'),
    path('reset_password/', reset_password,name='reset_password'),
     path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
]
