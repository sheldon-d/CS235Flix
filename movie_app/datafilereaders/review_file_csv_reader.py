import csv
from typing import List, Iterable
from pathlib import Path

from movie_app.domainmodel import Review, Movie, User


class ReviewFileCSVReader:

    def __init__(self, file_name: str, movies: List[Movie], users: List[User]):
        if isinstance(file_name, str) and Path(file_name).exists() and '.csv' in file_name:
            self.__file_name = file_name
        else:
            self.__file_name = None

        self.__dataset_of_reviews: List[Review] = list()
        self.__dataset_of_movies: List[Movie] = movies
        self.__dataset_of_users: List[User] = users

    @property
    def file_name(self) -> str:
        return self.__file_name

    @property
    def dataset_of_reviews(self) -> Iterable[Review]:
        return iter(self.__dataset_of_reviews)

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csv_file:
            review_file_reader = csv.DictReader(csv_file)

            Review.reset_id()
            for row in review_file_reader:
                try:
                    user_id = int(row['User ID'])
                except ValueError:
                    user_id = None

                try:
                    movie_rank = int(row['Movie Rank'])
                except ValueError:
                    movie_rank = None

                review_text = row['Review Text']

                try:
                    rating = int(row['Rating'])
                except ValueError:
                    rating = None

                review_movie = next((movie for movie in self.__dataset_of_movies if movie.rank == movie_rank), None)
                review_user = next((user for user in self.__dataset_of_users if user.id == user_id), None)

                review = Review(review_movie, review_text, rating)

                if review_user is not None and review_user.id is not None:
                    review_user.add_review(review)

                if review not in self.__dataset_of_reviews and review.movie is not None and review.user is not None:
                    self.__dataset_of_reviews.append(review)
