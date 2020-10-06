from movie_app.domainmodel import Actor, Director, Genre, Movie, User, Review, WatchList
import pytest


@pytest.fixture()
def movie_from_file(dataset_of_movies):
    return next((movie for movie in dataset_of_movies if movie.rank == 1), None)


@pytest.fixture()
def actor_from_file(dataset_of_actors):
    return [actor for actor in dataset_of_actors][0]


def test_movie_file_reader_constructor(movie_file_reader_prod):
    movie_file_reader_prod.read_csv_file()
    assert sum(1 for _ in movie_file_reader_prod.dataset_of_movies) == 1000
    assert sum(1 for _ in movie_file_reader_prod.dataset_of_actors) == 1985
    assert sum(1 for _ in movie_file_reader_prod.dataset_of_directors) == 644
    assert sum(1 for _ in movie_file_reader_prod.dataset_of_genres) == 20


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


def test_movie_file_reader_sort_directors(movie_file_reader_prod):
    movie_file_reader_prod.read_csv_file()
    all_directors_sorted = sorted(movie_file_reader_prod.dataset_of_directors)
    assert all_directors_sorted[0:3] == [Director("Aamir Khan"), Director("Abdellatif Kechiche"), Director("Adam Leon")]


def test_movie_actor_colleagues(actor_from_file, movie_from_file):
    actor1 = Actor("Bradley Cooper")
    actor2 = Actor("Christian Bale")

    assert actor_from_file in movie_from_file.actors
    assert actor1 in movie_from_file.actors

    actors = [actor for actor in movie_from_file.actors]
    assert actors[0].check_if_this_actor_worked_with(actor_from_file) is False
    assert actors[0].check_if_this_actor_worked_with(actor1) is True
    assert actors[0].check_if_this_actor_worked_with(actor2) is False
    assert actors[1].check_if_this_actor_worked_with(actor_from_file) is True
    assert actors[1].check_if_this_actor_worked_with(actor1) is True


def test_user_file_reader(user_file_reader):
    user_file_reader.read_csv_file()
    assert sum(1 for _ in user_file_reader.dataset_of_users) == 3
    assert User('Martin', 'pw12345') in user_file_reader.dataset_of_users
    assert User('Ian', 'pw67890') in user_file_reader.dataset_of_users
    assert User('Daniel', 'pw87465') in user_file_reader.dataset_of_users
    assert User('Bob', 'pw01234') not in user_file_reader.dataset_of_users

    for user in user_file_reader.dataset_of_users:
        assert user.user_name is not None and user.password is not None
        assert user.id is not None
        assert sum(1 for _ in user.watched_movies) == 0
        assert sum(1 for _ in user.reviews) == 0
        assert user.time_spent_watching_movies_minutes == 0
        assert sum(1 for _ in user.watchlist) == 0
        assert user.watchlist.user is user


def test_review_file_reader(review_file_reader):
    review_file_reader.read_csv_file()
    assert sum(1 for _ in review_file_reader.dataset_of_reviews) == 3
    reviews = [review for review in review_file_reader.dataset_of_reviews]

    assert reviews[0].user == User('Ian', 'pw67890')
    assert reviews[1].user == User('Martin', 'pw12345')
    assert reviews[2].user == User('Daniel', 'pw87465')

    assert reviews[0].movie == Movie('Suicide Squad', 2016)
    assert reviews[1].movie == Movie('Mindhorn', 2016)
    assert reviews[2].movie == Movie('Guardians of the Galaxy', 2014)

    assert "loved" in reviews[0].review_text and reviews[0].rating == 10
    assert "enjoyable" in reviews[1].review_text and reviews[1].rating == 7
    assert "entertaining" in reviews[2].review_text and reviews[2].rating == 8


def test_watchlist_file_reader(watchlist_file_reader):
    watchlist_file_reader.read_csv_file()
    assert sum(1 for _ in watchlist_file_reader.dataset_of_watch_lists) == 3
    watch_lists = [watchlist for watchlist in watchlist_file_reader.dataset_of_watch_lists]

    assert watch_lists[0].user == User('Daniel', 'pw87465')
    assert watch_lists[1].user == User('Martin', 'pw12345')
    assert watch_lists[2].user == User('Ian', 'pw67890')

    assert watch_lists[0].size() == 5
    assert watch_lists[1].size() == 6
    assert watch_lists[2].size() == 0

    assert watch_lists[0].first_movie_in_watchlist() == Movie('Suicide Squad', 2016)
    assert watch_lists[1].first_movie_in_watchlist() == Movie('Split', 2016)
    assert watch_lists[2].first_movie_in_watchlist() is None

    assert watch_lists[0].select_movie_to_watch(5) is None
    assert watch_lists[1].select_movie_to_watch(5) == Movie('Suicide Squad', 2016)
    assert watch_lists[2].select_movie_to_watch(0) is None
