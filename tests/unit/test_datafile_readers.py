from datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from domainmodel.actor import Actor
from domainmodel.director import Director
from domainmodel.genre import Genre
from domainmodel.movie import Movie
from pathlib import Path

import pytest


@pytest.fixture()
def movie_file_reader():
    path = str(Path.cwd().joinpath('datafiles', 'Data1000Movies.csv'))
    return MovieFileCSVReader(path)


@pytest.fixture()
def movie_from_file(movie_file_reader):
    movie_file_reader.read_csv_file()
    return movie_file_reader.dataset_of_movies[0]


def test_movie_file_reader_constructor(movie_file_reader):
    movie_file_reader.read_csv_file()
    assert len(movie_file_reader.dataset_of_movies) == 1000
    assert len(movie_file_reader.dataset_of_actors) == 1985
    assert len(movie_file_reader.dataset_of_directors) == 644
    assert len(movie_file_reader.dataset_of_genres) == 20


def test_movie_file_reader_movies(movie_from_file):
    movie = Movie("Guardians of the Galaxy", 2014)
    director = Director("James Gunn")
    actor = Actor("Chris Pratt")
    genre = Genre("Action")

    assert repr(movie_from_file) == repr(movie)
    assert repr(movie_from_file.director) == repr(director)
    assert actor in movie_from_file.actors
    assert genre in movie_from_file.genres
    assert movie_from_file.runtime_minutes == 121


def test_movie_file_reader_sort_directors(movie_file_reader):
    movie_file_reader.read_csv_file()
    all_directors_sorted = sorted(movie_file_reader.dataset_of_directors)
    assert all_directors_sorted[0:3] == [Director("Aamir Khan"), Director("Abdellatif Kechiche"), Director("Adam Leon")]
