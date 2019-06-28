from django.contrib.auth.views import LogoutView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, FormView, RedirectView, DetailView
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView, \
    RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from django.contrib.sessions.backends.db import SessionStore
from .models import MoviePerson, Movie, MovieRate, UserToken, MovieSearch, Suggest
from .forms import MoviePersonForm, MovieForm, MovieRateForm, AuthenticationForm, MovieDownloader, SuggestForm
from django.contrib.auth import get_user_model, login, logout, authenticate
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password
from uuid import uuid4
from .api.serializer import MovieSerializer, MoviesSerializer
from rest_framework.authtoken.models import Token
from .tasks import download_movie, sending_mail
from celery.canvas import Signature, group, chord, chain

User = get_user_model()


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


class Login(FormView):
    form_class = AuthenticationForm
    template_name = 'movie_app/login.html'
    success_url = reverse_lazy('movie_app:administration')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            username = request.POST['username']
            try:
                query_user = User.objects.get(username=username)
            except Exception:
                query_user = None
            if query_user is not None:
                if query_user.username == username:
                    password = form.cleaned_data.get("password")
                    user = authenticate(username=username, password=password)
                    request.session['user'] = user.username
                    if user:
                        user_token = Token(user=query_user)
                        user_token.save()
                    else:
                        return self.form_invalid(form)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class Logout(RedirectView):
    pattern_name = 'movie_app:login'

    def get(self, request, *args, **kwargs):
        try:
            username = request.session['user']
            user = User.objects.get(username=username)
            token = Token.objects.filter(user_id=user.id)
            token.delete()
            del request.session['user']
        except KeyError:
            pass
        return super(Logout, self).get(request, *args, **kwargs)


class SerializerView(ListView):
    model = MovieSearch
    # template_name = 'movie_app/serializer.html'
    # queryset = MovieSearch.objects.all()
    content_type = 'application/json'
    response_class = HttpResponse

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SerializerView, self).get_context_data(object_list=object_list, **kwargs)
        context.update({'serialized_data': JSONRenderer().render(MovieSerializer(self.get_queryset(), many=True).data)})
        return context

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            context.get('serialized_data'), **response_kwargs
        )


class SerializerDetail(DetailView):
    content_type = 'application/json'
    model = MovieSearch
    response_class = HttpResponse

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SerializerDetail, self).get_context_data(object_list=object_list, **kwargs)
        context.update({'serialized_data': JSONRenderer().render(MovieSerializer(self.get_object()).data)})
        return context

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            context.get('serialized_data'), **response_kwargs
        )


# class MovieListView(ListAPIView):
#     queryset = MovieSearch.objects.all()
#     serializer_class = MoviesSerializer
#
#
# class MovieDetailView(RetrieveAPIView):
#     queryset = MovieSearch.objects.all()
#     serializer_class = MoviesSerializer
#
#
# class MovieDeleteView(DestroyAPIView):
#     queryset = MovieSearch.objects.all()
#     serializer_class = MoviesSerializer


class MovieListView(ListCreateAPIView):
    queryset = MovieSearch.objects.all()
    serializer_class = MoviesSerializer


class MovieUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = MovieSearch.objects.all()
    serializer_class = MoviesSerializer


class ViewSets(viewsets.ModelViewSet):
    """
       A viewset for viewing and editing user instances.
    """
    serializer_class = MoviesSerializer
    queryset = MovieSearch.objects.all()
    lookup_field = 'pk'


class MoviesDownloader(FormView):
    form_class = MovieDownloader
    template_name = 'movie_app/downloader.html'
    success_url = reverse_lazy('movie_app:list_movies')

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        movie_title = form.cleaned_data.get("movie_name").split(',')
        movie_title = [movie.strip() for movie in movie_title]
        print(movie_title)
        chord(group(download_movie.s(movie) for movie in movie_title), sending_mail.s()).delay()
        return super().form_valid(form)


class SuggestedMovies(CreateView):
    model = Suggest
    success_url = reverse_lazy('movie_app:administration')
    template_name = 'movie_app/admin/create/suggested_movies.html'
    form_class = SuggestForm
