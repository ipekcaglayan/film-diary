from django.shortcuts import render, redirect
from .models import Film, Genre, FilmLike
from my_profile.models import Review, SeenFilm, Watch
from films.models import FilmList, ListName


# Create your views here.


def movies(request):
    keyword = request.GET.get("keyword")
    if keyword:
        films = Film.objects.filter(title__icontains=keyword)
        return render(request, 'films/movies.html', {'films': films})
    films = Film.objects.all().order_by('title')
    return render(request, 'films/movies.html', {'films': films})


def film_detail(request, id):
    detailed_film = Film.objects.get(id=id)
    genres = detailed_film.genres.all()
    film_reviews = Review.objects.filter(film__title=detailed_film.title)
    if request.user.is_authenticated:
        added_watchlist = Watch.objects.filter(user=request.user, film=detailed_film)
        added = list(SeenFilm.objects.filter(film=detailed_film, user=request.user))
        liked = FilmLike.objects.filter(film=detailed_film, user=request.user)
        return render(request, 'films/film_detail.html',
                      {'detailed_film': detailed_film, 'genres': genres, 'film_reviews': film_reviews, 'added': added,
                       'liked': liked, 'added_watchlist': added_watchlist})
    else:
        return render(request, 'films/film_detail.html',
                      {'detailed_film': detailed_film, 'genres': genres, 'film_reviews': film_reviews})


def genres(request):
    keyword = request.GET.get("keyword")
    if keyword:
        all_genres = Genre.objects.filter(name__icontains=keyword)
        return render(request, 'films/genres.html', {'genres': all_genres})
    all_genres = Genre.objects.all().order_by('name')
    return render(request, 'films/genres.html', {'genres': all_genres})


def genre_detail(request, id):
    genre = Genre.objects.get(id=id)
    genre_films = Film.objects.filter(genres__name=genre.name)
    return render(request, 'films/genre_detail.html', {'genre_films': genre_films, 'genre': genre})


def watched_films(request):
    seen_films = SeenFilm.objects.filter(user=request.user)
    return render(request, 'films/watched_films.html', {'seen_films': seen_films})


def all_lists(request):
    list_names = ListName.objects.all().order_by('-date')
    list_films = []
    for name in list_names:
        if list(FilmList.objects.filter(list=name)):
            last_added = FilmList.objects.filter(list=name).order_by('-date')[0]
            list_films.append((list(FilmList.objects.filter(list=name)[:3]), name, last_added.date))
    return render(request, 'films/all_lists.html', {'list_films': list_films})
