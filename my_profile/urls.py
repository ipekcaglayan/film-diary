from django.urls import path
from . import views
from films import views as films_views

app_name = 'profile'
urlpatterns = [
    path('<str:city>/', views.my_profile, name='profile'),
    # path('reviews/', views.reviews, name='reviews'),
    # path('watchlist/', views.watchlist, name='watchlist'),
    path('<int:id>/', views.review_detail, name="detail"),
    path('watchlater/', views.watch_later, name='watch later'),
    path('addreview/', views.add_review, name='add review'),
    path('edit/<int:id>/', views.edit_review, name='edit review'),
    path('ajax/', views.watched_button_ajax, name='buttonAjax'),
    path('like/', views.like_button_ajax, name='likeAjax'),
    path('watchl/', views.watchlist_ajax, name='watchlist ajax'),
    path('later/', views.watch_later_ajax, name='watchLaterAjax'),
    path('filmlistajax/', views.remove_list_ajax, name='film_list_ajax'),
    path('deletelist/', views.delete_list_ajax, name='delete_list_ajax'),
    path('watchedfilms/', films_views.watched_films, name='watched films'),
    # path('lists/', views.user_lists, name='lists'),
    path('lists/<int:id>/', views.list_detail, name='list detail'),
    path('createlist/', views.create_list, name='create list'),
    path('addfilm/<int:id>/', views.film_to_list, name='film to list'),
    path('watchedajax/', views.watched_ajax, name='watchedAjax'),
    path('deletereviewajax/', views.delete_review_ajax, name='delete review ajax'),

]
