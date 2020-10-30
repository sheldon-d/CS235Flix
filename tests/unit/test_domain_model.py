from movie_app.domainmodel import Actor, Director, Genre, Movie, Review, User, WatchList

import pytest


@pytest.fixture()
def director():
    return Director("Taika Waititi")


@pytest.fixture()
def director_invalid():
    return Director(" ")


@pytest.fixture()
def genre():
    return Genre("Comedy")


@pytest.fixture()
def genre_invalid():
    return Genre(" ")


@pytest.fixture()
def actor():
    return Actor("Brad Pitt")


@pytest.fixture()
def actor_invalid():
    return Actor(" ")


@pytest.fixture()
def movie():
    return Movie("Moana", 2016)


@pytest.fixture()
def movie_invalid():
    return Movie(" ", 1899)


@pytest.fixture()
def review(movie):
    review_text = "This movie was very enjoyable."
    rating = 8
    return Review(movie, review_text, rating)


@pytest.fixture()
def review_invalid(movie_invalid):
    review_text = " "
    rating = 0
    return Review(movie_invalid, review_text, rating)


@pytest.fixture()
def user():
    return User("Martin", "pw12345")


@pytest.fixture()
def user_invalid():
    return User(" ", " ")


@pytest.fixture()
def watchlist():
    return WatchList()


def test_director_constructor(director, director_invalid):
    assert repr(director) == "<Director Taika Waititi>"
    assert repr(director_invalid) == "<Director None>"
    assert director_invalid.director_full_name is None
    director3 = Director(42)
    assert director3.director_full_name is None


def test_director_eq(director, director_invalid):
    directors = [Director(42), Director("Peter Jackson"), Director("Taika Waititi")]
    assert director_invalid == directors[0]
    assert director != directors[1]
    assert director == directors[2]


def test_director_lt(director, director_invalid):
    directors = [Director(42), Director("Peter Jackson"), Director("Taika Waititi")]
    assert directors[1] < directors[2]
    assert not director < directors[2]
    assert director_invalid < director
    assert not director_invalid < directors[0]


def test_director_hash(director, director_invalid):
    directors = [Director(42), Director("Peter Jackson"), Director("Taika Waititi")]
    assert hash(director) == hash(directors[2])
    assert hash(director) != hash(directors[1])
    assert hash(director_invalid) == hash(directors[0])


def test_genre_constructor(genre, genre_invalid):
    assert repr(genre) == "<Genre Comedy>"
    assert repr(genre_invalid) == "<Genre None>"
    assert genre_invalid.genre_name is None
    genre3 = Genre(0)
    assert genre3.genre_name is None


def test_genre_eq(genre, genre_invalid):
    genres = [Genre(0), Genre("Action"), Genre("Comedy")]
    assert genre_invalid == genres[0]
    assert genre != genres[1]
    assert genre == genres[2]


def test_genre_lt(genre, genre_invalid):
    genres = [Genre(0), Genre("Action"), Genre("Comedy")]
    assert genres[1] < genres[2]
    assert not genre < genres[2]
    assert genre_invalid < genre
    assert not genre_invalid < genres[0]


def test_genre_hash(genre, genre_invalid):
    genres = [Genre(0), Genre("Action"), Genre("Comedy")]
    assert hash(genre) == hash(genres[2])
    assert hash(genre) != hash(genres[1])
    assert hash(genre_invalid) == hash(genres[0])


def test_actor_constructor(actor, actor_invalid):
    assert repr(actor) == "<Actor Brad Pitt>"
    assert repr(actor_invalid) == "<Actor None>"
    assert actor_invalid.actor_full_name is None
    actor3 = Actor(42)
    assert actor3.actor_full_name is None


def test_actor_eq(actor, actor_invalid):
    actors = [Actor(42), Actor("Angelina Jolie"), Actor("Brad Pitt")]
    assert actor_invalid == actors[0]
    assert actor != actors[1]
    assert actor == actors[2]


def test_actor_lt(actor, actor_invalid):
    actors = [Actor(42), Actor("Angelina Jolie"), Actor("Brad Pitt")]
    assert actors[1] < actors[2]
    assert not actor < actors[2]
    assert actor_invalid < actor
    assert not actor_invalid < actors[0]


def test_actor_hash(actor, actor_invalid):
    actors = [Actor(42), Actor("Angelina Jolie"), Actor("Brad Pitt")]
    assert hash(actor) == hash(actors[2])
    assert hash(actor) != hash(actors[1])
    assert hash(actor_invalid) == hash(actors[0])


