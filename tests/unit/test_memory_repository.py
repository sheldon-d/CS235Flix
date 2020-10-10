from movie_app.adapters.repository import RepositoryException
from movie_app.domainmodel import Actor, Director, Genre, Movie, Review, User, WatchList
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
        in_memory_repo.add_review(Director('Joe'))

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


def test_repository_can_get_review(in_memory_repo):
    review = in_memory_repo.get_review(1)
    assert review.user == User('Ian', 'pw67890')
    assert review.movie == Movie('Suicide Squad', 2016)
    assert "loved" in review.review_text
    assert review.rating == 10

    assert review in review.user.reviews and review in review.movie.reviews

    user = in_memory_repo.get_user(review.user.user_name)
    assert review in user.reviews

    movie = in_memory_repo.get_movie_by_rank(review.movie.rank)
    assert review in movie.reviews


def test_can_get_reviews_for_movie(in_memory_repo):
    movie = in_memory_repo.get_movie_by_rank(1)
    reviews_for_movie = in_memory_repo.get_reviews_for_movie(movie)

    assert len(reviews_for_movie) == 2
    assert in_memory_repo.get_review(3) in reviews_for_movie
    assert in_memory_repo.get_review(4) in reviews_for_movie
    assert in_memory_repo.get_review(1) not in reviews_for_movie


def test_repository_can_add_user(in_memory_repo):
    user = User('John', 'pwxyz123')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user(user.user_name) is user


def test_repository_cannot_add_invalid_user(in_memory_repo):
    with pytest.raises(RepositoryException):
        in_memory_repo.add_user(0)
    with pytest.raises(RepositoryException):
        in_memory_repo.add_user(Director('Joe'))


def test_repository_can_get_user(in_memory_repo):
    user = in_memory_repo.get_user('martin')
    assert user == User('Martin', 'pw12345')
    assert user.id == 1

    review1 = in_memory_repo.get_review(2)
    review2 = in_memory_repo.get_review(4)
    assert review1 in user.reviews and review2 in user.reviews
    assert user.watchlist.size() == 6
    assert in_memory_repo.get_movie_by_rank(7) in user.watchlist

    user = in_memory_repo.get_user('ian')
    assert user == User('Ian', 'pw67890')
    assert user.id == 2

    review = in_memory_repo.get_review(1)
    movie = in_memory_repo.get_movie_by_rank(review.movie.rank)
    assert review in user.reviews and review in movie.reviews
    assert user.watchlist.size() == 0


def test_repository_cannot_get_nonexistent_user(in_memory_repo):
    user = in_memory_repo.get_user('Sam')
    assert user is None


def test_repository_can_get_users_watched_movie(in_memory_repo):
    user = in_memory_repo.get_user('daniel')
    movie = in_memory_repo.get_movie_by_rank(7)
    users_watched_movie = in_memory_repo.get_users_watched_movie(movie)
    assert user in users_watched_movie

    user1 = in_memory_repo.get_user('martin')
    movie = in_memory_repo.get_movie_by_rank(3)
    users_watched_movie = in_memory_repo.get_users_watched_movie(movie)
    assert user in users_watched_movie and user1 in users_watched_movie
    assert user1.time_spent_watching_movies_minutes == \
           sum([in_memory_repo.get_movie_by_rank(x).runtime_minutes for x in [2, 6, 5, 3]])

    assert len(in_memory_repo.get_users_watched_movie(in_memory_repo.get_movie_by_rank(1))) == 0


def test_repository_can_add_watchlist(in_memory_repo):
    user = User('Matt', 'pw4567')
    user.watchlist.add_movie(Movie('Sing', 2016))
    in_memory_repo.add_watchlist(user.watchlist)

    assert in_memory_repo.get_watchlist_by_user_id(user.id) == user.watchlist
    assert in_memory_repo.get_watchlist_by_user_id(user.id).size() == 1


def test_repository_cannot_add_invalid_watchlist(in_memory_repo):
    watchlist = WatchList()
    watchlist.add_movie(Movie('Guardians of the Galaxy', 2014))

    with pytest.raises(RepositoryException):
        in_memory_repo.add_watchlist(watchlist)
    with pytest.raises(RepositoryException):
        in_memory_repo.add_watchlist(Director('Joe'))

    user = User('John', 'pw0135')
    user.watchlist.add_movie(Movie('A Movie', 2020))

    with pytest.raises(RepositoryException):
        in_memory_repo.add_watchlist(user.watchlist)

    user.watchlist.remove_movie(Movie('A Movie', 2020))
    in_memory_repo.add_watchlist(user.watchlist)


def test_repository_can_get_watchlist(in_memory_repo):
    watchlist = in_memory_repo.get_watchlist_by_user_id(3)

    assert watchlist.user == in_memory_repo.get_user('daniel')
    assert watchlist.size() == 5
    assert watchlist.first_movie_in_watchlist() == in_memory_repo.get_movie_by_rank(5)
    assert watchlist.select_movie_to_watch(4) == in_memory_repo.get_movie_by_rank(8)


def test_repository_cannot_get_nonexistent_watchlist(in_memory_repo):
    watchlist = in_memory_repo.get_watchlist_by_user_id(4)
    assert watchlist is None
