from sqlalchemy import (
    Table, MetaData, Column, Integer, String, ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from movie_app.domainmodel import *

metadata = MetaData()


def map_model_to_tables():
    pass
