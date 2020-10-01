"""Initialise Flask app."""
import os
from flask import Flask


def create_app(test_config=None):
    """Construct the core application"""

    # Create the Flask app object
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = os.path.join('adapters/datafiles')

    return app
