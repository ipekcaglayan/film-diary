from django.urls import path
from . import views
from films import views as films_views

app_name = 'profile'
urlpatterns = [
    path('x/<str:city>/', views.MyProfile.as_view(), name='profile'),
    path('review_detail/<int:id>/', views.ReviewDetail.as_view(), name="detail"),
    # path('watchlater/', views.watch_later, name='watch later'),
    path('addreview/<int:id>/', views.AddReview.as_view(), name='add review'),
    path('edit/<int:id>/', views.edit_review, name='edit review'),
    path('ajax/', views.WatchedButtonAjax.as_view(), name='buttonAjax'),
    path('like/', views.LikeButtonAjax.as_view(), name='likeAjax'),
    path('watchl/', views.WatchlistAjax.as_view(), name='watchlist ajax'),
    path('later/', views.WatchLaterAjax.as_view(), name='watchLaterAjax'),
    path('filmlistajax/', views.RemoveListAjax.as_view(), name='film_list_ajax'),
    path('deletelist/', views.DeleteListAjax.as_view(), name='delete_list_ajax'),
    path('watchedfilms/', films_views.WatchedFilms.as_view(), name='watched films'),
    path('lists/<int:id>/', views.ListDetail.as_view(), name='list detail'),
    path('createlist/', views.create_list, name='create list'),
    path('addfilm/<int:id>/', views.film_to_list, name='film to list'),
    path('watchedajax/', views.WatchedAjax.as_view(), name='watchedAjax'),
    path('deletereviewajax/', views.DeleteReviewAjax.as_view(), name='delete review ajax'),
    path('likereview/', views.LikeReview.as_view(), name='like review ajax'),
    path('likelist/', views.LikeList.as_view(), name='like list ajax'),

]
