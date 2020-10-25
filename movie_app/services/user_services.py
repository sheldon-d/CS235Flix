from movie_app.adapters.repository import AbstractRepository
from movie_app.domainmodel import User, Review, WatchList


class ServicesException(Exception):
    def __init__(self, message=None):
        pass


def get_review(review_id: int, repo: AbstractRepository) -> Review:
    review = repo.get_review(review_id)
    if review is None:
        raise ServicesException('Review does not exist in the repository')
    return review
