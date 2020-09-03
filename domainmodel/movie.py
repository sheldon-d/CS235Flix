from typing import List
from domainmodel.genre import Genre
from domainmodel.actor import Actor
from domainmodel.director import Director


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
        self.__director: 'Director' = Director(str())
        self.__actors: List['Actor'] = list()
        self.__genres: List['Genre'] = list()
        self.__runtime_minutes = None

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
    def director(self) -> 'Director':
        return self.__director

    @director.setter
    def director(self, director: 'Director'):
        if isinstance(director, Director):
            self.__director = director

    @property
    def actors(self) -> List['Actor']:
        return self.__actors

    @property
    def genres(self) -> List['Genre']:
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

    def add_actor(self, actor: 'Actor'):
        if isinstance(actor, Actor) and actor not in self.__actors and actor.actor_full_name is not None:
            self.__actors.append(actor)

    def remove_actor(self, actor: 'Actor'):
        if actor in self.__actors:
            self.__actors.remove(actor)

    def add_genre(self, genre: 'Genre'):
        if isinstance(genre, Genre) and genre not in self.__genres and genre.genre_name is not None:
            self.__genres.append(genre)

    def remove_genre(self, genre: 'Genre'):
        if genre in self.__genres:
            self.__genres.remove(genre)
