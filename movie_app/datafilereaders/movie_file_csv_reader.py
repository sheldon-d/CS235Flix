import csv
from typing import List, Iterable
from pathlib import Path

from movie_app.domainmodel.movie import Movie
from movie_app.domainmodel.actor import Actor
from movie_app.domainmodel.genre import Genre
from movie_app.domainmodel.director import Director


class MovieFileCSVReader:

    def __init__(self, file_name: str):
        if isinstance(file_name, str) and Path(file_name).exists() and '.csv' in file_name:
            self.__file_name = file_name
        else:
            self.__file_name = None

        self.__dataset_of_movies: List[Movie] = list()
        self.__dataset_of_actors: List[Actor] = list()
        self.__dataset_of_directors: List[Director] = list()
        self.__dataset_of_genres: List[Genre] = list()

    @property
    def file_name(self) -> str:
        return self.__file_name

    @property
    def dataset_of_movies(self) -> Iterable[Movie]:
        return iter(self.__dataset_of_movies)

    @property
    def dataset_of_actors(self) -> Iterable[Actor]:
        return iter(self.__dataset_of_actors)

    @property
    def dataset_of_directors(self) -> Iterable[Director]:
        return iter(self.__dataset_of_directors)

    @property
    def dataset_of_genres(self) -> Iterable[Genre]:
        return iter(self.__dataset_of_genres)

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csv_file:
            movie_file_reader = csv.DictReader(csv_file)

            for row in movie_file_reader:
                title = row['Title']

                try:
                    release_year = int(row['Year'])
                except ValueError:
                    release_year = None

                try:
                    rank = int(row['Rank'])
                except ValueError:
                    rank = None

                description = row['Description']
                director = Director(row['Director'])
                actors = [Actor(full_name) for full_name in row['Actors'].split(',')]
                genres = [Genre(genre_name) for genre_name in row['Genre'].split(',')]

                try:
                    runtime_minutes = int(row['Runtime (Minutes)'])
                except ValueError:
                    runtime_minutes = None

                try:
                    external_rating = float(row['Rating'])
                except ValueError:
                    external_rating = None

                try:
                    rating_votes = int(row['Votes'])
                except ValueError:
                    rating_votes = None

                try:
                    revenue_millions = float(row['Revenue (Millions)'])
                except ValueError:
                    revenue_millions = None

                try:
                    metascore = int(row['Metascore'])
                except ValueError:
                    metascore = None

                movie = Movie(title, release_year)
                movie.rank = rank
                movie.description = description
                movie.director = director
                movie.runtime_minutes = runtime_minutes
                movie.external_rating = external_rating
                movie.rating_votes = rating_votes
                movie.revenue_millions = revenue_millions
                movie.metascore = metascore

                for actor in actors:
                    colleagues = [c for c in actors if not actor.check_if_this_actor_worked_with(c) and c is not actor]

                    if actor not in self.__dataset_of_actors and actor.actor_full_name is not None:
                        for colleague in colleagues:
                            actor.add_actor_colleague(colleague)
                        self.__dataset_of_actors.append(actor)
                    elif actor in self.__dataset_of_actors:
                        pos = self.__dataset_of_actors.index(actor)
                        for colleague in colleagues:
                            self.__dataset_of_actors[pos].add_actor_colleague(colleague)
                    movie.add_actor(actor)

                if director not in self.__dataset_of_directors and director.director_full_name is not None:
                    self.__dataset_of_directors.append(director)

                for genre in genres:
                    movie.add_genre(genre)
                    if genre not in self.__dataset_of_genres and genre.genre_name is not None:
                        self.__dataset_of_genres.append(genre)

                if movie not in self.dataset_of_movies and movie.title is not None:
                    self.__dataset_of_movies.append(movie)
