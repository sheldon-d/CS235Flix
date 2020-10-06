import abc
from typing import List

from movie_app.domainmodel import Actor, Director, Genre, Movie, Review, User, WatchList
from movie_app.datafilereaders import MovieFileCSVReader
from movie_app.activitysimulations import MovieWatchingSimulation

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_actor(self, actor: Actor):
        """ Adds an Actor to the repository. """
        if not isinstance(actor, Actor) or actor.actor_full_name is None:
            raise RepositoryException('Actor provided is either of the wrong type or missing a full name')

    @abc.abstractmethod
    def get_actor(self, actor_full_name: str) -> Actor:
        """ Returns the Actor with the given full name from this repository.

        If there is no Actor with the given full name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_actors_by_colleagues(self, colleagues: List[Actor]) -> List[Actor]:
        """ Returns a list of Actors with all of colleagues in the given list.

        If there are no Actors with all of the colleagues in the given list, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_director(self, director: Director):
        """ Adds a Director to the repository. """
        if not isinstance(director, Director) or director.director_full_name is None:
            raise RepositoryException('Director provided is either of the wrong type or missing a full name')

    @abc.abstractmethod
    def get_director(self, director_full_name: str) -> Director:
        """ Returns the Director with the given full name from this repository.

        If there is no Director with the given full name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        """ Adds a Genre to the repository. """
        if not isinstance(genre, Genre) or genre.genre_name is None:
            raise RepositoryException('Genre provided is either of the wrong type or missing a name')

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        """ Returns the Genres stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        """ Adds a movie to the repository. """
        if not isinstance(movie, Movie) or movie.title is None or movie.release_year is None:
            raise RepositoryException('Movie provided is either of the wrong type or missing a title or release year')

    @abc.abstractmethod
    def get_movie(self, title: str, release_year: int) -> Movie:
        """ Returns the Movie with the given title and release year from this repository.

        If there is no Movie with the given title and release year, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_by_rank(self, rank: int) -> Movie:
        """ Returns the Movie with the given rank from this repository.

        If there is no Movie with the given rank, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_release_year(self, release_year: int) -> List[Movie]:
        """ Returns a list of Movies with the given release year.

        If there are no Movies with the given release year, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_director(self, director: Director) -> List[Movie]:
        """ Returns a list of Movies with the given Director.

        If there are no Movies with the given Director, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_actors(self, actor_list: List[Actor]) -> List[Movie]:
        """ Returns a list of Movies with all of the Actors in the given list.

        If there are no Movies with all of the Actors in the given list, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_genres(self, genre_list: List[Genre]) -> List[Movie]:
        """ Returns a list of Movies with all of the Genres in the given list.

        If there are no Movies with all of the Genres in the given list, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a Review to the repository.

        If the Review doesn't have bidirectional links with a Movie and a User,
        this method raises a RepositoryException and doesn't update the repository.
        """
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Review not correctly linked to a User')
        if review.movie is None or review not in review.movie.reviews:
            raise RepositoryException('Review is not correctly linked to a Movie')

    @abc.abstractmethod
    def get_review(self, review_id: int) -> Review:
        """ Returns Review with the given id from the repository.

        If there is no Review with the given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews_for_movie(self, movie: Movie) -> List[Review]:
        """ Returns a list of Reviews for the given Movie.

        If there are no Reviews for the given Movie, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        """ Adds a User to the repository. """
        if not isinstance(user, User) or user.user_name is None or user.password is None:
            raise RepositoryException('User provided is either of the wrong type or missing a username or password')

    @abc.abstractmethod
    def get_user(self, user_name: str) -> User:
        """ Returns the User with the given username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_users_watched_movie(self, movie: Movie) -> List[User]:
        """ Returns a list of Users who have watched the given Movie.

        If no Users have watched the given Movie, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_watchlist(self, watchlist: WatchList):
        """ Adds a Watchlist to the repository.

        If the Watchlist doesn't have a bidirectional link with a User,
        this method raises a RepositoryException and doesn't update the repository.
        """
        if watchlist.user is None or watchlist is not watchlist.user.watchlist:
            raise RepositoryException('Watchlist not correctly linked to a User')

    @abc.abstractmethod
    def get_watchlist(self, watchlist_id: int) -> WatchList:
        """ Returns Watchlist with the given id from the repository.

        If there is no Watchlist with the given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_movie_file_csv_reader(self, movie_file_reader: MovieFileCSVReader):
        """ Sets a MovieFileCSVReader object for the repository. """
        if not isinstance(movie_file_reader, MovieFileCSVReader) or movie_file_reader.file_name is None:
            raise RepositoryException('Movie file CSV reader provided is either of the wrong type or does not have a \
            valid csv filename')

    @abc.abstractmethod
    def get_movie_file_csv_reader(self) -> MovieFileCSVReader:
        """ Returns the MovieFileCSVReader object from the repository.

        If there is no MovieFileCSVReader object, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_watching_sim(self, watching_sim: MovieWatchingSimulation):
        """ Adds a MovieWatchingSimulation object to the repository. """
        if not isinstance(watching_sim, MovieWatchingSimulation) or watching_sim.movie is None:
            raise RepositoryException('Movie watching simulation provided is either of the wrong type \
            or missing a Movie to watch')

    @abc.abstractmethod
    def get_watching_sim(self, watching_sim_id: int) -> MovieWatchingSimulation:
        """ Returns a MovieWatchingSimulation object with the given id from the repository.

        If there is no MovieWatchingSimulation object with the given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_watching_sims_for_movie(self, movie: Movie) -> List[MovieWatchingSimulation]:
        """ Returns a list of MovieWatchingSimulations for the given Movie.

        If there are none for the given Movie, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_watching_sims_by_users(self, user_list: List[User]) -> List[MovieWatchingSimulation]:
        """ Returns a list of MovieWatchingSimulations with all of the Users in the given list.

        If there are none with all of the Users in the given list, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def load_movie_dataset(self):
        """ Loads the Actor, Director, Genre, and Movie datasets with all provided attributes from the
            MovieFileCSVReader object
        """
        raise NotImplementedError

    @abc.abstractmethod
    def load_users_and_watch_lists(self):
        raise NotImplementedError

    @abc.abstractmethod
    def load_reviews(self):
        raise NotImplementedError

    @abc.abstractmethod
    def load_activity_simulations(self):
        raise NotImplementedError

    @abc.abstractmethod
    def populate(self, data_path: str):
        raise NotImplementedError
