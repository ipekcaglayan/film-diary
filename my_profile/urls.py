from django.urls import path
from . import views
from films import views as films_views

app_name = 'profile'
urlpatterns = [
    path('', views.my_profile, name='profile'),
    path('reviews/', views.reviews, name='reviews'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('<int:id>/', views.review_detail, name="detail"),
    path('watchlater/', views.watch_later, name='watch later'),
    path('addreview/', views.add_review, name='add review'),
    path('edit/<int:id>/', views.edit_review, name='edit review'),
    path('ajax/', views.watched_button_ajax, name='buttonAjax'),
    path('like/', views.like_button_ajax, name='likeAjax'),
    path('watchedfilms/', films_views.watched_films, name='watched films'),
    path('lists/', views.lists, name='lists'),
    path('lists/<int:id>/', views.list_detail, name='list detail'),
    path('createlist/', views.create_list, name='create list'),
    path('addfilm/<int:id>/', views.film_to_list, name='film to list'),
    path('resume/', views.resume, name='resume'),

]