def test_actor_colleagues(director, actor, actor_invalid):
    actors = [actor, actor_invalid, Actor(42), Actor("Angelina Jolie"),
              Actor("Brad Pitt"), director]

    for actor_x in actors:
        actor.add_actor_colleague(actor_x)

    assert actor.check_if_this_actor_worked_with(actor) is False
    assert actor.check_if_this_actor_worked_with(actor_invalid) is False
    assert actor.check_if_this_actor_worked_with(actors[2]) is False
    assert actor.check_if_this_actor_worked_with(actors[3]) is True
    assert actor.check_if_this_actor_worked_with(actors[4]) is False
    assert actor.check_if_this_actor_worked_with(director) is False


def test_movie_constructor(movie, movie_invalid):
    assert repr(movie) == "<Movie Moana, 2016>"
    assert repr(movie_invalid) == "<Movie None, None>"
    assert movie_invalid.title is None
    assert movie_invalid.release_year is None
    movie3 = Movie(0, " ")
    assert movie3.title is None
    assert movie3.release_year is None


def test_movie_director(director, movie, director_invalid, movie_invalid):
    assert repr(movie.director) == '<Director None>'
    movie.director = director
    assert movie.director == director
    movie.director = director_invalid
    assert movie.director == director_invalid
    movie_invalid.director = director
    assert movie_invalid.director == director
    movie_invalid.director = director_invalid
    assert movie_invalid.director == director_invalid


def test_movie_add_actors(director, actor, movie, actor_invalid, movie_invalid):
    actors = [Actor("Auli'i Cravalho"), Actor("Dwayne Johnson"), Actor("Rachel House"), Actor("Temuera Morrison")]
    for actor_x in actors:
        movie.add_actor(actor_x)
    assert [actor for actor in movie.actors] == actors

    actors = [actor, actor_invalid, director, actor]
    for actor_x in actors:
        movie_invalid.add_actor(actor_x)

    assert actor_invalid not in movie_invalid.actors
    assert director not in movie_invalid.actors
    assert sum(1 for _ in movie_invalid.actors) == 1


def test_movie_remove_actors(director, actor, movie, actor_invalid):
    actors = [Actor("Auli'i Cravalho"), Actor("Dwayne Johnson"), Actor("Rachel House"), Actor("Temuera Morrison")]
    for actor_x in actors:
        movie.add_actor(actor_x)
    assert [actor for actor in movie.actors] == actors

    movie.remove_actor(actor)
    assert [actor for actor in movie.actors] == actors
    movie.remove_actor(actor_invalid)
    assert [actor for actor in movie.actors] == actors
    movie.remove_actor(actors[0])
    assert actors[0] not in movie.actors and [actor for actor in movie.actors] != actors
    movie.remove_actor(director)
    assert sum(1 for _ in movie.actors) == 3


def test_movie_add_genres(director, genre, movie, genre_invalid, movie_invalid):
    genres = [Genre("Action"), Genre("Romance"), Genre("Horror"), Genre("Mystery")]
    for genre_x in genres:
        movie.add_genre(genre_x)
    assert [genre for genre in movie.genres] == genres

    genres = [genre, genre_invalid, director, genre]
    for genre_x in genres:
        movie_invalid.add_genre(genre_x)

    assert genre_invalid not in movie_invalid.genres
    assert director not in movie_invalid.genres
    assert sum(1 for _ in movie_invalid.genres) == 1


def test_movie_remove_genres(director, genre, movie, genre_invalid):
    genres = [Genre("Action"), Genre("Romance"), Genre("Horror"), Genre("Mystery")]
    for genre_x in genres:
        movie.add_genre(genre_x)
    assert [genre for genre in movie.genres] == genres

    movie.remove_genre(genre)
    assert [genre for genre in movie.genres] == genres
    movie.remove_genre(genre_invalid)
    assert [genre for genre in movie.genres] == genres
    movie.remove_genre(genres[3])
    assert genres[3] not in movie.genres and [genre for genre in movie.genres] != genres
    movie.remove_genre(director)
    assert sum(1 for _ in movie.genres) == 3


