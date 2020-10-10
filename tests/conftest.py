from movie_app.datafilereaders import MovieFileCSVReader, UserFileCSVReader, ReviewFileCSVReader, WatchListFileCSVReader
from movie_app.adapters.memory_repository import MemoryRepository
from config import DataPaths

import pytest

prod_data = DataPaths.PROD_DATA_PATHS
test_data = DataPaths.TEST_DATA_PATHS


@pytest.fixture()
def movie_file_reader_prod():
    return MovieFileCSVReader(prod_data["movies"])


@pytest.fixture()
def dataset_of_movies_prod(movie_file_reader_prod):
    movie_file_reader_prod.read_csv_file()
    return list(movie_file_reader_prod.dataset_of_movies)


@pytest.fixture()
def movie_file_reader():
    return MovieFileCSVReader(test_data["movies"])


@pytest.fixture()
def dataset_of_movies(movie_file_reader):
    movie_file_reader.read_csv_file()
    return list(movie_file_reader.dataset_of_movies)


@pytest.fixture()
def dataset_of_actors(movie_file_reader):
    movie_file_reader.read_csv_file()
    return list(movie_file_reader.dataset_of_actors)


@pytest.fixture()
def user_file_reader(dataset_of_movies):
    return UserFileCSVReader(test_data["users"], dataset_of_movies)


@pytest.fixture()
def dataset_of_users(user_file_reader):
    user_file_reader.read_csv_file()
    return list(user_file_reader.dataset_of_users)


@pytest.fixture()
def review_file_reader(dataset_of_movies, dataset_of_users):
    return ReviewFileCSVReader(test_data["reviews"], dataset_of_movies, dataset_of_users)


@pytest.fixture()
def watchlist_file_reader(dataset_of_movies, dataset_of_users):
    return WatchListFileCSVReader(test_data["watchlists"], dataset_of_movies, dataset_of_users)


@pytest.fixture()
def in_memory_repo():
    repo = MemoryRepository()
    repo.populate(test_data)
    return repo
