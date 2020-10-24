from typing import List
import random

from movie_app.adapters.repository import AbstractRepository
from movie_app.domainmodel import Movie, Actor, Director, Genre


class ServicesException(Exception):
    def __init__(self, message=None):
        pass


def get_director(director_full_name: str, repo: AbstractRepository) -> Director:
    director = repo.get_director(director_full_name)
    if director is None:
        raise ServicesException('Director does not exist in the repository')
    return director


def get_actor(actor_full_name: str, repo: AbstractRepository) -> Actor:
    actor = repo.get_actor(actor_full_name)
    if actor is None:
        raise ServicesException('Actor does not exist in the repository')
    return actor


def get_movies_by_rank(rank_list: List[int], repo: AbstractRepository) -> List[Movie]:
    movies = repo.get_movies_by_rank(rank_list)
    return movies


def get_movie_ranks_by_release_year(release_year: int, repo: AbstractRepository) -> List[int]:
    movie_ranks = repo.get_movie_ranks_by_release_year(release_year)
    return movie_ranks


def get_movie_ranks_by_director(director: Director, repo: AbstractRepository) -> List[int]:
    movie_ranks = repo.get_movie_ranks_by_director(director)
    return movie_ranks


def get_movie_ranks_by_actors(actor_list: List[Actor], repo: AbstractRepository) -> List[int]:
    movie_ranks = repo.get_movie_ranks_by_actors(actor_list)
    return movie_ranks


def get_movie_ranks_by_genres(genre_list: List[Genre], repo: AbstractRepository) -> List[int]:
    movie_ranks = repo.get_movie_ranks_by_genres(genre_list)
    return movie_ranks


def get_most_common_director_names(quantity: int, repo: AbstractRepository) -> List[str]:
    directors = repo.get_most_common_directors(quantity)
    director_names = [director.director_full_name for director in directors]

    return director_names


def get_most_common_actor_names(quantity: int, repo: AbstractRepository) -> List[str]:
    actors = repo.get_most_common_actors(quantity)
    actor_names = [actor.actor_full_name for actor in actors]

    return actor_names


def get_most_common_genre_names(quantity: int, repo: AbstractRepository) -> List[str]:
    genres = repo.get_most_common_genres(quantity)
    genre_names = [genre.genre_name for genre in genres]

    return genre_names


def get_random_movies(quantity: int, repo: AbstractRepository) -> List[Movie]:
    movie_count = repo.get_number_of_movies()

    if quantity >= movie_count:
        # Reduce the quantity of movies to generate if the repository has an insufficient number of movies
        quantity = movie_count - 1

    # Pick distinct and random movies
    random_movie_ranks = random.sample(range(1, movie_count), quantity)
    movies = repo.get_movies_by_rank(random_movie_ranks)

    return movies
