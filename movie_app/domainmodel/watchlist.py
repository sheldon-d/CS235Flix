from typing import List, TYPE_CHECKING
from movie_app.domainmodel.movie import Movie

if TYPE_CHECKING:
    from movie_app.domainmodel.user import User


class WatchList:

    def __init__(self):
        self.__watch_list: List[Movie] = list()
        self.__user = None
        self.__id = id(self)

    @property
    def user(self) -> 'User':
        return self.__user

    @user.setter
    def user(self, user: 'User'):
        from movie_app.domainmodel.user import User
        if isinstance(user, User) and user.user_name is not None and self.__user is None:
            self.__user = user

    @property
    def id(self) -> int:
        return self.__id

    def add_movie(self, movie: Movie):
        if isinstance(movie, Movie) and movie not in self.__watch_list and movie.title is not None:
            self.__watch_list.append(movie)

    def remove_movie(self, movie: Movie):
        if movie in self.__watch_list:
            self.__watch_list.remove(movie)

    def select_movie_to_watch(self, index: int) -> Movie:
        if isinstance(index, int) and 0 <= index < len(self.__watch_list):
            return self.__watch_list[index]

    def size(self) -> int:
        return len(self.__watch_list)

    def first_movie_in_watchlist(self) -> Movie:
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

    def __eq__(self, other) -> bool:
        if not isinstance(other, WatchList):
            return False
        return self.__watch_list == other.__watch_list and self.__user == other.__user

    def __hash__(self):
        return hash((self.__user, self.__id))
