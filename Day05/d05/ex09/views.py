from django.shortcuts import render
from django.http import HttpResponse
from .models import People

def display(request):
    # Filtrer les personnages dont le climat de la planète d'origine contient 'windy'
    people = People.objects.filter(homeworld__climate__icontains='windy').order_by('name')
    
    if not people.exists():
        command_line = "python3 manage.py loaddata data/ex09_initial_data.json"
        context = {
            'no_data': True,
            'command_line': command_line,
        }
    else:
        context = {
            'no_data': False,
            'people': people,
        }

    return render(request, 'ex09/display.html', context)