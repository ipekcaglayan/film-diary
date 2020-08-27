from django.shortcuts import render
from films.models import Film
from my_profile.models import Review, SeenFilm
from django.db.models import Count


def homepage(request):
    film = Film.objects.get(id=30)
    film2 = Film.objects.get(id=31)
    reviews = Review.objects.all().order_by('-date')[:6]
    dictionary = SeenFilm.objects.values("film_id").annotate(count=Count('film')).order_by("-count")
    popular_films=[]
    for ele in dictionary:
        film = Film.objects.get(id=ele['film_id'])
        popular_films.append(film)

    return render(request, 'homepage/index.html',
                  {'film': film, 'film2': film2, 'reviews': reviews, 'popular_films': popular_films})
