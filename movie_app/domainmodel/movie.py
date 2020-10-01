from typing import List, Iterable
from movie_app.domainmodel.genre import Genre
from movie_app.domainmodel.actor import Actor
from movie_app.domainmodel.director import Director
from movie_app.domainmodel.review import Review


class Movie:

    def __init__(self, title: str, release_year: int):
        if isinstance(title, str) and title.strip() != "":
            self.__title = title.strip()
        else:
            self.__title = None

        if isinstance(release_year, int) and release_year >= 1900:
            self.__release_year = release_year
        else:
            self.__release_year = None

        self.__description = None
        self.__director: Director = Director(str())
        self.__actors: List[Actor] = list()
        self.__genres: List[Genre] = list()
        self.__runtime_minutes = None
        self.__external_rating = None
        self.__rating_votes = None
        self.__revenue_millions = None
        self.__metascore = None
        self.__reviews: List[Review] = list()

    @property
    def title(self) -> str:
        return self.__title

    @property
    def release_year(self) -> int:
        return self.__release_year

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str):
        if isinstance(description, str) and description.strip() != "":
            self.__description = description.strip()

    @property
    def director(self) -> Director:
        return self.__director

    @director.setter
    def director(self, director: Director):
        if isinstance(director, Director):
            self.__director = director

    @property
    def actors(self) -> List[Actor]:
        return self.__actors

    @property
    def genres(self) -> List[Genre]:
        return self.__genres

    @property
    def runtime_minutes(self) -> int:
        return self.__runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, runtime_minutes: int):
        if isinstance(runtime_minutes, int):
            if runtime_minutes > 0:
                self.__runtime_minutes = runtime_minutes
            else:
                raise ValueError

    @property
    def external_rating(self) -> float:
        return self.__external_rating

    @external_rating.setter
    def external_rating(self, external_rating: float):
        if isinstance(external_rating, (float, int)) and 0 <= external_rating <= 10:
            self.__external_rating = round(external_rating, 1)

    @property
    def rating_votes(self) -> int:
        return self.__rating_votes

    @rating_votes.setter
    def rating_votes(self, rating_votes: int):
        if isinstance(rating_votes, int) and rating_votes >= 0:
            self.__rating_votes = rating_votes

    @property
    def revenue_millions(self) -> float:
        return self.__revenue_millions

    @revenue_millions.setter
    def revenue_millions(self, revenue_millions: float):
        if isinstance(revenue_millions, (float, int)) and revenue_millions >= 0:
            self.__revenue_millions = round(revenue_millions, 2)

    @property
    def metascore(self) -> int:
        return self.__metascore

    @metascore.setter
    def metascore(self, metascore: int):
        if isinstance(metascore, int) and 0 <= metascore <= 100:
            self.__metascore = metascore

    @property
    def reviews(self) -> Iterable[Review]:
        return iter(self.__reviews)

    def __repr__(self) -> str:
        return f"<Movie {self.__title}, {self.__release_year}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Movie):
            return False
        return self.__title == other.__title and self.__release_year == other.__release_year

    def __lt__(self, other) -> bool:
        if self.__title is None:
            return other.__title is not None
        elif other.__title is None:
            return False
        elif self.__title == other.__title:
            if self.__release_year is None:
                return other.__release_year is not None
            elif other.__release_year is None:
                return False
            return self.__release_year < other.__release_year
        return self.__title < other.__title

    def __hash__(self):
        return hash((self.__title, self.__release_year))

    def add_actor(self, actor: Actor):
        if isinstance(actor, Actor) and actor not in self.__actors and actor.actor_full_name is not None:
            self.__actors.append(actor)

    def remove_actor(self, actor: Actor):
        if actor in self.__actors:
            self.__actors.remove(actor)

    def add_genre(self, genre: Genre):
        if isinstance(genre, Genre) and genre not in self.__genres and genre.genre_name is not None:
            self.__genres.append(genre)

    def remove_genre(self, genre: Genre):
        if genre in self.__genres:
            self.__genres.remove(genre)

    def add_review(self, review: Review):
        if isinstance(review, Review) and review not in self.__reviews and \
                review.movie is self and review.rating is not None and review.user is not None:
            self.__reviews.append(review)

    def remove_review(self, review: Review):
        if review in self.__reviews:
            self.__reviews.remove(review)
