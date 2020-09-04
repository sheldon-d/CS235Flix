from typing import List, Iterable
from domainmodel.movie import Movie
import domainmodel.review as rev_mod


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

        self.__watched_movies: List['Movie'] = list()
        self.__reviews: List['rev_mod.Review'] = list()
        self.__time_spent_watching_movies_minutes: int = 0

    @property
    def user_name(self) -> str:
        return self.__user_name

    @property
    def password(self) -> str:
        return self.__password

    @property
    def watched_movies(self) -> Iterable['Movie']:
        return iter(self.__watched_movies)

    @property
    def reviews(self) -> Iterable['rev_mod.Review']:
        return iter(self.__reviews)

    @property
    def time_spent_watching_movies_minutes(self) -> int:
        return self.__time_spent_watching_movies_minutes

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

    def watch_movie(self, movie: 'Movie'):
        if isinstance(movie, Movie) and movie.title is not None and movie.runtime_minutes is not None:
            if movie not in self.__watched_movies:
                self.__watched_movies.append(movie)
            self.__time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review: 'rev_mod.Review'):
        if isinstance(review, rev_mod.Review) and review not in self.__reviews and \
                review.movie is not None and review.rating is not None and review.user is None:
            self.__reviews.append(review)
            review.user = self
