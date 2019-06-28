import requests
from datetime import datetime

from celery import group, chord
from django.conf.global_settings import EMAIL_HOST_USER
from .models import MovieSearch, Actor, Director
import urllib.request
from django.core.files import File
from movie_project.celery import app
from django.core.mail import send_mail
from .models import Suggest

# app = get_current_app()


@app.task()
def add(x, y):
    print(x + y)
    return x + y


@app.task()
def downloader():
    movies = Suggest.objects.all()
    if movies.count() > 1:
        chord(group(download_movie.s(movie.movie_title) for movie in movies), sending_mail.s()).delay()
        Suggest.objects.all().delete()


@app.task()
def sending_mail(title):
    """

    Args:
        title:

    Returns:

    """
    list_movies = ''
    for movie in title:
        list_movies += movie + ', '
    send_mail(
        "Movie Download Process",
        f'movie with title: {list_movies}, was downloaded successfully',
        EMAIL_HOST_USER,
        ['izzymovil@gmail.com'],
        fail_silently=False,
    )


@app.task()
def download_movie(movie_title):
    url = 'http://www.omdbapi.com/?s={}&apikey=1645c9f'.format(movie_title)
    response = requests.get(url)
    imdbID_array = [i['imdbID'] for i in response.json()['Search']]
    movies_array = [(requests.get('http://www.omdbapi.com/?i={}&apikey=1645c9f&type=movies'.format(i))).json() for i
                    in imdbID_array]
    for movie in movies_array:
        title = movie['Title']
        released = movie['Released']
        released = datetime.strptime(released, '%d %b %Y')
        duration = movie['Runtime']

        if duration != "N/A":

            duration = duration.split()
            duration = int(duration[0])
        else:
            duration = None
        director = movie['Director']
        actors = movie['Actors'].split(', ')
        poster = movie['Poster']
        genre = movie['Genre']
        detail = movie['Plot']
        language = movie['Language'][0]
        country = movie['Country']
        instances_actor_array = []
        states_actor_array = []
        # save actor in Actor model
        for actor in actors:
            actor_instance, actor_state = Actor.objects.get_or_create(name=actor)
            instances_actor_array.append(actor_instance)
            states_actor_array.append(actor_state)

        director_instance = []
        if director != 'N/A':
            director_instance, director_state = Director.objects.get_or_create(name=director)
        else:
            director = None
        result = urllib.request.urlretrieve(poster, 'media/image.jpg')
        poster = File(open('media/image.jpg', 'rb'))
        defaults = {'duration': duration, 'poster': poster, 'director': director_instance}
        print(director, type(director))
        try:
            instance, state = MovieSearch.objects.get_or_create(title=title, detail=detail,
                                                                genre=genre, original_language=language,
                                                                release_date=released, country=country,
                                                                defaults=defaults
                                                                )
            if state:
                instance.actor.add(*instances_actor_array)
        except Exception as e:
            print(e)
    return movie_title
