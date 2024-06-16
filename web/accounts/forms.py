from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

import re

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='電子郵件', max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise forms.ValidationError("請輸入有效的電子郵件地址。")
        return email

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())
