from django.shortcuts import render

def django(request):
    return render(request, 'django.html')

def affichage(request):
    return render(request, 'affichage.html')

def templates(request):
    return render(request, 'templates.html')

# Create your views here.
