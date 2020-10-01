class Genre:

    def __init__(self, genre_name: str):
        if isinstance(genre_name, str) and genre_name.strip() != "":
            self.__genre_name = genre_name.strip()
        else:
            self.__genre_name = None

    @property
    def genre_name(self) -> str:
        return self.__genre_name

    def __repr__(self) -> str:
        return f"<Genre {self.__genre_name}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Genre):
            return False
        return self.__genre_name == other.__genre_name

    def __lt__(self, other) -> bool:
        if self.__genre_name is None:
            return other.__genre_name is not None
        elif other.__genre_name is None:
            return False
        return self.__genre_name < other.__genre_name

    def __hash__(self):
        return hash(self.__genre_name)
