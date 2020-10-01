import abc
from typing import List

from movie_app.domainmodel import *

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_actor(self, new_actor: actor.Actor):
        """ Adds an Actor to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_actor(self, actor_full_name: str) -> actor.Actor:
        """ Returns the Actor with the given full name from this repository.

        If there is no Actor with the given full name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_director(self, new_director: director.Director):
        """ Adds a Director to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_director(self, director_full_name: str) -> director.Director:
        """ Returns the Director with the given full name from this repository.

        If there is no Director with the given full name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, new_genre: genre.Genre):
        """ Adds a Genre to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> List[genre.Genre]:
        """ Returns the Genres stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, new_movie: movie.Movie):
        """ Adds a movie to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, title: str, release_year: int) -> movie.Movie:
        """ Returns the Movie with the given title and release year from this repository.

        If there is no Movie with the given title and release year, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, new_review: review.Review):
        """ Adds a Review to the repository.

        If the Review doesn't have bidirectional links with a Movie and a User,
        this method raises a RepositoryException and doesn't update the repository.
        """
        if new_review.user is None or new_review not in new_review.user.reviews:
            raise RepositoryException('Review not correctly linked to a User')
        if new_review.movie is None or new_review not in new_review.movie.reviews:
            raise RepositoryException('Review is not correctly linked to a Movie')

    @abc.abstractmethod
    def get_review(self, review_id: int) -> review.Review:
        """ Returns Review with the given id from the repository.

        If there is no Review with the given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, new_user: user.User):
        """ Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name: str) -> user.User:
        """ Returns the User with the given username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_watchlist(self, new_watchlist: watchlist.WatchList):
        """ Adds a Watchlist to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_watchlist(self, watchlist_id: int) -> watchlist.WatchList:
        """ Returns Watchlist with the given id from the repository.

        If there is no Watchlist with the given id, this method returns None.
        """
        raise NotImplementedError
