from django.shortcuts import render, redirect
from .models import Review, Watch, SeenFilm, ReviewLike
from films.models import Film, ListName, FilmList, FilmLike, ListLike
from accounts.models import Profile
from django.contrib.auth.models import User
from . import forms
from django.http import JsonResponse
from django.views import View
from django.db.models import Count


# list_names = ListName.objects.all().order_by('-date')
#         list_films = []
#
#         for name in list_names:
#
#             if list(FilmList.objects.filter(list=name)):
#                 last_added = FilmList.objects.filter(list=name).order_by('-date')[0]
#                 list_films.append((list(FilmList.objects.filter(list=name)[:3]), name, last_added.date,
#                                    list(ListLike.objects.filter(list=name, user=request.user))))
#         return render(request, 'films/all_lists.html', {'list_films': list_films})
class MyProfile(View):
    def get(self, request, city, username):
        form = forms.CreateList()
        pp_form = forms.ProfilePicture()
        user = request.user
        seen_films = SeenFilm.objects.filter(user=request.user)
        reviews = Review.objects.filter(author=request.user).order_by('-date')
        movies = Watch.objects.filter(user=request.user)
        list_names = ListName.objects.filter(user=request.user).order_by('-date')
        list_films = []
        seen_film_number = SeenFilm.objects.filter(user_id=request.user.id).values("user_id").annotate(
            count=Count('film'))
        review_number = Review.objects.filter(author_id=request.user.id).values("author_id").annotate(
            count=Count('film'))
        list_number = ListName.objects.filter(user_id=request.user.id).values("user_id").annotate(
            count=Count('list_name'))
        if seen_film_number:
            seen_film_number = seen_film_number[0]['count']
        else:
            seen_film_number = 0
        if list_number:
            list_number = list_number[0]['count']
        else:
            list_number = 0
        if review_number:
            review_number = review_number[0]['count']
        else:
            review_number = 0

        liked_reviews = ReviewLike.objects.filter(user=request.user)
        liked_films = FilmLike.objects.filter(user=request.user)
        liked_lists = ListLike.objects.filter(user=request.user)
        liked_list_films = []
        for liked_list in liked_lists:
            if list(FilmList.objects.filter(list=liked_list.list)):
                liked_list_films.append(
                    ((list(FilmList.objects.filter(list=liked_list.list)[:3])), liked_list.list))
        for name in list_names:
            if list(FilmList.objects.filter(list=name)):
                list_films.append((list(FilmList.objects.filter(list=name).order_by('-date')[:3]), name, name.date))
            else:
                list_films.append(([], name, name.date))
        return render(request, 'my_profile/my_profile.html',
                      {'user': user, 'seen_films': seen_films, 'reviews': reviews, 'movies': movies,
                       'list_films': list_films, 'city': city, 'form': form, 'liked_list_films': liked_list_films,
                       'liked_films': liked_films, 'liked_reviews': liked_reviews, 'username': username,
                       'pp_form': pp_form, 'seen_film_number': seen_film_number, 'list_number': list_number,
                       'review_number': review_number})


# def my_profile(request, city):
#     user = request.user
#     seen_films = SeenFilm.objects.filter(user=request.user)
#     reviews = Review.objects.filter(author=request.user).order_by('date')
#     movies = Watch.objects.filter(user=request.user)
#     list_names = ListName.objects.filter(user=request.user)
#     list_films = []
#     for name in list_names:
#         if list(FilmList.objects.filter(list=name)):
#             list_films.append((list(FilmList.objects.filter(list=name)[:3]), name, name.date))
#         else:
#             list_films.append(([], name, name.date))
#     return render(request, 'my_profile/my_profile.html',
#                   {'user': user, 'seen_films': seen_films, 'reviews': reviews, 'movies': movies,
#                    'list_films': list_films, 'city': city})


# def reviews(request):
#     reviews = Review.objects.filter(author=request.user).order_by('date')
#     return render(request, 'my_profile/reviews.html', {'reviews': reviews})

# def watchlist(request):
#     movies = Watch.objects.filter(user=request.user)
#     return render(request, 'my_profile/watchlist.html', {'movies': movies})

class ReviewDetail(View):
    def get(self, request, id):
        review = Review.objects.get(id=id)
        liked = ReviewLike.objects.filter(review=review, user=request.user)
        form = forms.EditReview()
        return render(request, 'my_profile/review_detail.html', {'review': review, 'form': form, 'liked': liked})


