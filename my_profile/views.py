from django.shortcuts import render, redirect
from .models import Review, Watch, SeenFilm
from films.models import Film, ListName, FilmList, FilmLike
from accounts.models import Profile
from . import forms
from django.http import JsonResponse


def my_profile(request):
    user = request.user
    return render(request, 'my_profile/my_profile.html', {'user': user})




def reviews(request):
    reviews = Review.objects.filter(author=request.user).order_by('date')
    return render(request, 'my_profile/reviews.html', {'reviews': reviews})


def watchlist(request):
    movies = Watch.objects.filter(user=request.user)
    return render(request, 'my_profile/watchlist.html', {'movies': movies})


def review_detail(request, id):
    review = Review.objects.get(id=id)
    return render(request, 'my_profile/review_detail.html', {'review': review})


def watch_later(request):
    if request.method == 'POST':
        form = forms.AddFilm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('profile:watchlist')
    else:
        form = forms.AddFilm()
    return render(request, "my_profile/add_watchlater.html", {'form': form})


def add_review(request):
    if request.method == 'POST':
        form = forms.AddReview(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            SeenFilm.objects.create(film=instance.film, user=request.user)
            return redirect('profile:reviews')
    else:
        form = forms.AddReview()
    return render(request, "my_profile/add_review.html", {'form': form})


def edit_review(request, id):
    review = Review.objects.get(id=id)
    if request.method == 'POST':
        form = forms.EditReview(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return redirect('profile:reviews')
    else:
        form = forms.EditReview(instance=review)
        return render(request, 'my_profile/edit_review.html', {'form': form})


def watched_button_ajax(request):
    data = {'success': True}
    if request.method == 'POST':
        film_id = request.POST['film_id']
        film = Film.objects.get(id=film_id)
        added = SeenFilm.objects.filter(film=film, user=request.user)
        if not list(added):
            SeenFilm.objects.create(film=film, user=request.user)
            data['success'] = True
        else:
            added.delete()
            data['success'] = False
    return JsonResponse(data)


def lists(request):
    list_names = ListName.objects.filter(user=request.user)
    return render(request, 'films/lists.html', {'list_names': list_names})


def list_detail(request, id):
    list_name = ListName.objects.get(id=id)
    list_films = FilmList.objects.filter(list=list_name)
    return render(request, 'films/list_detail.html', {'list_films': list_films, 'list_name': list_name})


def create_list(request):
    if request.method == 'POST':
        form = forms.CreateList(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('profile:lists')
    else:
        form = forms.CreateList()
    return render(request, "films/create_list.html", {'form': form})


def film_to_list(request, id):
    list_name = ListName.objects.get(id=id)
    if request.method == 'POST':
        form = forms.FilmToList(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.list = list_name
            instance.save()
            return redirect('profile:lists')
    else:
        form = forms.FilmToList()
    return render(request, "films/list_to_film.html", {'form': form, 'list_name': list_name})


def like_button_ajax(request):
    data = {'success': True}
    if request.method == 'POST':
        film_id = request.POST['film_id']
        film = Film.objects.get(id=film_id)
        liked = FilmLike.objects.filter(film=film, user=request.user)
        if not list(liked):
            FilmLike.objects.create(film=film, user=request.user)
            data['success'] = True
        else:
            liked.delete()
            data['success'] = False
    return JsonResponse(data)


def resume(request):
    return render(request, 'homepage/resume.html')
