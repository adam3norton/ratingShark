from django.contrib import admin
from .models import Album, Track, User, User_Favorite_Album, Review

# Register your models here.
admin.site.register(Album)
admin.site.register(Track)
admin.site.register(User)
admin.site.register(User_Favorite_Album)
admin.site.register(Review)