def test_movie_runtime(movie, movie_invalid):
    assert movie.runtime_minutes is None
    movie.runtime_minutes = 120
    assert movie.runtime_minutes == 120
    movie.runtime_minutes = "abc"
    assert movie.runtime_minutes == 120

    movie_invalid.runtime_minutes = "abc"
    assert movie_invalid.runtime_minutes is None
    movie_invalid.runtime_minutes = list()
    assert movie_invalid.runtime_minutes is None

    with pytest.raises(ValueError):
        movie_invalid.runtime_minutes = 0
    with pytest.raises(ValueError):
        movie_invalid.runtime_minutes = -1
    assert movie_invalid.runtime_minutes is None


def test_movie_description(movie, movie_invalid):
    assert movie.description is None
    movie.description = "   A family movie              "
    assert movie.description == "A family movie"
    movie.description = ""
    assert movie.description == "A family movie"
    movie.description = 42
    assert movie.description == "A family movie"

    movie_invalid.description = 0
    assert movie_invalid.description is None
    movie_invalid.description = ""
    assert movie_invalid.description is None
    movie_invalid.description = "   "
    assert movie_invalid.description is None


def test_movie_eq(movie, movie_invalid):
    movies = [Movie("  ", 1899), Movie("Jaws", 2020), Movie("Moana", 2016), Movie("Moana", 1900)]
    assert movie != movies[1]
    assert movie == movies[2]
    assert movie != movies[3]
    assert movie_invalid == movies[0]


def test_movie_lt(movie, movie_invalid):
    movies = [Movie("  ", 1899), Movie("Jaws", 2020), Movie("Moana", 2016), Movie("Moana", 1900)]
    assert movies[1] < movies[2]
    assert not movie < movies[2]
    assert movie_invalid < movie
    assert not movie_invalid < movies[0]
    assert movies[3] < movies[2]


def test_movie_hash(movie, movie_invalid):
    movies = [Movie("  ", 1899), Movie("Jaws", 2020), Movie("Moana", 2016), Movie("Moana", 1900)]
    assert hash(movie) == hash(movies[2])
    assert hash(movie) != hash(movies[1])
    assert hash(movie_invalid) == hash(movies[0])
    assert hash(movie) != hash(movies[3])


def test_review_constructor(movie, review, movie_invalid, review_invalid):
    assert repr(review) == "<Review Moana, 8>"
    assert repr(review_invalid) == "<Review None, None>"
    assert review.movie == movie
    assert review_invalid.movie == movie_invalid
    assert review.rating == 8
    assert review_invalid.rating is None
    assert review.review_text == "This movie was very enjoyable."
    assert review_invalid.review_text is None

    review3 = Review(0, 0, 11)
    assert review3.movie is None
    assert review3.review_text is None
    assert review3.rating is None


def test_review_eq():
    movies = [Movie("Jaws", 1975), Movie("Moana", 2016), Movie("Moana", 2016)]
    review_texts = ["This movie was very exciting.", "This movie was very entertaining.", "      "]
    ratings = [10, 8, 5]
    reviews = [Review(movies[i], review_texts[i], ratings[i]) for i in range(len(movies))]

    assert reviews[0] != reviews[1]
    assert reviews[1] != reviews[2]


def test_user_constructor(user, user_invalid):
    assert repr(user) == "<User martin>"
    assert repr(user_invalid) == "<User None>"
    assert user_invalid.user_name is None
    user3 = User(0, 0)
    assert user3.user_name is None


def test_user_eq(user, user_invalid):
    users = [User(0, 0), User("Ian", "pw67890"), User("  MARTIN   ", "pw54321")]
    assert user_invalid == users[0]
    assert user != users[1]
    assert user == users[2]


def test_user_lt(user, user_invalid):
    users = [User(0, 0), User("Ian", "pw67890"), User("  MARTIN   ", "pw54321")]
    assert users[1] < users[2]
    assert not user < users[2]
    assert user_invalid < user
    assert not user_invalid < users[0]


def test_user_hash(user, user_invalid):
    users = [User(0, 0), User("Ian", "pw67890"), User("  MARTIN   ", "pw54321")]
    assert hash(user) == hash(users[2])
    assert hash(user) != hash(users[1])
    assert hash(user_invalid) == hash(users[0])


