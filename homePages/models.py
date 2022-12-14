from django.db import models
from datetime import datetime, timedelta

# Create your models here.


class Album(models.Model):
    name = models.CharField(max_length=150)
    uri = models.CharField(max_length=30)

    def __str__(self):
        return (self.name)
    class Meta:
        db_table = "album"

class Track(models.Model):
    name = models.CharField(max_length=50)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return (self.name)
    class Meta:
        db_table = "track"

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=13, blank=True)

    class Meta:
        db_table = "user"

    def __str__(self) :
        return (self.full_name)
    
    @property
    def full_name(self) :
        return '%s %s' % (self.first_name, self.last_name)

    def save(self) :
        self.first_name = self.first_name.upper()
        self.last_name = self.last_name.upper()
        super(User, self).save()

class User_Favorite_Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_favorite_album"
    
    def __str__(self):
        return_string = self.user.first_name + ': ' + self.album.name
        return (return_string)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    stars = models.IntegerField(null=False, blank=False, default=0)
    album_image = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = "review"

    def __str__(self) :
        return_string = self.user.first_name + ': ' + self.album.name + ': ' + str(self.stars)
        return (return_string)
