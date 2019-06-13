from django.contrib import admin
from django.urls import path
from .views import index, AdminView, CreatePerson, EditPerson, ListPerson, CreateMovie, ListMovie, EditMovie, \
    CreateMovieRate, Movies
from django.conf import settings
from django.conf.urls.static import static
app_name = 'movie_app'

urlpatterns = [
    path('', index, name='index'),
    path('administration/', AdminView.main, name='administration'),
    path('administration/add/person/', CreatePerson.as_view(), name='create_person'),
    path('administration/people/', ListPerson.as_view(), name='list_people'),
    path('administration/edit/person/<pk>', EditPerson.as_view(), name='edit_person'),
    path('administration/add/movie/', CreateMovie.as_view(), name='create_movie'),
    path('administration/movies/', ListMovie.as_view(), name='list_movies'),
    path('administration/edit/movie/<pk>', EditMovie.as_view(), name='edit_movie'),
    path('administration/add/rate/', CreateMovieRate.as_view(), name='create_movie_rate'),
    path('movies/', Movies.as_view(), name='movies'),
    # path('', include('movie_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)