def test_user_watch_movie(movie, user, movie_invalid, user_invalid):
    movie3 = Movie("Moana", 1900)
    movie3.runtime_minutes = 140
    user.watch_movie(movie)
    user_invalid.watch_movie(movie_invalid)

    assert user.time_spent_watching_movies_minutes == 0
    assert movie not in user.watched_movies
    assert user_invalid.time_spent_watching_movies_minutes == 0
    assert movie_invalid not in user_invalid.watched_movies

    movie.runtime_minutes = 120
    movie_invalid.runtime_minutes = 100
    user.watch_movie(movie)
    user.watch_movie(movie)
    user.watch_movie(movie3)
    user_invalid.watch_movie(movie_invalid)
    user_invalid.watch_movie(movie3)
    user_invalid.watch_movie(movie3)

    assert user.time_spent_watching_movies_minutes == 380
    assert sum(1 for _ in user.watched_movies) == 2
    assert user_invalid.time_spent_watching_movies_minutes == 280
    assert sum(1 for _ in user_invalid.watched_movies) == 1


def test_user_add_review(review, user, review_invalid, user_invalid):
    movie1 = Movie("Jaws", 1975)
    review_text1 = "This movie was very exciting."
    rating1 = 10
    review1 = Review(movie1, review_text1, rating1)
    review2 = Review(movie1, 'Nice movie.', 11)
    review3 = Review(0, 'Boring movie.', 1)

    user.add_review(review)
    user.add_review(review1)
    user_invalid.add_review(review_invalid)
    user_invalid.add_review(review1)
    user_invalid.add_review(review2)
    user_invalid.add_review(review3)

    assert review in user.reviews
    assert review1 in user.reviews
    assert review_invalid not in user_invalid.reviews
    assert review1 not in user_invalid.reviews
    assert review2 not in user_invalid.reviews
    assert review3 not in user_invalid.reviews


def test_watchlist_constructor(watchlist):
    assert watchlist.size() == 0
    assert [movie for movie in watchlist] == []
    assert list(watchlist) == []
    assert watchlist.select_movie_to_watch(0) is None
    assert watchlist.select_movie_to_watch(-1.5) is None
    assert watchlist.first_movie_in_watchlist() is None


def test_watchlist_add_movie(watchlist, movie, movie_invalid):
    movies = [movie, movie_invalid, ("  ", 1899), Movie("Jaws", 2020),
              Movie("Moana", 2016), Movie("Moana", 1900)]

    for movie_x in movies:
        watchlist.add_movie(movie_x)

    assert watchlist.first_movie_in_watchlist() == movie
    assert watchlist.size() == 3
    assert movie in watchlist
    assert movie_invalid not in watchlist
    assert movies[2] not in watchlist
    assert movies[3] in watchlist
    assert movies[4] in watchlist
    assert movies[5] in watchlist

    assert next(watchlist) == movie
    assert next(watchlist) == movies[3]
    assert next(watchlist) == movies[5]

    with pytest.raises(StopIteration):
        next(watchlist)


def test_watchlist_remove_movie(watchlist, movie, movie_invalid):
    movies = [movie, movie_invalid, ("  ", 1899), Movie("Jaws", 2020),
              Movie("Moana", 2016), Movie("Moana", 1900)]

    for movie_x in movies:
        watchlist.add_movie(movie_x)

    assert watchlist.first_movie_in_watchlist() == movie
    assert watchlist.size() == 3
    watchlist.remove_movie(movie)
    assert watchlist.first_movie_in_watchlist() == movies[3]
    assert watchlist.size() == 2
    watchlist.remove_movie(movie_invalid)
    assert watchlist.size() == 2
    watchlist.remove_movie(movies[3])

    assert watchlist.first_movie_in_watchlist() == movies[5]
    assert watchlist.size() == 1
    watchlist.remove_movie(movies[5])
    assert watchlist.first_movie_in_watchlist() is None
    assert watchlist.size() == 0
    watchlist.remove_movie(movies[5])
    assert watchlist.size() == 0


def test_watchlist_select(watchlist, movie, movie_invalid):
    movies = [movie, movie_invalid, ("  ", 1899), Movie("Jaws", 2020),
              Movie("Moana", 2016), Movie("Moana", 1900)]

    for movie_x in movies:
        watchlist.add_movie(movie_x)

    assert watchlist.select_movie_to_watch(-1) is None
    assert watchlist.select_movie_to_watch(0) == movie
    assert watchlist.select_movie_to_watch(1) == movies[3]
    assert watchlist.select_movie_to_watch(2) == movies[5]
    assert watchlist.select_movie_to_watch(3) is None

    assert watchlist.select_movie_to_watch(0.5) is None
    assert watchlist.select_movie_to_watch('a') is None
