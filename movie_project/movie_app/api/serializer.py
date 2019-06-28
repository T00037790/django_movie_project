from rest_framework import serializers
from django.db import models
from movie_app.models import Actor

from movie_app.models import MovieSearch


class MovieSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50)
    duration = serializers.IntegerField()
    detail = serializers.CharField()
    genre = serializers.CharField(max_length=50)
    original_language = serializers.CharField(max_length=50)
    release_date = serializers.DateField()
    country = serializers.CharField(max_length=50)
    poster = serializers.ImageField()
    # actor = serializers.CharField()
    director = serializers.CharField()


class MoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieSearch
        fields = ('title', 'duration', 'detail', 'genre', 'original_language', 'country', 'release_date', 'poster')
