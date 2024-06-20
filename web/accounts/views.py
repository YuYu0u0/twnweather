from django.shortcuts import render, redirect

# Create your views here.
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm,LoginForm
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


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
                form.add_error(None, '帳號或密碼不正確')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('index')

def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "重置密碼"
                    email_template_name = "accounts/reset_email.html"
                    c = {
                        "email": user.email,
                        'domain': get_current_site(request).domain,
                        'site_name': '網站名稱',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email_content = render_to_string(email_template_name, c)
                    send_mail(subject, email_content, 'from@example.com', [user.email], fail_silently=False)
            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()
    return render(request, 'accounts/forget_password.html', {'form': form})

from django.core.exceptions import ObjectDoesNotExist
def password_reset_confirm(request, uidb64=None, token=None):
    UserModel = User
    assert uidb64 is not None and token is not None  # 保证参数不为空
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        form = SetPasswordForm(user, request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('password_reset_complete')
        return render(request, 'registration/password_reset_confirm.html', {'form': form})
    else:
        return redirect('password_reset_invalid')