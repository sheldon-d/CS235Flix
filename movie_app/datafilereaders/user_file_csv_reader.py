import csv
from typing import List, Dict, Iterable
from pathlib import Path

from movie_app.domainmodel import User, Movie


class UserFileCSVReader:

    def __init__(self, file_name: str, movies: Dict[int, Movie]):
        if isinstance(file_name, str) and Path(file_name).exists() and '.csv' in file_name:
            self.__file_name = file_name
        else:
            self.__file_name = None

        self.__dataset_of_users: List[User] = list()
        self.__dataset_of_movies: Dict[int, Movie] = movies

    @property
    def file_name(self) -> str:
        return self.__file_name

    @property
    def dataset_of_users(self) -> Iterable[User]:
        return iter(self.__dataset_of_users)

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csv_file:
            user_file_reader = csv.DictReader(csv_file)

            User.reset_id()
            for row in user_file_reader:
                user_name = row['Name']
                password = row['Password']

                user = User(user_name, password)

                for val in row['Watched Movie Ranks'].split(','):
                    try:
                        movie_rank = int(val)

                        if movie_rank in self.__dataset_of_movies.keys():
                            watched_movie = self.__dataset_of_movies[movie_rank]
                            user.watch_movie(watched_movie)
                    except ValueError:
                        pass    # Ignore exception and don't add movie to watched movies

                if user not in self.__dataset_of_users and user.id is not None:
                    self.__dataset_of_users.append(user)
