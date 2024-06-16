from django.shortcuts import render, redirect

# Create your views here.

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm,LoginForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print('User registered successfully')
            return redirect('user_login')
        else:
            print(form.errors)  # 打印表單錯誤信息
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to the home page or any other page after login
                return redirect('current_weather')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})
