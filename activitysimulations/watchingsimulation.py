from typing import List, Iterable
from domainmodel.movie import Movie
from domainmodel.user import User
from domainmodel.review import Review


class MovieWatchingSimulation:

    def __init__(self, movie: 'Movie'):
        if isinstance(movie, Movie):
            self.__movie = movie
        else:
            self.__movie = None

        self.__users: List['User'] = list()
        self.__reviews: List['Review'] = list()

    @property
    def movie(self) -> 'Movie':
        return self.__movie

    @property
    def users(self) -> Iterable['User']:
        return iter(self.__users)

    @property
    def reviews(self) -> Iterable['Review']:
        return iter(self.__reviews)

    def add_user(self, user: 'User'):
        if isinstance(user, User) and user not in self.__users and user.user_name is not None:
            self.__users.append(user)

    def remove_user(self, user: 'User'):
        if user in self.__users:
            self.__users.remove(user)

    def watch_movie(self):
        for user in self.__users:
            user.watch_movie(self.__movie)

    def add_user_review(self, user: 'User', review: 'Review'):
        if user in self.__users and review.movie == self.__movie:
            user.add_review(review)

            if review in user.reviews and review not in self.__reviews:
                self.__reviews.append(review)
