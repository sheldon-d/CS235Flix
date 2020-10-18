import random

from movie_app.adapters.repository import AbstractRepository
from movie_app.domainmodel import Movie


def get_random_movies(quantity: int, repo: AbstractRepository):
    movie_count = repo.get_number_of_movies()

    if quantity >= movie_count:
        # Reduce the quantity of movies to generate if the repository has an insufficient number of movies
        quantity = movie_count - 1

    # Pick distinct and random movies
    random_movie_ranks = random.sample(range(1, movie_count), quantity)
    movies = repo.get_movies_by_rank(random_movie_ranks)

    return movies


