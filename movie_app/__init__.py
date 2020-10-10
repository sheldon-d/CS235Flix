"""Initialise Flask app."""
from flask import Flask
from config import DataPaths


def create_app(test_config=None):
    """Construct the core application"""

    # Create the Flask app object
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = DataPaths.PROD_DATA_BASE_PATH

    return app
