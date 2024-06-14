from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def logout_view(request):
    logout(request)
    return redirect('/')