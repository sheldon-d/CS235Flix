from flask import Blueprint, render_template, redirect, request, url_for, session

import movie_app.adapters.repository as repo
import movie_app.blueprints.utilities as utilities
import movie_app.services.movie_services as movie_services
import movie_app.services.auth_services as auth_services
import movie_app.services.user_services as services
from movie_app.domainmodel import User, Review, WatchList

from movie_app.blueprints.authentication import login_required

# Configure Blueprint
user_activity_blueprint = Blueprint('user_activity_bp', __name__)


@user_activity_blueprint.route('/browse_reviews', methods=['GET'])
@login_required
def browse_reviews():
    # Get username
    user_to_show_reviews = session['username']

    user = auth_services.get_user(user_to_show_reviews, repo.repo_instance)
    reviews = [review for review in user.reviews]
    edit_review_urls = {review.id: url_for('movie_bp.create_movie_review', review=review.id,
                                           add_review_for=review.movie.rank) for review in reviews}

    # Generate the webpage to display the Reviews for the user.
    return render_template(
        'user_activity/reviews.html',
        title=f"Reviews for user {user_to_show_reviews}",
        reviews=reviews,
        edit_review_urls=edit_review_urls
    )


@user_activity_blueprint.route('/browse_watchlist', methods=['GET'])
@login_required
def browse_watchlist():
    # Get username
    user_of_watchlist = session['username']
    movie_rank = request.args.get('movie')

    user = None
    watchlist = []
    director_urls = dict()
    actor_urls = dict()
    genre_urls = dict()
    image_urls = dict()

    try:
        user = auth_services.get_user(user_of_watchlist, repo.repo_instance)
        try:
            if movie_rank is not None:
                movie_rank = int(movie_rank)
                movie = movie_services.get_movies_by_rank([movie_rank], repo.repo_instance)[0]
                user.watchlist.add_movie(movie)
        except movie_services.ServicesException:
            pass    # Ignore exception and don't modify watchlist
    except auth_services.UnknownUserException:
        pass    # Ignore exception and don't modify watchlist

    if user is not None:
        watchlist = user.watchlist

        for movie in watchlist:
            director_full_name = movie.director.director_full_name
            director_urls[director_full_name] = url_for('movie_bp.movies_by_director', director=director_full_name)
            actor_urls.update(utilities.get_actor_urls_for_movie(movie))
            genre_urls.update(utilities.get_genre_urls_for_movie(movie))
            image_urls[movie.rank] = utilities.get_image_url_for_movie(movie.title)

    # Generate the webpage to display the Watchlist for the user.
    return render_template(
        'user_activity/watchlist.html',
        title=f"Watchlist for user {user_of_watchlist}",
        director_urls=director_urls,
        actor_urls=actor_urls,
        genre_urls=genre_urls,
        image_urls=image_urls,
        watchlist=watchlist
    )


@user_activity_blueprint.route('/recommended', methods=['GET'])
@login_required
def get_recommended_movies():
    pass
