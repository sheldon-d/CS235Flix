from movie_app.domainmodel.actor import Actor
from movie_app.domainmodel.director import Director
from movie_app.domainmodel.genre import Genre
from movie_app.domainmodel.movie import Movie

import pytest


@pytest.fixture()
def movie_from_file(movie_file_reader):
    movie_file_reader.read_csv_file()
    return movie_file_reader.dataset_of_movies[0]


@pytest.fixture()
def actor_from_file(movie_file_reader):
    movie_file_reader.read_csv_file()
    return movie_file_reader.dataset_of_actors[0]


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


def test_movie_actor_colleagues(actor_from_file, movie_from_file):
    actor1 = Actor("Bradley Cooper")
    actor2 = Actor("Christian Bale")

    assert actor_from_file in movie_from_file.actors
    assert actor1 in movie_from_file.actors

    assert movie_from_file.actors[0].check_if_this_actor_worked_with(actor_from_file) is False
    assert movie_from_file.actors[0].check_if_this_actor_worked_with(actor1) is True
    assert movie_from_file.actors[0].check_if_this_actor_worked_with(actor2) is False
    assert movie_from_file.actors[1].check_if_this_actor_worked_with(actor_from_file) is True
    assert movie_from_file.actors[1].check_if_this_actor_worked_with(actor1) is True

    # print([actor for actor in actor_from_file.colleagues])
