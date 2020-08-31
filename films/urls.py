from django.urls import path
from . import views
app_name = 'films'
urlpatterns = [
    path('', views.movies, name="movies"),
    path('<int:id>', views.FilmDetail.as_view(), name="detail"),
]
