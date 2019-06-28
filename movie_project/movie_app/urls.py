from django.contrib import admin
from django.urls import path
from .views import index, AdminView, CreatePerson, EditPerson, ListPerson, CreateMovie, ListMovie, EditMovie, \
    CreateMovieRate, Movies, Login, Logout, SerializerView, SerializerDetail, MovieUpdateView, MovieListView, \
    ViewSets, MoviesDownloader, SuggestedMovies
from django.conf import settings
from django.conf.urls.static import static

app_name = 'movie_app'

urlpatterns = [
    path('', index, name='index'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('administration/', AdminView.main, name='administration'),
    path('administration/add/person/', CreatePerson.as_view(), name='create_person'),
    path('administration/people/', ListPerson.as_view(), name='list_people'),
    path('administration/edit/person/<pk>', EditPerson.as_view(), name='edit_person'),
    path('administration/add/movie/', CreateMovie.as_view(), name='create_movie'),
    path('administration/movies/', ListMovie.as_view(), name='list_movies'),
    path('administration/edit/movie/<pk>', EditMovie.as_view(), name='edit_movie'),
    path('administration/add/rate/', CreateMovieRate.as_view(), name='create_movie_rate'),
    # path('movies/', Movies.as_view(), name='movies'),
    path('serializer/', SerializerView.as_view(), name='serializer'),
    path('detail/<pk>', SerializerDetail.as_view(), name='detail'),
    path('movie/', MovieListView.as_view(), name='movie_list_create'),
    path('movie/<pk>', MovieUpdateView.as_view(), name='movie_detail_update_delete'),
    path('movies/<int:pk>/', ViewSets.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy', 'patch': 'partial_update'}), name='first'),
    path('movies/', ViewSets.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update'}), name='second'),
    path('movies/download', MoviesDownloader.as_view(), name='download'),
    path('movies/suggest', SuggestedMovies.as_view(), name='suggested_movies'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)