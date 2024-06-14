from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from ..forms import Signin
from django.contrib import messages
import random
from django.contrib.auth.models import User


def signin(request):
    if request.user.is_authenticated:
        return redirect('/')
    if not request.user.is_authenticated:
        if 'username' not in request.session:
            username = random.choice(settings.NAMES)
            request.session['username'] = username
            request.session.set_expiry(42)
        name = request.session.get('username')
        login_id = 0
    else:
        name = request.user.username
        login_id = 1
    if request.method == "POST":
        form = Signin(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print(user)
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Wrong password!')
    else:
        form = Signin()
    return render(request, 'signin.html', {'username': name, "login" : login_id, 'form': form})