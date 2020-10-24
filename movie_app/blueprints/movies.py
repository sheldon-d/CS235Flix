from flask import Blueprint, render_template, redirect, request, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, IntegerField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange

import movie_app.adapters.repository as repo
import movie_app.blueprints.utilities as utilities
import movie_app.services.movie_services as services
from movie_app.domainmodel import Movie, Genre

from movie_app.blueprints.authentication import login_required

# Configure Blueprint
movie_blueprint = Blueprint('movie_bp', __name__)


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review_text = TextAreaField('Review text', [
        DataRequired(),
        Length(min=4, message='Your review text is too short'),
        ProfanityFree(message='Your review text must not contain profanity')])
    rating = IntegerField('Rating (1-10)', [
        DataRequired(),
        NumberRange(min=1, max=10, message='Rating must be between 1 and 10')])
    movie_rank = HiddenField("Movie rank")
    submit = SubmitField('Submit Review')


@movie_blueprint.route('/movies_by_director', methods=['GET'])
def movies_by_director():
    movies_per_page = 3

    # Read query parameters
    director_full_name = request.args.get('director')
    cursor = request.args.get('cursor')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    try:
        # Try converting movie_to_show_reviews from string to int.
        movie_to_show_reviews = int(movie_to_show_reviews)
    except TypeError:
        # No view_reviews_for query parameter, so set to a non-existent movie rank.
        movie_to_show_reviews = -1

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
    movies = services.get_movies_by_rank(movie_ranks[cursor:cursor + movies_per_page], repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    director_urls = dict()
    actor_urls = dict()
    genre_urls = dict()
    view_review_urls = dict()
    add_review_urls = dict()

    director_urls[director_full_name] = url_for('movie_bp.movies_by_director', director=director_full_name)

    for movie in movies:
        actor_urls.update(utilities.get_actor_urls_for_movie(movie))
        genre_urls.update(utilities.get_genre_urls_for_movie(movie))
        view_review_urls[movie.rank] = url_for('movie_bp.movies_by_director', director=director_full_name,
                                               cursor=cursor, view_reviews_for=movie.rank)
        add_review_urls[movie.rank] = url_for('movie_bp.create_movie_review', add_review_for=movie.rank)

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
        genre_urls=genre_urls,
        view_review_urls=view_review_urls,
        add_review_urls=add_review_urls,
        show_reviews_for_movie=movie_to_show_reviews
    )


@movie_blueprint.route('/movies_by_actors', methods=['GET'])
def movies_by_actors():
    movies_per_page = 3

    # Read query parameters
    actor_full_names_string = request.args.get('actors')
    actor_full_names = actor_full_names_string.split('/')
    cursor = request.args.get('cursor')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    try:
        # Try converting movie_to_show_reviews from string to int.
        movie_to_show_reviews = int(movie_to_show_reviews)
    except TypeError:
        # No view_reviews_for query parameter, so set to a non-existent movie rank.
        movie_to_show_reviews = -1

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
    view_review_urls = dict()
    add_review_urls = dict()

    for movie in movies:
        director_full_name = movie.director.director_full_name
        director_urls[director_full_name] = url_for('movie_bp.movies_by_director', director=director_full_name)
        actor_urls.update(utilities.get_actor_urls_for_movie(movie))
        genre_urls.update(utilities.get_genre_urls_for_movie(movie))
        view_review_urls[movie.rank] = url_for('movie_bp.movies_by_actors', actors=actor_full_names_string,
                                               cursor=cursor, view_reviews_for=movie.rank)
        add_review_urls[movie.rank] = url_for('movie_bp.create_movie_review', add_review_for=movie.rank)

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
        genre_urls=genre_urls,
        view_review_urls=view_review_urls,
        add_review_urls=add_review_urls,
        show_reviews_for_movie=movie_to_show_reviews
    )


@movie_blueprint.route('/movies_by_genres', methods=['GET'])
def movies_by_genres():
    movies_per_page = 3

    # Read query parameters
    genre_names_string = request.args.get('genres')
    genre_names = genre_names_string.split('/')
    cursor = request.args.get('cursor')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    try:
        # Try converting movie_to_show_reviews from string to int.
        movie_to_show_reviews = int(movie_to_show_reviews)
    except TypeError:
        # No view_reviews_for query parameter, so set to a non-existent movie rank.
        movie_to_show_reviews = -1

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
    view_review_urls = dict()
    add_review_urls = dict()

    for movie in movies:
        director_full_name = movie.director.director_full_name
        director_urls[director_full_name] = url_for('movie_bp.movies_by_director', director=director_full_name)
        actor_urls.update(utilities.get_actor_urls_for_movie(movie))
        genre_urls.update(utilities.get_genre_urls_for_movie(movie))
        view_review_urls[movie.rank] = url_for('movie_bp.movies_by_genres', genres=genre_names_string,
                                               cursor=cursor, view_reviews_for=movie.rank)
        add_review_urls[movie.rank] = url_for('movie_bp.create_movie_review', add_review_for=movie.rank)

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
        genre_urls=genre_urls,
        view_review_urls=view_review_urls,
        add_review_urls=add_review_urls,
        show_reviews_for_movie=movie_to_show_reviews
    )


@movie_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def create_movie_review():
    # Obtain the username of the currently logged in user.
    username = session['username']

    form = ReviewForm()

    if form.validate_on_submit():
        # Successful POST results if the review text and rating has passed data validation.
        # Extract the Movie rank, representing the reviewed Movie, from the form.
        movie_rank = int(form.movie_rank.data)

        # Using the service layer to create and store the new review.
        services.create_review(movie_rank, form.review_text.data, form.rating.data, username, repo.repo_instance)

        # Retrieve the Movie that was reviewed.
        movie: Movie = services.get_movies_by_rank([movie_rank], repo.repo_instance)[0]

        return redirect(url_for('movie_bp.movies_by_director', director=movie.director.director_full_name,
                                view_reviews_for=movie.rank))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the Movie rank, representing the Movie to review, from a query parameter of the GET request.
        movie_rank = int(request.args.get('add_review_for'))

        # Store the Movie rank in the form.
        form.movie_rank.data = movie_rank
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the Movie rank of the Movie being reviewed from the form.
        movie_rank = int(form.movie_rank.data)

    movie: Movie = services.get_movies_by_rank([movie_rank], repo.repo_instance)[0]
    return render_template(
        'movies/create_movie_review.html',
        title='Create review',
        movie=movie,
        form=form,
        handler_url=url_for('movie_bp.create_movie_review'),
        random_movies=utilities.get_random_movies(),
    )
