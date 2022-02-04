from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from mysite.forms import UserCreationForm
from django.core.mail import send_mail
import os


def index(request):
    context = {
        "title": "hello"
    }
    return render(request, "mysite/index.html", context)


# Login画面の表示(Djangoのデフォルト)
class Login(LoginView):
    template_name = "mysite/auth.html"


# サインアップしたデータをAdminに保存している
def signup(request):
    context = {}
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
    return render(request, "mysite/auth.html", context)


def contact(request):
    context = {}

    # email
    subject = "題名"
    message = "本文テスト"
    email_from = os.environ["DEFAULT_EMAIL_FROM"]
    email_to = [os.environ["DEFAULT_EMAIL_FROM"], ]
    send_mail(subject, message, email_from, email_to)

    return render(request, "mysite/snippets/contact.html", )
