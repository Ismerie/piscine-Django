from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import random
import time
from ..models import Tip
from ..forms import For_tip
from django.contrib.auth.models import User

def home(request):
    if not request.user.is_authenticated:
        if 'username' not in request.session:
            username = random.choice(settings.NAMES)
            request.session['username'] = username
            request.session.set_expiry(42)
        name = request.session.get('username')
        login = 0
        form_tip = 0
    else:
        name = request.user.username
        login = 1
        if request.method == 'POST':
            form_tip = For_tip(request.POST)
            if form_tip.is_valid():
                text = form_tip.cleaned_data.get('text')
                tip1 = Tip.objects.create(content=text, auteur=User.objects.get(username=name))
                tip1.save()
        else:
            form_tip = For_tip()
    tips = Tip.objects.all()
    print(tips)
    print(login)
    return render(request, 'index.html', {'username': name, 'login': login, 'tip': tips, "form_tip": form_tip, "tips": tips})