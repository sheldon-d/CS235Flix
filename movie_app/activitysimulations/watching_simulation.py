from typing import List, Iterable
from movie_app.domainmodel.movie import Movie
from movie_app.domainmodel.user import User
from movie_app.domainmodel.review import Review


class MovieWatchingSimulation:
    __watching_sim_id = 1

    def __init__(self, movie: Movie):
        if isinstance(movie, Movie):
            self.__movie = movie
        else:
            self.__movie = None

        self.__users: List[User] = list()
        self.__reviews: List[Review] = list()
        self.__id: int = MovieWatchingSimulation.__watching_sim_id

        MovieWatchingSimulation.__watching_sim_id += 1

    @property
    def movie(self) -> Movie:
        return self.__movie

    @property
    def users(self) -> Iterable[User]:
        return iter(self.__users)

    @property
    def reviews(self) -> Iterable[Review]:
        return iter(self.__reviews)

    @property
    def id(self) -> int:
        return self.__id

    def __repr__(self) -> str:
        return f"<MovieWatchingSimulation {self.__movie}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, MovieWatchingSimulation):
            return False
        return self.__movie == other.__movie and self.__users == other.__users and self.__reviews == other.__reviews

    def __hash__(self):
        return hash((self.__movie, self.__id))

    def add_user(self, user: User):
        if isinstance(user, User) and user not in self.__users and user.user_name is not None:
            self.__users.append(user)

    def remove_user(self, user: User):
        if user in self.__users:
            self.__users.remove(user)

    def watch_movie(self):
        for user in self.__users:
            user.watch_movie(self.__movie)

    def add_user_review(self, user: User, review: Review):
        if user in self.__users and (review.user is None or review.user is user) and \
                review.movie is self.__movie and review.movie in user.watched_movies:
            user.add_review(review)

            if review in user.reviews and review in self.__movie.reviews and review not in self.__reviews:
                self.__reviews.append(review)

    def remove_user_review(self, review: Review):
        if review in self.__reviews:
            self.__reviews.remove(review)
            review.user.remove_review(review)

    @staticmethod
    def reset_id():
        MovieWatchingSimulation.__watching_sim_id = 1
