from os import environ
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


class Config:
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    SECRET_KEY = environ.get('SECRET_KEY')


class DataPaths:
    APP_BASE_PATH = Path.cwd().joinpath('movie_app')
    PROD_DATA_BASE_PATH = APP_BASE_PATH.joinpath('adapters', 'datafiles')
    TEST_DATA_BASE_PATH = Path.cwd().joinpath('tests', 'data')

    PROD_DATA_PATHS = {
        "movies": str(PROD_DATA_BASE_PATH.joinpath('Data1000Movies.csv')),
        "users": str(PROD_DATA_BASE_PATH.joinpath('users.csv')),
        "reviews": str(PROD_DATA_BASE_PATH.joinpath('reviews.csv')),
        "watch_lists": str(PROD_DATA_BASE_PATH.joinpath('watch_lists.csv')),
        "watching_sims": str(PROD_DATA_BASE_PATH.joinpath('watching_sims.csv'))
    }

    TEST_DATA_PATHS = {
        "movies": str(TEST_DATA_BASE_PATH.joinpath('movies.csv')),
        "users": str(TEST_DATA_BASE_PATH.joinpath('users.csv')),
        "reviews": str(TEST_DATA_BASE_PATH.joinpath('reviews.csv')),
        "watch_lists": str(TEST_DATA_BASE_PATH.joinpath('watch_lists.csv')),
        "watching_sims": str(TEST_DATA_BASE_PATH.joinpath('watching_sims.csv'))
    }
