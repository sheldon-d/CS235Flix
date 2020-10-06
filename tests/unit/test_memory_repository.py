from movie_app.adapters.repository import RepositoryException
from movie_app.domainmodel import Actor, Director, Genre, Movie, Review, User, WatchList
from movie_app.datafilereaders import MovieFileCSVReader
from movie_app.activitysimulations import MovieWatchingSimulation

import pytest


def test_repository_can_add_actor(in_memory_repo):
    actor = Actor("Bob Jones")
    in_memory_repo.add_actor(actor)

    assert in_memory_repo.get_actor(actor.actor_full_name) is actor


def test_repository_cannot_add_invalid_actor(in_memory_repo):
    with pytest.raises(RepositoryException):
        in_memory_repo.add_actor(0)
    with pytest.raises(RepositoryException):
        in_memory_repo.add_actor(Actor(''))


def test_repository_can_get_actor(in_memory_repo):
    actor = in_memory_repo.get_actor('Chris Pratt')
    assert actor == Actor('Chris Pratt')
    assert actor.check_if_this_actor_worked_with(Actor('Vin Diesel')) is True
    assert actor.check_if_this_actor_worked_with(Actor('Jennifer Lawrence')) is True


def test_repository_cannot_get_nonexistent_actor(in_memory_repo):
    actor = in_memory_repo.get_actor('Sam')
    assert actor is None


def test_repository_can_get_actors_with_colleagues(in_memory_repo):
    colleague_names = 'Vin Diesel, Bradley Cooper, Zoe Saldana, Jennifer Lawrence'
    colleagues = [Actor(name) for name in colleague_names.split(',')]

    actor_with_colleagues = in_memory_repo.get_actors_by_colleagues(colleagues)
    assert Actor('Chris Pratt') in actor_with_colleagues
    assert len(actor_with_colleagues) == 1

    colleague_names = 'Margot Robbie, Viola Davis, Sam Smith'
    colleagues = [Actor(name) for name in colleague_names.split(',')]

    actor_with_colleagues = in_memory_repo.get_actors_by_colleagues(colleagues)
    assert Actor('Will Smith') in actor_with_colleagues
    assert Actor('Jared Leto') in actor_with_colleagues
    assert len(actor_with_colleagues) == 2


def test_repository_cannot_get_actors_with_no_colleagues(in_memory_repo):
    colleagues = [0, Director('Bob'), 'hello']
    actor_with_colleagues = in_memory_repo.get_actors_by_colleagues(colleagues)
    assert len(actor_with_colleagues) == 0


def test_repository_can_add_director(in_memory_repo):
    director = Director("Taika Waititi")
    in_memory_repo.add_director(director)

    assert in_memory_repo.get_director(director.director_full_name) is director


def test_repository_cannot_add_invalid_director(in_memory_repo):
    with pytest.raises(RepositoryException):
        in_memory_repo.add_director(0)
    with pytest.raises(RepositoryException):
        in_memory_repo.add_director(Director(''))


def test_repository_can_get_director(in_memory_repo):
    director = in_memory_repo.get_director('James Gunn')
    assert director == Director('James Gunn')


def test_repository_cannot_get_nonexistent_director(in_memory_repo):
    director = in_memory_repo.get_director('John Doe')
    assert director is None


def test_repository_can_add_genre(in_memory_repo):
    genre = Genre("Historical Drama")
    in_memory_repo.add_genre(genre)

    assert genre in in_memory_repo.get_genres()


def test_repository_cannot_add_invalid_genre(in_memory_repo):
    with pytest.raises(RepositoryException):
        in_memory_repo.add_genre(0)
    with pytest.raises(RepositoryException):
        in_memory_repo.add_genre(Genre(''))


def test_repository_can_get_genres(in_memory_repo):
    genres = in_memory_repo.get_genres()
    assert len(genres) == 14


def test_repository_can_add_movie(in_memory_repo):
    movie = Movie("Moana", 2016)
    in_memory_repo.add_movie(movie)

    assert in_memory_repo.get_movie(movie.title, movie.release_year) is movie


