from typing import List
from domainmodel.movie import Movie


class WatchList:

    def __init__(self):
        self.__watch_list: List['Movie'] = list()

    def add_movie(self, movie: 'Movie'):
        if isinstance(movie, Movie) and movie not in self.__watch_list and movie.title is not None:
            self.__watch_list.append(movie)

    def remove_movie(self, movie: 'Movie'):
        if movie in self.__watch_list:
            self.__watch_list.remove(movie)

    def select_movie_to_watch(self, index: int) -> 'Movie':
        if isinstance(index, int) and 0 <= index < len(self.__watch_list):
            return self.__watch_list[index]

    def size(self) -> int:
        return len(self.__watch_list)

    def first_movie_in_watchlist(self) -> 'Movie':
        if len(self.__watch_list) > 0:
            return self.__watch_list[0]

    def __iter__(self):
        self.__index = 0
        return iter(self.__watch_list)

    def __next__(self):
        if self.__index < len(self.__watch_list):
            current = self.__watch_list[self.__index]
            self.__index += 1
            return current
        else:
            raise StopIteration
