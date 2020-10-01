from movie_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from pathlib import Path

import pytest


@pytest.fixture()
def movie_file_reader():
    path = str(Path.cwd().joinpath('movie_app', 'adapters', 'datafiles', 'Data1000Movies.csv'))
    return MovieFileCSVReader(path)