# def review_detail(request, id):
#     review = Review.objects.get(id=id)
#     return render(request, 'my_profile/review_detail.html', {'review': review})


# def watch_later(request):
#     if request.method == 'POST':
#         form = forms.AddFilm(request.POST, request.FILES)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.user = request.user
#             instance.save()
#             return redirect('profile:watchlist')
#     else:
#         form = forms.AddFilm()
#     return render(request, "my_profile/add_watchlater.html", {'form': form})

# class AddReviewAjax(View):
#     def post(self, request):
#         data = {'success': False}
#         film_id = request.POST['film_id']
#         film = Film.objects.get(id=film_id)
#         form = forms.AddReview(request.POST, request.FILES)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.author = request.user
#             instance.film = film
#             instance.save()
#             SeenFilm.objects.create(film=instance.film, user=request.user)
#         return JsonResponse(data)

class AddReview(View):
    def post(self, request, id):
        form = forms.AddReview(request.POST, request.FILES)
        if form.is_valid():
            film = Film.objects.get(id=id)
            instance = form.save(commit=False)
            instance.author = request.user
            instance.film = film
            instance.save()
            if not list(SeenFilm.objects.filter(film=film, user=request.user)):
                SeenFilm.objects.create(film=film, user=request.user)
            return redirect('films:detail', id=id)

    def get(self, request):
        form = forms.AddReview()
        return render(request, "my_profile/add_review.html", {'form': form, 'id': id})


# def add_review(request, id):
#     if request.method == 'POST':
#         form = forms.AddReview(request.POST, request.FILES)
#         if form.is_valid():
#             film = Film.objects.get(id=id)
#             instance = form.save(commit=False)
#             instance.author = request.user
#             instance.film = film
#             instance.save()
#             SeenFilm.objects.create(film=film, user=request.user)
#             return redirect('films:detail', id=id)
#     else:
#         form = forms.AddReview()
#     return render(request, "my_profile/add_review.html", {'form': form, 'id': id})


