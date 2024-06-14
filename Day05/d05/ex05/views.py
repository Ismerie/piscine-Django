from django import db
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Movies
from .forms import DropdownMovieForm

def populate(request):
    movies = [
        {
            "episode_nb": 1,
            "title": "The Phantom Menace",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "1999-05-19"
        },
        {
            "episode_nb": 2,
            "title": "Attack of the Clones",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "2002-05-16"
        },
        {
            "episode_nb": 3,
            "title": "Revenge of the Sith",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "2005-05-19"
        },
        {
            "episode_nb": 4,
            "title": "A New Hope",
            "director": "George Lucas",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1977-05-25"
        },
        {
            "episode_nb": 5,
            "title": "The Empire Strikes Back",
            "director": "Irvin Kershner",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1980-05-17"
        },
        {
            "episode_nb": 6,
            "title": "Return of the Jedi",
            "director": "Richard Marquand",
            "producer": "Howard G. Kazanjian, George Lucas, Rick McCallum",
            "release_date": "1983-05-25"
        },
        {
            "episode_nb": 7,
            "title": "The Force Awakens",
            "director": "J. J. Abrams",
            "producer": "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
            "release_date": "2015-12-11"
        }
    ]

    response = []
    for value in movies:
        try:
            Movies.objects.create(
                episode_nb=value['episode_nb'],
                title=value['title'],
                director=value['director'],
                producer=value['producer'],
                release_date=value['release_date'],
            )
            response.append("OK")
        except Exception as e:
            response.append(e)

    return HttpResponse("<br/>".join(str(i) for i in response))


def display(request):
    try:
        movies = Movies.objects.all()
        if len(movies) == 0:
            return HttpResponse("No data available")
        return render(request, 'ex05/display.html', {"movies": movies})
    except Exception as e:
        return HttpResponse("No data available")

def remove(request):
    if request.method == "GET":
        try:
            movies = Movies.objects.all()
            if len(movies) == 0:
                return HttpResponse("No data available")
        except Exception as e:
            print(e)
            return HttpResponse("No data available")
        choices = ((movie.title, movie.title) for movie in movies)
        context = {"form": DropdownMovieForm(choices)}
        return render(request, "ex05/remove.html", context)
    
    elif request.method == "POST":
        try:
            movies = Movies.objects.all()
            if len(movies) == 0:
                return HttpResponse("No data available")
        except Exception as e:
            print(e)
            return HttpResponse("No data available")
        choices = ((movie.title, movie.title) for movie in movies)
        data = DropdownMovieForm(choices, request.POST)
        if data.is_valid():
            try:
                Movies.objects.get(title=data.cleaned_data['movie']).delete()
            except Exception as e:
                return print(e)
        return redirect(request.path)
