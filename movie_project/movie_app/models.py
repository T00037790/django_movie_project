from django.db import models
from django.contrib.auth import get_user_model
from .choices import GENRES, RATING, ROLES, DEFAULT_GENRE


User = get_user_model()


class MoviePerson(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    role = models.CharField(max_length=25, choices=ROLES)

    def __str__(self):
        return '{} is an {}'.format(self.name, self.role)


class Movie(models.Model):
    title = models.CharField(max_length=50)
    duration = models.IntegerField()
    detail = models.TextField(max_length=150)
    poster = models.ImageField(upload_to='movie_app/posters', max_length=100, default=None)
    movie_people = models.ManyToManyField(MoviePerson)
    trailer_url = models.URLField()
    genre = models.CharField(max_length=50, choices=GENRES, default=DEFAULT_GENRE)
    rating = models.FloatField(null=True, blank=True)
    original_language = models.CharField(max_length=50)
    release_date = models.DateField()
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    def image_url(self):
        if self.poster and hasattr(self.poster, 'url'):
            return self.poster.url


class MovieRate(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=150)
    rating = models.IntegerField(choices=RATING)

    def __str__(self):
        return '{} has {} of rate from {}'.format(self.movie, self.rating, self.user)


class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)


class MovieSearch(models.Model):
    title = models.CharField(max_length=50)
    duration = models.IntegerField(null=True)
    detail = models.TextField(max_length=150)
    genre = models.CharField(max_length=50)
    original_language = models.CharField(max_length=50)
    release_date = models.DateField()
    country = models.CharField(max_length=50)
    poster = models.ImageField(upload_to='movie_app/posters', null=True, max_length=100, default=None, blank=True)
    actor = models.ManyToManyField('Actor')
    director = models.ForeignKey('Director', on_delete=models.CASCADE, null=True)


class Actor(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Suggest(models.Model):
    movie_title = models.CharField(max_length=100)

