from movie_app.datafilereaders import MovieFileCSVReader, UserFileCSVReader, ReviewFileCSVReader, \
    WatchListFileCSVReader, WatchingSimFileCSVReader
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
def dict_of_movies(movie_file_reader):
    movie_file_reader.read_csv_file()
    dataset_of_movies = {movie.rank: movie for movie in list(movie_file_reader.dataset_of_movies)}
    return dataset_of_movies


@pytest.fixture()
def dataset_of_actors(movie_file_reader):
    movie_file_reader.read_csv_file()
    return list(movie_file_reader.dataset_of_actors)


@pytest.fixture()
def user_file_reader(dict_of_movies):
    return UserFileCSVReader(test_data["users"], dict_of_movies)


@pytest.fixture()
def dataset_of_users(user_file_reader):
    user_file_reader.read_csv_file()
    return list(user_file_reader.dataset_of_users)


@pytest.fixture()
def review_file_reader(dict_of_movies, dataset_of_users):
    return ReviewFileCSVReader(test_data["reviews"], dict_of_movies, dataset_of_users)


@pytest.fixture()
def dataset_of_reviews(review_file_reader):
    review_file_reader.read_csv_file()
    dataset_of_reviews = {review.id: review for review in list(review_file_reader.dataset_of_reviews)}
    return dataset_of_reviews


@pytest.fixture()
def watchlist_file_reader(dict_of_movies, dataset_of_users):
    return WatchListFileCSVReader(test_data["watch_lists"], dict_of_movies, dataset_of_users)


@pytest.fixture()
def watching_sim_file_reader(dict_of_movies, dataset_of_users, dataset_of_reviews):
    return WatchingSimFileCSVReader(test_data["watching_sims"], dict_of_movies, dataset_of_users, dataset_of_reviews)


@pytest.fixture()
def in_memory_repo():
    repo = MemoryRepository()
    repo.populate(test_data)
    return repo
