from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from ..forms import Signup
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import random

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = Signup(request.POST)
        if form.is_valid():
            password = form.clean_password2()
            username = form.clean_username()
            print(username)
            print(password)
            user = authenticate(request, username=username, password=password)
            if user is None:
                new_user = User.objects.create_user(username, None, password)
                new_user.save()
                login(request, new_user)
                return redirect('/')
            else:
                messages.error(request, 'User already exits!')      
    else:
        form = Signup()
    if not request.user.is_authenticated:
        if 'username' not in request.session:
            name = random.choice(settings.NAMES)
            request.session['username'] = name
            request.session.set_expiry(42)
        name = request.session.get('username')
        login_id = 0
    else:
        name = request.user.username
        login_id = 1
    return render(request, 'signup.html', {'username': name, "login": login_id, 'form': form})