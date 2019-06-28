from django import forms
from django.contrib.auth.hashers import check_password

from .models import Movie, MoviePerson, MovieRate, User, Suggest
from django.core.exceptions import ValidationError


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


class AuthenticationForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def clean(self):
        data = super(AuthenticationForm, self).clean()
        if not self.errors:
            username = data['username']
            try:
                query_user = User.objects.get(username=username)
            except Exception:
                raise ValidationError('Username does not exist!')
            query_user = User.objects.get(username=username)
            match_check = check_password(data['password'], query_user.password)
            if not match_check:
                raise ValidationError('incorrect password')
        return data


class MovieDownloader(forms.Form):
    movie_name = forms.CharField()


class SuggestForm(forms.ModelForm):
    class Meta:
        model = Suggest
        fields = ['movie_title']
        labels = {'movie_title': 'Suggested Movies'}
        widgets = {'movie': forms.TextInput()}
