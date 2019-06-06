from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class MoviePerson(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    ROLES = (
        ('actor', 'Actor'),
        ('director', 'Director')
    )
    role = models.CharField(max_length=25, choices=ROLES)

    def __str__(self):
        return '{} is an {}'.format(self.name, self.role)


class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=50)
    duration = models.IntegerField()
    detail = models.TextField(max_length=150)
    movie_people = models.ManyToManyField(MoviePerson)
    trailer_url = models.URLField()
    genre = models.ManyToManyField(Genre)
    rating = models.FloatField()
    original_language = models.CharField(max_length=50)
    release_date = models.DateField()
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class MovieRate(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=150)
    RATING = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    rating = models.IntegerField(choices=RATING)

    def __str__(self):
        return '{} has {} of rate'.format(self.movie, self.rating)
