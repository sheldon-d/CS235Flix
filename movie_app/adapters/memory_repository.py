from typing import List, Dict

from movie_app.adapters.repository import AbstractRepository, RepositoryException
from movie_app.domainmodel import Actor, Director, Genre, Movie, Review, User, WatchList
from movie_app.datafilereaders import MovieFileCSVReader, UserFileCSVReader, ReviewFileCSVReader, \
    WatchListFileCSVReader, WatchingSimFileCSVReader
from movie_app.activitysimulations import MovieWatchingSimulation


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__actors: List[Actor] = list()
        self.__directors: List[Director] = list()
        self.__genres: List[Genre] = list()
        self.__movies: List[Movie] = list()
        self.__reviews: Dict[int, Review] = dict()
        self.__users: List[User] = list()
        self.__watch_lists: List[WatchList] = list()
        self.__movie_file_csv_reader = None
        self.__review_file_csv_reader = None
        self.__user_file_csv_reader = None
        self.__watchlist_file_csv_reader = None
        self.__watching_sim_file_csv_reader = None
        self.__watching_sims: Dict[int, MovieWatchingSimulation] = dict()

    def add_actor(self, actor: Actor):
        super().add_actor(actor)
        if actor not in self.__actors:
            self.__actors.append(actor)

    def get_actor(self, actor_full_name: str) -> Actor:
        return next((actor for actor in self.__actors if actor.actor_full_name == actor_full_name), None)

    def get_actors_by_colleagues(self, colleagues: List[Actor]) -> List[Actor]:
        # Only include colleagues which are Actors in this repository
        existing_colleagues = [actor for actor in colleagues if actor in self.__actors]

        # Fetch the Actors who have all of the existing colleagues in the given list
        actors_with_colleagues = []

        if len(existing_colleagues) == 0:
            return actors_with_colleagues

        for actor in self.__actors:
            has_worked_with_all = True

            for colleague in existing_colleagues:
                if not actor.check_if_this_actor_worked_with(colleague):
                    has_worked_with_all = False
                    break

            if has_worked_with_all and actor not in actors_with_colleagues:
                actors_with_colleagues.append(actor)

        return actors_with_colleagues

    def add_director(self, director: Director):
        super().add_director(director)
        if director not in self.__directors:
            self.__directors.append(director)

    def get_director(self, director_full_name: str) -> Director:
        return next((director for director in self.__directors
                     if director.director_full_name == director_full_name), None)

    def add_genre(self, genre: Genre):
        super().add_genre(genre)
        if genre not in self.__genres:
            self.__genres.append(genre)

    def get_genres(self) -> List[Genre]:
        return self.__genres

    def add_movie(self, movie: Movie):
        super().add_movie(movie)
        if movie not in self.__movies:
            self.__movies.append(movie)

    def get_movie(self, title: str, release_year: int) -> Movie:
        return next((movie for movie in self.__movies
                     if movie.title == title and movie.release_year == release_year), None)

    def get_movie_by_rank(self, rank: int) -> Movie:
        return next((movie for movie in self.__movies if movie.rank == rank), None)

    def get_movies_by_release_year(self, release_year: int) -> List[Movie]:
        return [movie for movie in self.__movies if movie.release_year == release_year]

    def get_movies_by_director(self, director: Director) -> List[Movie]:
        return [movie for movie in self.__movies if movie.director == director]

    def get_movies_by_actors(self, actor_list: List[Actor]) -> List[Movie]:
        # Only include Actors which are in this repository
        existing_actors = [actor for actor in actor_list if actor in self.__actors]

        # Fetch the Movies which have all of the existing actors in the given list
        movies_with_actors = []

        if len(existing_actors) == 0:
            return movies_with_actors

        for movie in self.__movies:
            has_all_actors = True

            for actor in existing_actors:
                if actor not in movie.actors:
                    has_all_actors = False
                    break

            if has_all_actors and movie not in movies_with_actors:
                movies_with_actors.append(movie)

        return movies_with_actors

    def get_movies_by_genres(self, genre_list: List[Genre]) -> List[Movie]:
        # Only include Genres which are in this repository
        existing_genres = [genre for genre in genre_list if genre in self.__genres]

        # Fetch the Movies which have all of the existing genres in the given list
        movies_with_genres = []

        if len(existing_genres) == 0:
            return movies_with_genres

        for movie in self.__movies:
            has_all_genres = True

            for genre in existing_genres:
                if genre not in movie.genres:
                    has_all_genres = False
                    break

            if has_all_genres and movie not in movies_with_genres:
                movies_with_genres.append(movie)

        return movies_with_genres

    def add_review(self, review: Review):
        super().add_review(review)
        if review.movie not in self.__movies:
            raise RepositoryException(f'Movie {review.movie} for Review is not in the repository')
        if review.id not in self.__reviews.keys() and review not in self.__reviews.values():
            self.__reviews[review.id] = review

    def get_review(self, review_id: int) -> Review:
        review = None

        if review_id in self.__reviews.keys():
            review = self.__reviews[review_id]

        return review

    def get_reviews_for_movie(self, movie: Movie) -> List[Review]:
        return [review for review in self.__reviews.values() if review.movie == movie and movie in self.__movies]

    def add_user(self, user: User):
        super().add_user(user)
        if user not in self.__users:
            self.__users.append(user)

    def get_user(self, user_name: str) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

    def get_user_by_id(self, user_id: int) -> User:
        return next((user for user in self.__users if user.id == user_id), None)

    def get_users_watched_movie(self, movie: Movie) -> List[User]:
        return [user for user in self.__users if movie in user.watched_movies and movie in self.__movies]

    def add_watchlist(self, watchlist: WatchList):
        super().add_watchlist(watchlist)
        for movie in watchlist:
            if movie not in self.__movies:
                raise RepositoryException(f'Movie {movie} in Watchlist is not in the repository')

        if watchlist not in self.__watch_lists:
            self.__watch_lists.append(watchlist)

    def get_watchlist_by_user_id(self, user_id: int) -> WatchList:
        return next((watchlist for watchlist in self.__watch_lists if watchlist.user.id == user_id), None)

    def set_movie_file_csv_reader(self, movie_file_reader: MovieFileCSVReader):
        super().set_movie_file_csv_reader(movie_file_reader)
        if self.__movie_file_csv_reader is None:
            self.__movie_file_csv_reader = movie_file_reader

    def get_movie_file_csv_reader(self) -> MovieFileCSVReader:
        return self.__movie_file_csv_reader

    def set_user_file_csv_reader(self, user_file_reader: UserFileCSVReader):
        super().set_user_file_csv_reader(user_file_reader)
        if self.__user_file_csv_reader is None:
            self.__user_file_csv_reader = user_file_reader

    def get_user_file_csv_reader(self) -> UserFileCSVReader:
        return self.__user_file_csv_reader

    def set_review_file_csv_reader(self, review_file_reader: ReviewFileCSVReader):
        super().set_review_file_csv_reader(review_file_reader)
        if self.__review_file_csv_reader is None:
            self.__review_file_csv_reader = review_file_reader

    def get_review_file_csv_reader(self) -> ReviewFileCSVReader:
        return self.__review_file_csv_reader

    def set_watchlist_file_csv_reader(self, watchlist_file_reader: WatchListFileCSVReader):
        super().set_watchlist_file_csv_reader(watchlist_file_reader)
        if self.__watchlist_file_csv_reader is None:
            self.__watchlist_file_csv_reader = watchlist_file_reader

    def get_watchlist_file_csv_reader(self) -> WatchListFileCSVReader:
        return self.__watchlist_file_csv_reader

    def set_watching_sim_file_csv_reader(self, watching_sim_file_reader: WatchingSimFileCSVReader):
        super().set_watching_sim_file_csv_reader(watching_sim_file_reader)
        if self.__watching_sim_file_csv_reader is None:
            self.__watching_sim_file_csv_reader = watching_sim_file_reader

    def get_watching_sim_file_csv_reader(self) -> WatchingSimFileCSVReader:
        return self.__watching_sim_file_csv_reader

    def add_watching_sim(self, watching_sim: MovieWatchingSimulation):
        super().add_watching_sim(watching_sim)
        if watching_sim.movie not in self.__movies:
            raise RepositoryException(f'Movie {watching_sim.movie} for watching simulation is not in the repository')

        for user in watching_sim.users:
            if user not in self.__users:
                raise RepositoryException(f'User {user} for watching simulation is not in the repository')

        for review in watching_sim.reviews:
            if review not in self.__reviews.values():
                raise RepositoryException(f'Review {review} for watching simulation is not in the repository')

        if watching_sim.id not in self.__watching_sims.keys() and watching_sim not in self.__watching_sims.values():
            self.__watching_sims[watching_sim.id] = watching_sim

    def get_watching_sim(self, watching_sim_id: int) -> MovieWatchingSimulation:
        watching_sim = None

        if watching_sim_id in self.__watching_sims.keys():
            watching_sim = self.__watching_sims[watching_sim_id]

        return watching_sim

    def get_watching_sims_for_movie(self, movie: Movie) -> List[MovieWatchingSimulation]:
        return [watching_sim for watching_sim in self.__watching_sims.values() if watching_sim.movie == movie and
                movie in self.__movies]

    def get_watching_sims_by_users(self, user_list: List[User]) -> List[MovieWatchingSimulation]:
        # Only include Users which are in this repository
        existing_users = [user for user in user_list if user in self.__users]

        # Fetch the Watching Simulations which have all of the existing users in the given list
        watching_sims_with_users = []

        if len(existing_users) == 0:
            return watching_sims_with_users

        for watching_sim in self.__watching_sims.values():
            has_all_users = True

            for user in existing_users:
                if user not in watching_sim.users:
                    has_all_users = False
                    break

            if has_all_users and watching_sim not in watching_sims_with_users:
                watching_sims_with_users.append(watching_sim)

        return watching_sims_with_users

    def get_watching_sims_with_no_users(self) -> List[MovieWatchingSimulation]:
        return [watching_sim for watching_sim in self.__watching_sims.values() if len(list(watching_sim.users)) == 0]

    def load_movie_dataset(self):
        if self.__movie_file_csv_reader is not None:
            self.__movie_file_csv_reader.read_csv_file()

            for movie in self.__movie_file_csv_reader.dataset_of_movies:
                self.add_movie(movie)

            for actor in self.__movie_file_csv_reader.dataset_of_actors:
                self.add_actor(actor)

            for director in self.__movie_file_csv_reader.dataset_of_directors:
                self.add_director(director)

            for genre in self.__movie_file_csv_reader.dataset_of_genres:
                self.add_genre(genre)

    def load_users(self):
        if self.__user_file_csv_reader is not None:
            self.__user_file_csv_reader.read_csv_file()

            for user in self.__user_file_csv_reader.dataset_of_users:
                self.add_user(user)

    def load_reviews(self):
        if self.__review_file_csv_reader is not None:
            self.__review_file_csv_reader.read_csv_file()

            for review in self.__review_file_csv_reader.dataset_of_reviews:
                self.add_review(review)

    def load_watch_lists(self):
        if self.__watchlist_file_csv_reader is not None:
            self.__watchlist_file_csv_reader.read_csv_file()

            for watchlist in self.__watchlist_file_csv_reader.dataset_of_watch_lists:
                self.add_watchlist(watchlist)

    def load_activity_simulations(self):
        if self.__watching_sim_file_csv_reader is not None:
            self.__watching_sim_file_csv_reader.read_csv_file()

            for watching_sim in self.__watching_sim_file_csv_reader.dataset_of_watching_sims:
                self.add_watching_sim(watching_sim)

    def populate(self, data_path_dict):
        super().populate(data_path_dict)

        self.set_movie_file_csv_reader(MovieFileCSVReader(data_path_dict["movies"]))
        self.load_movie_dataset()

        self.set_user_file_csv_reader(UserFileCSVReader(data_path_dict["users"], self.__movies))
        self.load_users()

        self.set_review_file_csv_reader(ReviewFileCSVReader(data_path_dict["reviews"], self.__movies, self.__users))
        self.load_reviews()

        self.set_watchlist_file_csv_reader(
            WatchListFileCSVReader(data_path_dict["watch_lists"], self.__movies, self.__users))
        self.load_watch_lists()

        self.set_watching_sim_file_csv_reader(
            WatchingSimFileCSVReader(data_path_dict["watching_sims"], self.__movies, self.__users, self.__reviews))
        self.load_activity_simulations()
