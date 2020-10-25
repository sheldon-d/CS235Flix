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
        title=f"Reviews for user {user.user_name}",
        reviews=reviews,
        edit_review_urls=edit_review_urls
    )


@user_activity_blueprint.route('/browse_watchlist', methods=['GET'])
@login_required
def browse_watchlist():
    pass


@user_activity_blueprint.route('/recommended', methods=['GET'])
@login_required
def get_recommended_movies():
    pass
