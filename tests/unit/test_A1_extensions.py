from movie_app.activitysimulations.watchingsimulation import MovieWatchingSimulation
from movie_app.domainmodel.movie import Movie
from movie_app.domainmodel.review import Review
from movie_app.domainmodel.user import User

import pytest


@pytest.fixture()
def movie():
    return Movie("Guardians of the Galaxy", 2014)


@pytest.fixture()
def movie_all_attributes(movie_file_reader):
    movie_file_reader.read_csv_file()
    return movie_file_reader.dataset_of_movies[0]


@pytest.fixture()
def movie_missing_attributes(movie_file_reader):
    movie_file_reader.read_csv_file()
    return movie_file_reader.dataset_of_movies[39]


@pytest.fixture()
def review(movie):
    review_text = "This movie was very enjoyable."
    rating = 8
    return Review(movie, review_text, rating)


@pytest.fixture()
def user():
    return User("Martin", "pw12345")


@pytest.fixture()
def watching_simulation(movie_all_attributes):
    return MovieWatchingSimulation(movie_all_attributes)


def test_movie_external_rating(movie):
    assert movie.external_rating is None
    movie.external_rating = ''
    assert movie.external_rating is None
    movie.external_rating = 0
    assert movie.external_rating == 0
    movie.external_rating = 10
    assert movie.external_rating == 10

    movie.external_rating = 4.856
    assert movie.external_rating == 4.9
    movie.external_rating = -0.5
    assert movie.external_rating == 4.9
    movie.external_rating = 10.1
    assert movie.external_rating == 4.9

    movie.external_rating = 0.04
    assert movie.external_rating == 0
    movie.external_rating = 9.96
    assert movie.external_rating == 10


def test_movie_rating_votes(movie):
    assert movie.rating_votes is None
    movie.rating_votes = ''
    assert movie.rating_votes is None
    movie.rating_votes = 0
    assert movie.rating_votes == 0
    movie.rating_votes = 1561575
    assert movie.rating_votes == 1561575

    movie.rating_votes = -1
    assert movie.rating_votes == 1561575
    movie.rating_votes = 220.3
    assert movie.rating_votes == 1561575


def test_movie_revenue_millions(movie):
    assert movie.revenue_millions is None
    movie.revenue_millions = ''
    assert movie.revenue_millions is None
    movie.revenue_millions = 0
    assert movie.revenue_millions == 0
    movie.revenue_millions = 10.25
    assert movie.revenue_millions == 10.25

    movie.revenue_millions = 1.2345
    assert movie.revenue_millions == 1.23
    movie.revenue_millions = -0.5
    assert movie.revenue_millions == 1.23
    movie.revenue_millions = 120
    assert movie.revenue_millions == 120

    movie.revenue_millions = 0.004
    assert movie.revenue_millions == 0
    movie.revenue_millions = 0.005
    assert movie.revenue_millions == 0.01
    movie.revenue_millions = 0.05
    assert movie.revenue_millions == 0.05
    movie.revenue_millions = 333.13
    assert movie.revenue_millions == 333.13


def test_movie_metascore(movie):
    assert movie.metascore is None
    movie.metascore = ''
    assert movie.metascore is None
    movie.metascore = 0
    assert movie.metascore == 0
    movie.metascore = 100
    assert movie.metascore == 100
    movie.metascore = 63
    assert movie.metascore == 63

    movie.metascore = -1
    assert movie.metascore == 63
    movie.metascore = 101
    assert movie.metascore == 63
    movie.metascore = 50.2
    assert movie.metascore == 63


def test_movie_file_reader_attributes(movie_all_attributes, movie_missing_attributes):
    assert movie_all_attributes.title == 'Guardians of the Galaxy'
    assert movie_all_attributes.release_year == 2014
    assert movie_all_attributes.runtime_minutes == 121
    assert movie_all_attributes.external_rating == 8.1
    assert movie_all_attributes.rating_votes == 757074
    assert movie_all_attributes.revenue_millions == 333.13
    assert movie_all_attributes.metascore == 76

    assert movie_missing_attributes.title == '5- 25- 77'
    assert movie_missing_attributes.release_year == 2007
    assert movie_missing_attributes.runtime_minutes == 113
    assert movie_missing_attributes.external_rating == 7.1
    assert movie_missing_attributes.rating_votes == 241
    assert movie_missing_attributes.revenue_millions is None
    assert movie_missing_attributes.metascore is None


def test_user_review_relationship(user, review):
    user.add_review(review)
    assert review in user.reviews
    assert review.user == user

    user2 = User('Ian', 'pw67890')
    user2.add_review(review)
    assert review not in user2.reviews
    assert review.user == user

    user3 = User('Daniel', 'pw87465')
    review.user = user3
    assert review.user == user


