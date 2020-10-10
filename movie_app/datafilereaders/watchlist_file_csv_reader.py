import csv
from typing import List, Iterable
from pathlib import Path

from movie_app.domainmodel import WatchList, Movie, User


class WatchListFileCSVReader:

    def __init__(self, file_name: str, movies: List[Movie], users: List[User]):
        if isinstance(file_name, str) and Path(file_name).exists() and '.csv' in file_name:
            self.__file_name = file_name
        else:
            self.__file_name = None

        self.__dataset_of_watch_lists: List[WatchList] = list()
        self.__dataset_of_movies: List[Movie] = movies
        self.__dataset_of_users: List[User] = users

    @property
    def file_name(self) -> str:
        return self.__file_name

    @property
    def dataset_of_watch_lists(self) -> Iterable[WatchList]:
        return iter(self.__dataset_of_watch_lists)

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csv_file:
            watchlist_file_reader = csv.DictReader(csv_file)

            for row in watchlist_file_reader:
                try:
                    user_id = int(row['User ID'])
                except ValueError:
                    user_id = None

                watchlist_user = next((user for user in self.__dataset_of_users if user.id == user_id), None)

                if watchlist_user is not None and watchlist_user.id is not None:
                    for val in row['Movie Ranks'].split(','):
                        try:
                            movie_rank = int(val)
                            watch_list_movie = next((movie for movie in self.__dataset_of_movies
                                                     if movie.rank == movie_rank), None)
                            watchlist_user.watchlist.add_movie(watch_list_movie)
                        except ValueError:
                            pass    # Ignore exception and don't add movie to watchlist

                    if watchlist_user.watchlist not in self.__dataset_of_watch_lists:
                        self.__dataset_of_watch_lists.append(watchlist_user.watchlist)
