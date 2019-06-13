from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from .models import MoviePerson, Movie, MovieRate
from .forms import MoviePersonForm, MovieForm, MovieRateForm


def index(request):
    context = {}
    return render(request, 'movie_app/index.html', context)


class AdminView:

    @staticmethod
    def main(request):
        context = {'role': 'Admin'}
        return render(request, 'movie_app/admin/index.html', context)


class CreatePerson(CreateView):
    model = MoviePerson
    success_url = reverse_lazy('movie_app:administration')
    template_name = 'movie_app/admin/create/person.html'
    form_class = MoviePersonForm


class ListPerson(ListView):
    model = MoviePerson
    template_name = 'movie_app/admin/list/person.html'


class EditPerson(UpdateView):
    model = MoviePerson
    form_class = MoviePersonForm
    template_name = 'movie_app/admin/update/person.html'
    success_url = reverse_lazy('movie_app:list_people')


class CreateMovie(CreateView):
    model = Movie
    success_url = reverse_lazy('movie_app:administration')
    template_name = 'movie_app/admin/create/movie.html'
    form_class = MovieForm


class ListMovie(ListView):
    model = Movie
    template_name = 'movie_app/admin/list/movie.html'


class EditMovie(UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movie_app/admin/update/movie.html'
    success_url = reverse_lazy('movie_app:list_movies')


class CreateMovieRate(CreateView):
    model = MovieRate
    success_url = reverse_lazy('movie_app:administration')
    template_name = 'movie_app/admin/create/rate.html'
    form_class = MovieRateForm


class Movies(ListView):
    model = Movie
    template_name = 'movie_app/movies.html'
