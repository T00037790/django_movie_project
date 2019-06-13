from django import forms
from .models import Movie, MoviePerson, MovieRate
from .choices import ROLES


class MoviePersonForm(forms.ModelForm):
    class Meta:
        model = MoviePerson

        fields = [
            'name',
            'age',
            'role',

        ]
        labels = {
            'name': 'Name',
            'age': 'Age',
            'role': 'Role',
        }
        widgets = {
            'name': forms.TextInput(),
            'age': forms.NumberInput(),
            'role': forms.Select(),
        }


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie

        fields = [
            'title',
            'duration',
            'detail',
            'poster',
            'movie_people',
            'trailer_url',
            'genre',
            'original_language',
            'release_date',
            'country',

        ]
        labels = {
             'title': 'Title',
             'duration': 'Duration',
             'detail': 'Detail',
             'poster': 'Poster',
             'movie_people': 'Actors and Directors',
             'trailer_url': 'Trailer URL',
             'genre': 'Genre',
             'original_language': 'Original Language',
             'release_date': 'Release Date',
             # 'country': 'Country',
        }
        widgets = {
            #  'title': forms.TextInput(),
            #  'duration': forms.NumberInput(),
            #  'detail': forms.TextInput(),
            #  'movie_people': forms.SelectMultiple(),
            # 'poster': forms.ImageField(),
            #  'trailer_url': forms.URLInput(),
            #  'genre': forms.SelectMultiple(),
            #  'original_language': forms.TextInput(),
            #  'release_date': forms.DateField(),
            # 'country': forms.TextInput(),

        }


class MovieRateForm(forms.ModelForm):
    class Meta:
        model = MovieRate
        fields = [
            'movie',
            'user',
            'comment',
            'rating',
            ]

        labels = {
            'movie': 'Movie',
            'user': 'User',
            'comment': 'Comment',
            'rating': 'Rating',
        }

        widgets = {
            'movie': forms.Select(),
            'user': forms.Select(),

        }

