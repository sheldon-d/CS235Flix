from flask import Blueprint, render_template, redirect, request, url_for, session

import movie_app.adapters.repository as repo
import movie_app.blueprints.utilities as utilities
import movie_app.services.services as services
from movie_app.domainmodel import Genre

# Configure Blueprint
movie_blueprint = Blueprint('movie_bp', __name__)


@movie_blueprint.route('/movies_by_director', methods=['GET'])
def movies_by_director():
    movies_per_page = 3

    # Read query parameters
    director_full_name = request.args.get('director')
    cursor = request.args.get('cursor')

    try:
        # Try converting cursor from string to int.
        cursor = int(cursor)
    except TypeError:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0

    # Retrieve Movie ranks for Movies with the given director.
    director = services.get_director(director_full_name, repo.repo_instance)
    movie_ranks = services.get_movie_ranks_by_director(director, repo.repo_instance)

    # Retrieve only a batch of Movies to display on the Web page
    movies = services.get_movies_by_rank(movie_ranks[cursor:cursor+movies_per_page], repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None
    director_urls = dict()
    actor_urls = dict()
    genre_urls = dict()

    director_urls[director_full_name] = url_for('movie_bp.movies_by_director', director=director_full_name)

    for movie in movies:
        actor_urls.update(utilities.get_actor_urls_for_movie(movie))
        genre_urls.update(utilities.get_genre_urls_for_movie(movie))

    if cursor > 0:
        # There are preceding Movies, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for(
            'movie_bp.movies_by_director', director=director_full_name, cursor=cursor - movies_per_page)
        first_movie_url = url_for('movie_bp.movies_by_director', director=director_full_name)

    if cursor + movies_per_page < len(movie_ranks):
        # There are further Movies, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for(
            'movie_bp.movies_by_director', director=director_full_name, cursor=cursor + movies_per_page)
        last_cursor = movies_per_page * int(len(movie_ranks) / movies_per_page)
        if len(movie_ranks) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movie_bp.movies_by_director', director=director_full_name, cursor=last_cursor)

    # Generate the webpage to display the Movies.
    return render_template(
        'movies/movies.html',
        title='Movies',
        movies_title='Movies directed by ' + director_full_name,
        movies=movies,
        random_movies=utilities.get_random_movies(len(movies) * 2),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        director_urls=director_urls,
        actor_urls=actor_urls,
        genre_urls=genre_urls
    )


@movie_blueprint.route('/movies_by_actors', methods=['GET'])
def movies_by_actors():
    movies_per_page = 3

    # Read query parameters
    actor_full_names_string = request.args.get('actors')
    actor_full_names = actor_full_names_string.split('/')
    cursor = request.args.get('cursor')

    try:
        # Try converting cursor from string to int.
        cursor = int(cursor)
    except TypeError:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0

    # Retrieve Movie ranks for Movies with the given actors.
    actors = [services.get_actor(name, repo.repo_instance) for name in actor_full_names]
    movie_ranks = services.get_movie_ranks_by_actors(actors, repo.repo_instance)

    # Retrieve only a batch of Movies to display on the Web page
    movies = services.get_movies_by_rank(movie_ranks[cursor:cursor + movies_per_page], repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None
    director_urls = dict()
    actor_urls = dict()
    genre_urls = dict()

    for movie in movies:
        director_full_name = movie.director.director_full_name
        director_urls[director_full_name] = url_for('movie_bp.movies_by_director', director=director_full_name)
        actor_urls.update(utilities.get_actor_urls_for_movie(movie))
        genre_urls.update(utilities.get_genre_urls_for_movie(movie))

    if cursor > 0:
        # There are preceding Movies, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for(
            'movie_bp.movies_by_actors', actors=actor_full_names_string, cursor=cursor - movies_per_page)
        first_movie_url = url_for('movie_bp.movies_by_actors', actors=actor_full_names_string)

    if cursor + movies_per_page < len(movie_ranks):
        # There are further Movies, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for(
            'movie_bp.movies_by_actors', actors=actor_full_names_string, cursor=cursor + movies_per_page)
        last_cursor = movies_per_page * int(len(movie_ranks) / movies_per_page)
        if len(movie_ranks) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movie_bp.movies_by_actors', actors=actor_full_names_string, cursor=last_cursor)

    # Generate the webpage to display the Movies.
    return render_template(
        'movies/movies.html',
        title='Movies',
        movies_title=f"Movies with actors: {', '.join(actor_full_names)}",
        movies=movies,
        random_movies=utilities.get_random_movies(len(movies) * 2),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        director_urls=director_urls,
        actor_urls=actor_urls,
        genre_urls=genre_urls
    )


@movie_blueprint.route('/movies_by_genres', methods=['GET'])
def movies_by_genres():
    movies_per_page = 3

    # Read query parameters
    genre_names_string = request.args.get('genres')
    genre_names = genre_names_string.split('/')
    cursor = request.args.get('cursor')

    try:
        # Try converting cursor from string to int.
        cursor = int(cursor)
    except TypeError:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0

    # Retrieve Movie ranks for Movies with the given genres.
    genres = [Genre(genre_name) for genre_name in genre_names]
    movie_ranks = services.get_movie_ranks_by_genres(genres, repo.repo_instance)

    # Retrieve only a batch of Movies to display on the Web page
    movies = services.get_movies_by_rank(movie_ranks[cursor:cursor + movies_per_page], repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None
    director_urls = dict()
    actor_urls = dict()
    genre_urls = dict()

    for movie in movies:
        director_full_name = movie.director.director_full_name
        director_urls[director_full_name] = url_for('movie_bp.movies_by_director', director=director_full_name)
        actor_urls.update(utilities.get_actor_urls_for_movie(movie))
        genre_urls.update(utilities.get_genre_urls_for_movie(movie))

    if cursor > 0:
        # There are preceding Movies, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for(
            'movie_bp.movies_by_genres', genres=genre_names_string, cursor=cursor - movies_per_page)
        first_movie_url = url_for('movie_bp.movies_by_genres', genres=genre_names_string)

    if cursor + movies_per_page < len(movie_ranks):
        # There are further Movies, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for(
            'movie_bp.movies_by_genres', genres=genre_names_string, cursor=cursor + movies_per_page)
        last_cursor = movies_per_page * int(len(movie_ranks) / movies_per_page)
        if len(movie_ranks) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movie_bp.movies_by_genres', genres=genre_names_string, cursor=last_cursor)

    # Generate the webpage to display the Movies.
    return render_template(
        'movies/movies.html',
        title='Movies',
        movies_title=f"Movies with genres: {', '.join(genre_names)}",
        movies=movies,
        random_movies=utilities.get_random_movies(len(movies) * 2),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        director_urls=director_urls,
        actor_urls=actor_urls,
        genre_urls=genre_urls
    )
