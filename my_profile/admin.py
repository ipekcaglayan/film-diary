from django.contrib import admin
from .models import Review, Watch, SeenFilm
# Register your models here.
admin.site.register(Review)
admin.site.register(Watch)
admin.site.register(SeenFilm)