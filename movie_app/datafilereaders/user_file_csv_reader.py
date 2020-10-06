import csv
from typing import List, Iterable
from pathlib import Path

from movie_app.domainmodel import User


class UserFileCSVReader:

    def __init__(self, file_name: str):
        if isinstance(file_name, str) and Path(file_name).exists() and '.csv' in file_name:
            self.__file_name = file_name
        else:
            self.__file_name = None

        self.__dataset_of_users: List[User] = list()

    @property
    def file_name(self) -> str:
        return self.__file_name

    @property
    def dataset_of_users(self) -> Iterable[User]:
        return iter(self.__dataset_of_users)

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csv_file:
            user_file_reader = csv.DictReader(csv_file)

            for row in user_file_reader:
                try:
                    user_id = int(row['ID'])
                except ValueError:
                    user_id = None

                user_name = row['Name']
                password = row['Password']

                user = User(user_name, password)
                user.id = user_id

                if user not in self.__dataset_of_users and user.id is not None:
                    self.__dataset_of_users.append(user)
