from typing import List, Iterable
from movie_app.domainmodel.movie import Movie
from movie_app.domainmodel.review import Review
from movie_app.domainmodel.watchlist import WatchList


class User:

    def __init__(self, user_name: str, password: str):
        if isinstance(user_name, str) and user_name.strip() != "":
            self.__user_name = user_name.strip().lower()
        else:
            self.__user_name = None

        if isinstance(password, str) and password.strip() != "":
            self.__password = password
        else:
            self.__password = None

        self.__id = None
        self.__watched_movies: List[Movie] = list()
        self.__reviews: List[Review] = list()
        self.__time_spent_watching_movies_minutes: int = 0
        self.__watchlist: WatchList = WatchList()

        self.__watchlist.user = self

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, user_id: int):
        if isinstance(user_id, int) and user_id > 0 and self.__id is None:
            self.__id = user_id

    @property
    def user_name(self) -> str:
        return self.__user_name

    @property
    def password(self) -> str:
        return self.__password

    @property
    def watched_movies(self) -> Iterable[Movie]:
        return iter(self.__watched_movies)

    @property
    def reviews(self) -> Iterable[Review]:
        return iter(self.__reviews)

    @property
    def time_spent_watching_movies_minutes(self) -> int:
        return self.__time_spent_watching_movies_minutes

    @property
    def watchlist(self) -> WatchList:
        return self.__watchlist

    def __repr__(self) -> str:
        return f"<User {self.__user_name}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return self.__user_name == other.__user_name

    def __lt__(self, other) -> bool:
        if self.__user_name is None:
            return other.__user_name is not None
        elif other.__user_name is None:
            return False
        return self.__user_name < other.__user_name

    def __hash__(self):
        return hash(self.__user_name)

    def watch_movie(self, movie: Movie):
        if isinstance(movie, Movie) and movie.title is not None and movie.runtime_minutes is not None:
            if movie not in self.__watched_movies:
                self.__watched_movies.append(movie)
            self.__time_spent_watching_movies_minutes += movie.runtime_minutes

    def remove_watched_movie(self, movie: Movie):
        if movie in self.__watched_movies:
            self.__watched_movies.remove(movie)

            if self.__time_spent_watching_movies_minutes >= movie.runtime_minutes:
                self.__time_spent_watching_movies_minutes -= movie.runtime_minutes

    def add_review(self, review: Review):
        if isinstance(review, Review) and review not in self.__reviews and \
                review.movie is not None and review.rating is not None and review.user is None:
            review.user = self
            self.__reviews.append(review)
            review.movie.add_review(review)

    def remove_review(self, review: Review):
        if review in self.__reviews:
            self.__reviews.remove(review)
            review.movie.remove_review(review)
