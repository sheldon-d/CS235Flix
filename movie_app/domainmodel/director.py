class Director:

    def __init__(self, director_full_name: str):
        if isinstance(director_full_name, str) and director_full_name.strip() != "":
            self.__director_full_name = director_full_name.strip()
        else:
            self.__director_full_name = None

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    def __repr__(self) -> str:
        return f"<Director {self.__director_full_name}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Director):
            return False
        return self.__director_full_name == other.__director_full_name

    def __lt__(self, other) -> bool:
        if self.__director_full_name is None:
            return other.__director_full_name is not None
        elif other.__director_full_name is None:
            return False
        return self.__director_full_name < other.__director_full_name

    def __hash__(self):
        return hash(self.__director_full_name)
