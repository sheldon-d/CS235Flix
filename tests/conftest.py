from movie_app.datafilereaders import MovieFileCSVReader, UserFileCSVReader, ReviewFileCSVReader, WatchListFileCSVReader
from movie_app.adapters.memory_repository import MemoryRepository
from pathlib import Path

import pytest

# Using actual data
MOVIE_DATA_PATH = str(Path.cwd().joinpath('movie_app', 'adapters', 'datafiles', 'Data1000Movies.csv'))

# Using test data
TEST_MOVIE_DATA_PATH = str(Path.cwd().joinpath('tests', 'data', 'movies.csv'))
TEST_USER_DATA_PATH = str(Path.cwd().joinpath('tests', 'data', 'users.csv'))
TEST_REVIEW_DATA_PATH = str(Path.cwd().joinpath('tests', 'data', 'reviews.csv'))
TEST_WATCHLIST_DATA_PATH = str(Path.cwd().joinpath('tests', 'data', 'watchlists.csv'))


@pytest.fixture()
def movie_file_reader_prod():
    return MovieFileCSVReader(MOVIE_DATA_PATH)


@pytest.fixture()
def dataset_of_movies_prod(movie_file_reader_prod):
    movie_file_reader_prod.read_csv_file()
    return movie_file_reader_prod.dataset_of_movies


@pytest.fixture()
def movie_file_reader():
    return MovieFileCSVReader(TEST_MOVIE_DATA_PATH)


@pytest.fixture()
def dataset_of_movies(movie_file_reader):
    movie_file_reader.read_csv_file()
    return movie_file_reader.dataset_of_movies


@pytest.fixture()
def dataset_of_actors(movie_file_reader):
    movie_file_reader.read_csv_file()
    return movie_file_reader.dataset_of_actors


@pytest.fixture()
def user_file_reader():
    return UserFileCSVReader(TEST_USER_DATA_PATH)


@pytest.fixture()
def dataset_of_users(user_file_reader):
    user_file_reader.read_csv_file()
    return user_file_reader.dataset_of_users


@pytest.fixture()
def review_file_reader(dataset_of_movies, dataset_of_users):
    return ReviewFileCSVReader(TEST_REVIEW_DATA_PATH, dataset_of_movies, dataset_of_users)


@pytest.fixture()
def dataset_of_reviews(review_file_reader):
    review_file_reader.read_csv_file()
    return review_file_reader.dataset_of_reviews


@pytest.fixture()
def watchlist_file_reader(dataset_of_movies, dataset_of_users):
    return WatchListFileCSVReader(TEST_WATCHLIST_DATA_PATH, dataset_of_movies, dataset_of_users)


@pytest.fixture()
def dataset_of_watch_lists(watchlist_file_reader):
    watchlist_file_reader.read_csv_file()
    return watchlist_file_reader.dataset_of_watch_lists


@pytest.fixture()
def in_memory_repo():
    repo = MemoryRepository()
    repo.populate(TEST_MOVIE_DATA_PATH)
    return repo
