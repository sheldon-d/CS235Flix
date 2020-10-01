from typing import List, Iterable


class Actor:

    def __init__(self, actor_full_name: str):
        if isinstance(actor_full_name, str) and actor_full_name.strip() != "":
            self.__actor_full_name = actor_full_name.strip()
        else:
            self.__actor_full_name = None
        self.__colleagues: List[Actor] = list()

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    @property
    def colleagues(self) -> Iterable['Actor']:
        return iter(self.__colleagues)

    def __repr__(self) -> str:
        return f"<Actor {self.__actor_full_name}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Actor):
            return False
        return self.__actor_full_name == other.__actor_full_name

    def __lt__(self, other) -> bool:
        if self.__actor_full_name is None:
            return other.__actor_full_name is not None
        elif other.__actor_full_name is None:
            return False
        return self.__actor_full_name < other.__actor_full_name

    def __hash__(self):
        return hash(self.__actor_full_name)

    def add_actor_colleague(self, colleague: 'Actor'):
        if isinstance(colleague, Actor) and colleague not in self.__colleagues and self != colleague and \
                colleague.__actor_full_name is not None:
            self.__colleagues.append(colleague)

    def check_if_this_actor_worked_with(self, colleague: 'Actor'):
        return colleague in self.__colleagues
