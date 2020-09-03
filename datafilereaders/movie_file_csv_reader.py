import csv
from typing import List
from domainmodel.movie import Movie
from domainmodel.actor import Actor
from domainmodel.genre import Genre
from domainmodel.director import Director


class MovieFileCSVReader:

    def __init__(self, file_name: str):
        self.__file_name = file_name
        self.__dataset_of_movies: List['Movie'] = list()
        self.__dataset_of_actors: List['Actor'] = list()
        self.__dataset_of_directors: List['Director'] = list()
        self.__dataset_of_genres: List['Genre'] = list()

    @property
    def dataset_of_movies(self) -> List['Movie']:
        return self.__dataset_of_movies

    @property
    def dataset_of_actors(self) -> List['Actor']:
        return self.__dataset_of_actors

    @property
    def dataset_of_directors(self) -> List['Director']:
        return self.__dataset_of_directors

    @property
    def dataset_of_genres(self) -> List['Genre']:
        return self.__dataset_of_genres

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)

            for row in movie_file_reader:
                title = row['Title']
                release_year = int(row['Year'])
                description = row['Description']
                director = Director(row['Director'])
                actors = [Actor(full_name) for full_name in row['Actors'].split(',')]
                genres = [Genre(genre_name) for genre_name in row['Genre'].split(',')]
                runtime_minutes = int(row['Runtime (Minutes)'])

                movie = Movie(title, release_year)
                movie.description = description
                movie.director = director
                movie.runtime_minutes = runtime_minutes

                for actor in actors:
                    movie.add_actor(actor)
                    if actor not in self.__dataset_of_actors and actor.actor_full_name is not None:
                        self.__dataset_of_actors.append(actor)

                if director not in self.__dataset_of_directors and director.director_full_name is not None:
                    self.__dataset_of_directors.append(director)

                for genre in genres:
                    movie.add_genre(genre)
                    if genre not in self.__dataset_of_genres and genre.genre_name is not None:
                        self.__dataset_of_genres.append(genre)

                self.__dataset_of_movies.append(movie)
