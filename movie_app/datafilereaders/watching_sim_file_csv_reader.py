import csv
from typing import List, Dict, Iterable
from pathlib import Path

from movie_app.activitysimulations import MovieWatchingSimulation
from movie_app.domainmodel import Movie, User, Review


class WatchingSimFileCSVReader:

    def __init__(self, file_name: str, movies: List[Movie], users: List[User], reviews: Dict[int, Review]):
        if isinstance(file_name, str) and Path(file_name).exists() and '.csv' in file_name:
            self.__file_name = file_name
        else:
            self.__file_name = None

        self.__dataset_of_watching_sims: List[MovieWatchingSimulation] = list()
        self.__dataset_of_movies: List[Movie] = movies
        self.__dataset_of_users: List[User] = users
        self.__dataset_of_reviews: Dict[int, Review] = reviews

    @property
    def file_name(self) -> str:
        return self.__file_name

    @property
    def dataset_of_watching_sims(self) -> Iterable[MovieWatchingSimulation]:
        return iter(self.__dataset_of_watching_sims)

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csv_file:
            watching_sim_file_reader = csv.DictReader(csv_file)

            MovieWatchingSimulation.reset_id()
            for row in watching_sim_file_reader:
                try:
                    movie_rank = int(row['Movie Rank'])
                except ValueError:
                    movie_rank = None

                watching_sim_movie = next((movie for movie in self.__dataset_of_movies
                                           if movie.rank == movie_rank), None)

                if watching_sim_movie is not None:
                    watching_simulation = MovieWatchingSimulation(watching_sim_movie)

                    for val in row['User IDs'].split(','):
                        try:
                            user_id = int(val)
                            watching_sim_user = next((user for user in self.__dataset_of_users
                                                      if user.id == user_id), None)
                            watching_simulation.add_user(watching_sim_user)
                        except ValueError:
                            pass    # Ignore exception and don't add user to watching simulation

                    movie_watched = False   # checks if movie has been watched. True if a valid review exists

                    for val in row['Review IDs'].split(','):
                        try:
                            review_id = int(val)

                            if not movie_watched:
                                movie_watched = True
                                watching_simulation.watch_movie()

                            if review_id in self.__dataset_of_reviews.keys():
                                watching_sim_review = self.__dataset_of_reviews[review_id]
                                watching_simulation.add_user_review(watching_sim_review.user, watching_sim_review)
                        except ValueError:
                            pass    # Ignore exception and don't add review to watching simulation

                    if watching_simulation not in self.__dataset_of_watching_sims:
                        self.__dataset_of_watching_sims.append(watching_simulation)
