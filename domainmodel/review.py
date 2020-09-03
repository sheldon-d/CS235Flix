from datetime import datetime
from domainmodel.movie import Movie
# from domainmodel.user import User


class Review:

    def __init__(self, movie: 'Movie', review_text: str, rating: int):
        if isinstance(movie, Movie):
            self.__movie = movie
        else:
            self.__movie = None

        if isinstance(review_text, str) and review_text.strip() != "":
            self.__review_text = review_text.strip()
        else:
            self.__review_text = None

        if isinstance(rating, int) and 1 <= rating <= 10:
            self.__rating = rating
        else:
            self.__rating = None

        self.__timestamp: datetime = datetime.today()
        self.__user = None

    @property
    def movie(self) -> 'Movie':
        return self.__movie

    @property
    def review_text(self) -> str:
        return self.__review_text

    @property
    def rating(self) -> int:
        return self.__rating

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    # @property
    # def user(self) -> 'User':
    #     return self.__user
    #
    # @user.setter
    # def user(self, user: 'User'):
    #     if isinstance(user, User) and user.user_name is not None:
    #         self.__user = user

    def __repr__(self) -> str:
        return f"<Review {self.__movie.title}, {self.__rating}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Review):
            return False
        return self.__movie == other.__movie and self.__review_text == other.__review_text and \
               self.__rating == other.__rating and self.__timestamp == other.__timestamp
