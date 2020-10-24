from flask import Blueprint, render_template
import movie_app.blueprints.utilities as utilities

# Configure Blueprint
home_blueprint = Blueprint('home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template(
        'home.html',
        random_movies=utilities.get_random_movies(),
        common_director_urls=utilities.get_most_common_directors_and_urls(),
        common_actor_urls=utilities.get_most_common_actors_and_urls(),
        common_genre_urls=utilities.get_most_common_genres_and_urls()
    )
