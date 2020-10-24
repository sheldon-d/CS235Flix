from flask import Blueprint, url_for

import movie_app.adapters.repository as repo
import movie_app.services.services as services
from movie_app.domainmodel import Movie

# Configure Blueprint
utilities_blueprint = Blueprint('utilities_bp', __name__)


def get_most_common_directors_and_urls(quantity=10):
    director_names = services.get_most_common_director_names(quantity, repo.repo_instance)

    director_urls = dict()
    for director_full_name in director_names:
        director_urls[director_full_name] = url_for('movie_bp.movies_by_director', director=director_full_name)

    return director_urls


def get_most_common_actors_and_urls(quantity=10):
    actor_names = services.get_most_common_actor_names(quantity, repo.repo_instance)

    actor_urls = dict()
    for actor_full_name in actor_names:
        actor_urls[actor_full_name] = url_for('movie_bp.movies_by_actors', actors=actor_full_name)

    return actor_urls


def get_most_common_genres_and_urls(quantity=10):
    genre_names = services.get_most_common_genre_names(quantity, repo.repo_instance)

    genre_urls = dict()
    for genre_name in genre_names:
        genre_urls[genre_name] = url_for('movie_bp.movies_by_genres', genres=genre_name)

    return genre_urls


def get_actor_urls_for_movie(movie: Movie):
    actor_urls = dict()
    for actor in movie.actors:
        actor_urls[actor.actor_full_name] = url_for('movie_bp.movies_by_actors', actors=actor.actor_full_name)

    return actor_urls


def get_genre_urls_for_movie(movie: Movie):
    genre_urls = dict()
    for genre in movie.genres:
        genre_urls[genre.genre_name] = url_for('movie_bp.movies_by_genres', genres=genre.genre_name)
        
    return genre_urls


def get_random_movies(quantity=3):
    movies = services.get_random_movies(quantity, repo.repo_instance)
    return movies