def edit_review(request, id):
    review = Review.objects.get(id=id)
    if request.method == 'POST':
        form = forms.EditReview(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return redirect('profile:detail', id=id)
    else:
        form = forms.EditReview(instance=review)
        return render(request, 'my_profile/edit_review.html', {'form': form})


class WatchedButtonAjax(View):
    def post(self, request):
        data = {'success': True}
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


# def watched_button_ajax(request):
#     data = {'success': True}
#     if request.method == 'POST':
#         film_id = request.POST['film_id']
#         film = Film.objects.get(id=film_id)
#         added = SeenFilm.objects.filter(film=film, user=request.user)
#         if not list(added):
#             SeenFilm.objects.create(film=film, user=request.user)
#             data['success'] = True
#         else:
#             added.delete()
#             data['success'] = False
#     return JsonResponse(data)


# def user_lists(request):
#     list_names = ListName.objects.filter(user=request.user)
#     list_films = []
#     for name in list_names:
#         if list(FilmList.objects.filter(list=name)):
#             list_films.append((list(FilmList.objects.filter(list=name)[:3]), name, name.date))
#         else:
#             list_films.append(([], name, name.date))
#     return render(request, 'films/user_lists.html', {'list_films': list_films})


class ListDetail(View):
    def get(self, request, id):
        user = request.user
        form = forms.FilmToList()
        list_name = ListName.objects.get(id=id)
        list_films = FilmList.objects.filter(list=list_name)
        liked = ListLike.objects.filter(list=list_name, user=request.user)
        if list(FilmList.objects.filter(list=list_name)):
            last_added = FilmList.objects.filter(list=list_name).order_by('-date')[0]
            return render(request, 'films/list_detail.html',
                          {'list_films': list_films, 'list_name': list_name, 'last_update': last_added.date,
                           'form': form, 'user': user, 'liked': liked})
        return render(request, 'films/list_detail.html',
                      {'list_films': list_films, 'list_name': list_name, 'form': form, 'user': user, 'liked': liked})


# def list_detail(request, id):
#     list_name = ListName.objects.get(id=id)
#     list_films = FilmList.objects.filter(list=list_name)
#     if list(FilmList.objects.filter(list=list_name)):
#         last_added = FilmList.objects.filter(list=list_name).order_by('-date')[0]
#         return render(request, 'films/list_detail.html',
#                       {'list_films': list_films, 'list_name': list_name, 'last_update': last_added.date})
#     return render(request, 'films/list_detail.html',
#                   {'list_films': list_films, 'list_name': list_name})


def create_list(request):
    if request.method == 'POST':
        form = forms.CreateList(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('profile:profile', city='lists', username=request.user.username)
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
            return redirect('profile:list detail', id=id)
    else:
        form = forms.FilmToList()
    return render(request, "films/film_to_list.html", {'form': form, 'list_name': list_name})


class LikeButtonAjax(View):
    def post(self, request):
        data = {'success': True}
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


# def like_button_ajax(request):
#     data = {'success': True}
#     if request.method == 'POST':
#         film_id = request.POST['film_id']
#         film = Film.objects.get(id=film_id)
#         liked = FilmLike.objects.filter(film=film, user=request.user)
#         if not list(liked):
#             FilmLike.objects.create(film=film, user=request.user)
#             data['success'] = True
#         else:
#             liked.delete()
#             data['success'] = False
#     return JsonResponse(data)

class WatchlistAjax(View):
    def post(self, request):
        data = {'success': False}
        film_id = request.POST['film_id']
        film = Film.objects.get(id=film_id)
        Watch.objects.get(film=film).delete()
        data['success'] = True
        return JsonResponse(data)


# def watchlist_ajax(request):
#     data = {'success': False}
#     if request.method == 'POST':
#         film_id = request.POST['film_id']
#         film = Film.objects.get(id=film_id)
#         Watch.objects.get(film=film).delete()
#         data['success'] = True
#
#     return JsonResponse(data)


class WatchLaterAjax(View):
    def post(self, request):
        data = {'success': True}
        film_id = request.POST['film_id']
        film = Film.objects.get(id=film_id)
        watch_list = Watch.objects.filter(film=film, user=request.user)
        if not list(watch_list):
            Watch.objects.create(film=film, user=request.user)
            data['success'] = True
        else:
            watch_list.delete()
            data['success'] = False
        return JsonResponse(data)


# def watch_later_ajax(request):
#     data = {'success': True}
#     if request.method == 'POST':
#         film_id = request.POST['film_id']
#         film = Film.objects.get(id=film_id)
#         watch_list = Watch.objects.filter(film=film, user=request.user)
#         if not list(watch_list):
#             Watch.objects.create(film=film, user=request.user)
#             data['success'] = True
#         else:
#             watch_list.delete()
#             data['success'] = False
#     return JsonResponse(data)

class RemoveListAjax(View):
    def post(self, request):
        data = {'success': False}
        print(request)
        if request.method == 'POST':
            film_id = request.POST['film_id']
            list_name = request.POST['list_name']
            film = Film.objects.get(id=film_id)
            film_list = ListName.objects.get(list_name=list_name)
            FilmList.objects.get(film=film, list=film_list).delete()
            data['success'] = True

        return JsonResponse(data)

    # def remove_list_ajax(request):
    #     data = {'success': False}
    #     if request.method == 'POST':
    #         film_id = request.POST['film_id']
    #         list_name = request.POST['list_name']
    #         film = Film.objects.get(id=film_id)
    #         film_list = ListName.objects.get(list_name=list_name)
    #         FilmList.objects.get(film=film, list=film_list).delete()
    #         data['success'] = True
    #
    #     return JsonResponse(data)


class DeleteListAjax(View):
    def post(self, request):
        data = {'success': False}
        name_id = request.POST['name_id']
        ListName.objects.get(id=int(name_id)).delete()
        data['success'] = True
        return JsonResponse(data)


# def delete_list_ajax(request):
#     data = {'success': False}
#     if request.method == 'POST':
#         name_id = request.POST['name_id']
#         ListName.objects.get(id=int(name_id)).delete()
#         data['success'] = True
#
#     return JsonResponse(data)


class WatchedAjax(View):
    def post(self, request):
        data = {'success': True}
        film_id = request.POST['film_id']
        film = Film.objects.get(id=film_id)
        watched = SeenFilm.objects.filter(film=film, user=request.user)
        if not list(watched):
            SeenFilm.objects.create(film=film, user=request.user)
            data['success'] = True
        else:
            watched.delete()
            data['success'] = False
        return JsonResponse(data)


# def watched_ajax(request):
#     data = {'success': True}
#     if request.method == 'POST':
#         film_id = request.POST['film_id']
#         film = Film.objects.get(id=film_id)
#         watched = SeenFilm.objects.filter(film=film, user=request.user)
#         if not list(watched):
#             SeenFilm.objects.create(film=film, user=request.user)
#             data['success'] = True
#         else:
#             watched.delete()
#             data['success'] = False
#     return JsonResponse(data)

class DeleteReviewAjax(View):
    def post(self, request):
        data = {'success': False}
        review_id = request.POST['review_id']
        Review.objects.get(id=review_id).delete()
        data['success'] = True
        return JsonResponse(data)


# def delete_review_ajax(request):
#     data = {'success': False}
#     if request.method == 'POST':
#         review_id = request.POST['review_id']
#         Review.objects.get(id=review_id).delete()
#         data['success'] = True
#
#     return JsonResponse(data)

class LikeReview(View):
    def post(self, request):
        data = {'success': True}
        review_id = request.POST['review_id']
        review = Review.objects.get(id=review_id)
        liked = ReviewLike.objects.filter(review=review, user=request.user)
        if not list(liked):
            ReviewLike.objects.create(review=review, user=request.user)
            data['success'] = True
        else:
            liked.delete()
            data['success'] = False
        return JsonResponse(data)


class LikeList(View):
    def post(self, request):
        data = {'success': True}
        list_name_id = request.POST['list_name_id']
        list_name = ListName.objects.get(id=list_name_id)
        liked_list = ListLike.objects.filter(list=list_name, user=request.user)
        if not list(liked_list):
            ListLike.objects.create(list=list_name, user=request.user)
            data['success'] = True
        else:
            liked_list.delete()
            data['success'] = False
        return JsonResponse(data)


class OtherProfile(View):
    def get(self, request, username):
        istenen_user = User.objects.get(username=username)
        print(istenen_user.username)
        seen_films = SeenFilm.objects.filter(user=istenen_user)
        reviews = Review.objects.filter(author=istenen_user).order_by('-date')
        movies = Watch.objects.filter(user=istenen_user)
        list_names = ListName.objects.filter(user=istenen_user).order_by('-date')
        list_films = []

        liked_reviews = ReviewLike.objects.filter(user=istenen_user)
        liked_films = FilmLike.objects.filter(user=istenen_user)
        liked_lists = ListLike.objects.filter(user=istenen_user)
        liked_list_films = []
        seen_film_number = SeenFilm.objects.filter(user_id=istenen_user.id).values("user_id").annotate(
            count=Count('film'))
        if seen_film_number:
            seen_film_number = seen_film_number[0]['count']
        else:
            seen_film_number = 0
        review_number = Review.objects.filter(author_id=istenen_user.id).values("author_id").annotate(
            count=Count('film'))
        if review_number:
            review_number = review_number[0]['count']
        else:
            review_number = 0

        list_number = ListName.objects.filter(user_id=istenen_user.id).values("user_id").annotate(
            count=Count('list_name'))
        if list_number:
            list_number = list_number[0]['count']
        else:
            list_number = 0
        for liked_list in liked_lists:
            if list(FilmList.objects.filter(list=liked_list.list)):
                liked_list_films.append(
                    ((list(FilmList.objects.filter(list=liked_list.list)[:3])), liked_list.list))
        for name in list_names:
            if list(FilmList.objects.filter(list=name)):
                list_films.append((list(FilmList.objects.filter(list=name).order_by('-date')[:3]), name, name.date))
            else:
                list_films.append(([], name, name.date))
        return render(request, 'my_profile/other_profiles.html',
                      {'istenen_user': istenen_user, 'seen_films': seen_films, 'reviews': reviews, 'movies': movies,
                       'list_films': list_films, 'liked_list_films': liked_list_films,
                       'liked_films': liked_films, 'liked_reviews': liked_reviews, 'list_number': list_number,
                       'review_number': review_number, 'seen_film_number': seen_film_number})


class UploadPicture(View):
    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        form = forms.ProfilePicture(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile:profile', city='watched', username=request.user.username)

    def get(self, request):
        form = forms.ProfilePicture()
        return render(request, "my_profile/upload picture.html", {'form': form})
