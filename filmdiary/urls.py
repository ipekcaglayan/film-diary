"""filmdiary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from homepage import views as homepage_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from films import views as films_views
app_name = 'film diary'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage_views.homepage, name="home"),
    path('my_profile/', include('my_profile.urls'), name='my profile'),
    path('accounts/', include('accounts.urls')),
    path('films/', include('films.urls')),
    path('genres/', films_views.genres, name='genres'),
    path('genres/<int:id>', films_views.genre_detail, name="genre_detail"),
    path('lists/', films_views.all_lists, name="all lists"),

]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
