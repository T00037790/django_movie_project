import os
import urllib.request
import requests
from django.core.files import File
from django.core.management.base import BaseCommand
from movie_app.models import MovieSearch, Actor, Director
from datetime import datetime
import shutil


class Command(BaseCommand):
    help = 'fetch movies from OMDB API'

    def add_arguments(self, parser):
        # positional argument
        parser.add_argument('title', type=str)

        # kwargs like arguments
        parser.add_argument('-s', '--search', action='store_true', default=False)

    def handle(self, *args, **options):
        search = options['search']
        title = options['title']
        print(search)
        print(title)
        url = 'http://www.omdbapi.com/?s={}&apikey=1645c9f'.format(title)
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