def test_repository_cannot_add_invalid_movie(in_memory_repo):
    with pytest.raises(RepositoryException):
        in_memory_repo.add_movie(Movie('', 2009))
    with pytest.raises(RepositoryException):
        in_memory_repo.add_movie(Movie(0, 2010))
    with pytest.raises(RepositoryException):
        in_memory_repo.add_movie(Movie('Bee Movie', 1899))


def test_repository_can_get_movie(in_memory_repo):
    movie = in_memory_repo.get_movie('Sing', 2016)
    assert movie == Movie('Sing', 2016)


def test_repository_cannot_get_nonexistent_movie(in_memory_repo):
    movie = in_memory_repo.get_movie('Sing', 2010)
    assert movie is None


def test_repository_can_get_movies_by_release_year(in_memory_repo):
    movies = in_memory_repo.get_movies_by_release_year(2016)
    assert Movie('Passengers', 2016) in movies
    assert Movie('La La Land', 2016) in movies
    assert len(movies) == 8

    movies = in_memory_repo.get_movies_by_release_year(2010)
    assert len(movies) == 0


def test_repository_can_get_movies_by_director(in_memory_repo):
    movies = in_memory_repo.get_movies_by_director(Director('James Gunn'))
    assert Movie('Guardians of the Galaxy', 2014) in movies
    assert Movie('Slither', 2006) in movies
    assert len(movies) == 2

    movies = in_memory_repo.get_movies_by_director(Director('John Doe'))
    assert len(movies) == 0


def test_repository_can_get_movies_with_actors(in_memory_repo):
    actor_names = 'Vin Diesel, Bradley Cooper, Zoe Saldana'
    actors = [Actor(name) for name in actor_names.split(',')]

    movies_with_actors = in_memory_repo.get_movies_by_actors(actors)
    assert Movie('Guardians of the Galaxy', 2014) in movies_with_actors
    assert len(movies_with_actors) == 1

    actors = [Actor('Chris Pratt')]

    movies_with_actors = in_memory_repo.get_movies_by_actors(actors)
    assert Movie('Guardians of the Galaxy', 2014) in movies_with_actors
    assert Movie('Passengers', 2016) in movies_with_actors
    assert len(movies_with_actors) == 2


def test_repository_cannot_get_movies_with_no_actors(in_memory_repo):
    actors = [0, Director('Bob'), 'hello']
    movies_with_actors = in_memory_repo.get_movies_by_actors(actors)
    assert len(movies_with_actors) == 0


def test_repository_can_get_movies_with_genres(in_memory_repo):
    genre_names = 'Action, Adventure, Fantasy'
    genres = [Genre(name) for name in genre_names.split(',')]

    movies_with_genres = in_memory_repo.get_movies_by_genres(genres)
    assert Movie('Suicide Squad', 2016) in movies_with_genres
    assert Movie('The Great Wall', 2016) in movies_with_genres
    assert len(movies_with_genres) == 2

    genres = [Genre('Horror')]

    movies_with_genres = in_memory_repo.get_movies_by_genres(genres)
    assert Movie('Split', 2016) in movies_with_genres
    assert Movie('Slither', 2006) in movies_with_genres
    assert len(movies_with_genres) == 2


def test_repository_cannot_get_movies_with_no_genres(in_memory_repo):
    genres = [0, Actor('Bob'), 'hello']
    movies_with_genres = in_memory_repo.get_movies_by_genres(genres)
    assert len(movies_with_genres) == 0


def test_repository_can_add_review(in_memory_repo):
    user = User("Martin", "pw12345")
    movie = Movie('Moana', 2016)
    review = Review(movie, "This movie was very enjoyable.", 8)
    user.add_review(review)

    in_memory_repo.add_review(review)
    assert in_memory_repo.get_review(review.id) is review


def test_repository_cannot_add_invalid_review(in_memory_repo):
    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(Review('', '', 0))

    user = User("Martin", "pw12345")
    movie = Movie('Moana', 2016)
    review = Review(movie, "This movie was very enjoyable.", 8)
    review1 = Review(review.movie, review.review_text, review.rating)

    assert review is not review1 and review.id is not review1.id

    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)

    movie.add_review(review)
    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)

    review.user = user
    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)

    user.add_review(review)
    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)

    user.add_review(review1)
    in_memory_repo.add_review(review1)
    assert in_memory_repo.get_review(review1.id) is review1


def test_repository_can_get_reviews(in_memory_repo):
    pass
