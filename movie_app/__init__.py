"""Initialise Flask app."""
from flask import Flask
from config import DataPaths

import movie_app.adapters.repository as repo
from movie_app.adapters.memory_repository import MemoryRepository


def create_app(test_config=None):
    """Construct the core application"""

    # Create the Flask app object
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path_dict = DataPaths.PROD_DATA_PATHS

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path_dict = app.config['TEST_DATA_PATHS']

    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = MemoryRepository()
    repo.repo_instance.populate(data_path_dict)

    # Build the application
    with app.app_context():
        # Register blueprints
        from .blueprints import home, movies, utilities
        app.register_blueprint(home.home_blueprint)
        app.register_blueprint(movies.movie_blueprint)
        app.register_blueprint(utilities.utilities_blueprint)

    return app
