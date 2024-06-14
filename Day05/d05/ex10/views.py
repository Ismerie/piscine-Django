from django.shortcuts import render
from django.http import HttpResponse
from .forms import MovieFilterForm
from .models import People, Movies

def movie_filter_view(request):
    if request.method == 'POST':
        form = MovieFilterForm(request.POST)
        if form.is_valid():
            min_date = form.cleaned_data['min_release_date']
            max_date = form.cleaned_data['max_release_date']
            min_diameter = form.cleaned_data['planet_diameter_greater_than']
            gender = form.cleaned_data['character_gender']
            
            results = People.objects.filter(
                gender=gender,
                movies__release_date__range=(min_date, max_date),
                homeworld__diameter__gte=min_diameter
            ).distinct()
            display_result = []
            for person in results:
                for movie in person.movies.filter(release_date__range=(min_date, max_date)):
                    one_result = {
                        'name': person.name,
                        'gender': person.gender,
                        'title': movie.title,
                        'homeworld' : person.homeworld,
                        'diameter': person.homeworld.diameter
                    }
                    display_result.append(one_result)
            if results.exists():
                return render(request, 'ex10/results.html', {'results': display_result})
            else:
                return HttpResponse("Nothing corresponding to your research")
    else:
        form = MovieFilterForm()

    return render(request, 'ex10/movie_filter.html', {'form': form})