from django.shortcuts import render
from films.models import Film, ListName, FilmList
from my_profile.models import Review, SeenFilm, ReviewLike
from django.db.models import Count
from django.views import View


class Homepage(View):
    def get(self, request):
        film = Film.objects.get(id=30)
        film2 = Film.objects.get(id=31)
        reviews = Review.objects.all().order_by('-date')[:6]
        reviews_liked = []
        dictionary = SeenFilm.objects.values("film_id").annotate(count=Count('film')).order_by("-count")
        popular_films = []
        for ele in dictionary:
            film = Film.objects.get(id=ele['film_id'])
            popular_films.append(film)
        list_names = ListName.objects.all().order_by('-date')[:3]
        list_films = []
        for name in list_names:
            list_films.append(list(FilmList.objects.filter(list=name)[:3]))

        for r in reviews:
            liked = list(ReviewLike.objects.filter(review=r, user=request.user))
            reviews_liked.append((r, liked))

        return render(request, 'homepage/homepage.html',
                      {'film': film, 'film2': film2, 'reviews': reviews, 'popular_films': popular_films,
                       'list_films': list_films, 'list_names': list_names, 'reviews_liked': reviews_liked})