def test_movie_review_relationship(movie, review, user):
    movie.add_review(review)
    assert review not in movie.reviews
    user.add_review(review)
    assert review in user.reviews
    assert review in movie.reviews
    assert review.movie == movie
    movie.add_review(review)

    movie2 = Movie('Batman', 1989)
    movie2.add_review(review)
    assert review not in movie2.reviews
    assert review.movie == movie

    user.remove_review(review)
    assert review not in user.reviews
    assert review not in movie.reviews
    movie.remove_review(review)
    user2 = User('Ian', 'pw67890')
    user2.add_review(review)
    assert review not in user2.reviews
    assert review.user == user


def test_watching_simulation_constructor(movie_all_attributes, watching_simulation):
    assert watching_simulation.movie == movie_all_attributes
    assert sum(1 for _ in watching_simulation.users) == 0
    assert sum(1 for _ in watching_simulation.reviews) == 0


def test_watching_simulation_users(watching_simulation):
    users = [User('Martin', 'pw12345'), User('Ian', 'pw67890'), User('Daniel', 'pw87465')]

    for user in users:
        watching_simulation.add_user(user)
        assert user in watching_simulation.users

    user_invalid = User('  ', '123')
    watching_simulation.add_user(user_invalid)
    assert user_invalid not in watching_simulation.users

    assert sum(1 for _ in watching_simulation.users) == 3
    watching_simulation.add_user(users[0])
    assert sum(1 for _ in watching_simulation.users) == 3
    watching_simulation.remove_user(users[0])
    watching_simulation.remove_user(users[0])
    assert sum(1 for _ in watching_simulation.users) == 2


def test_watching_simulation_movies(watching_simulation):
    users = [User('Martin', 'pw12345'), User('Ian', 'pw67890'), User('Daniel', 'pw87465')]

    for user in users:
        watching_simulation.add_user(user)
        assert user in watching_simulation.users
        assert user.time_spent_watching_movies_minutes == 0

    watching_simulation.watch_movie()

    for user in watching_simulation.users:
        assert watching_simulation.movie in user.watched_movies
        assert user.time_spent_watching_movies_minutes == watching_simulation.movie.runtime_minutes
        assert sum(1 for _ in user.watched_movies) == 1

    user4 = User('Bob', 'pw12347')
    watching_simulation.add_user(user4)

    watching_simulation.watch_movie()

    for user in users:
        assert watching_simulation.movie in user.watched_movies
        assert user.time_spent_watching_movies_minutes == 2 * watching_simulation.movie.runtime_minutes
        assert sum(1 for _ in user.watched_movies) == 1

    assert watching_simulation.movie in user4.watched_movies
    assert user4.time_spent_watching_movies_minutes == watching_simulation.movie.runtime_minutes
    assert sum(1 for _ in user4.watched_movies) == 1


def test_watching_simulation_reviews(watching_simulation):
    users = [User('Martin', 'pw12345'), User('Ian', 'pw67890'), User('Daniel', 'pw87465')]

    for user in users:
        watching_simulation.add_user(user)

    watching_simulation.remove_user(users[1])
    watching_simulation.remove_user(users[1])
    user4 = User('Bob', 'pw12347')
    watching_simulation.add_user(user4)
    watching_simulation.add_user(user4)
    assert sum(1 for _ in watching_simulation.users) == 3

    watching_simulation.watch_movie()
    movie = watching_simulation.movie

    assert watching_simulation.movie in users[0].watched_movies
    assert watching_simulation.movie not in users[1].watched_movies
    assert watching_simulation.movie in users[2].watched_movies
    assert watching_simulation.movie in user4.watched_movies

    reviews = [Review(movie, "good", 8), Review(movie, "great", 10), Review(movie, "boring", 1)]

    for i in range(len(reviews)):
        user = users[i]
        review = reviews[i]
        watching_simulation.add_user_review(user, review)

    assert reviews[0] in watching_simulation.reviews and reviews[0] in users[0].reviews and reviews[0] in movie.reviews
    assert reviews[1] not in watching_simulation.reviews and reviews[1] not in users[1].reviews \
           and reviews[1] not in movie.reviews
    assert reviews[2] in watching_simulation.reviews and reviews[2] in users[2].reviews and reviews[2] in movie.reviews

    movie = Movie('Moana', 2016)
    review = Review(movie, 'Fun', 9)
    user4.add_review(review)
    watching_simulation.add_user_review(user4, review)

    assert review not in watching_simulation.reviews and review in user4.reviews

    review = Review(watching_simulation.movie, 'Fun', 9)
    watching_simulation.add_user_review(user4, review)

    assert review in watching_simulation.reviews and review in user4.reviews and \
           review in watching_simulation.movie.reviews
    watching_simulation.remove_user_review(review)
    assert review not in watching_simulation.reviews and review not in user4.reviews and \
        review not in watching_simulation.movie.reviews

    user5 = User('Tom', 'pw15567')
    user5.watch_movie(watching_simulation.movie)
    review = Review(watching_simulation.movie, 'Enjoyable', 8)
    watching_simulation.add_user_review(user5, review)

    assert review not in watching_simulation.reviews
