import hashlib
import time
from typing import Iterable

from models.Hand import Hand


class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand = Hand()
        self.hash = None

    def init_hash(self):
        self._hash = hashlib.sha256(
            self.name.encode() +
            str(self.hand.cards).encode() +
            str(time.time()).encode()
        ).hexdigest()

    def accept_cards(self, cards: Iterable[str] | str):
        self._hand.add_cards(cards)

    def play_card(self, *, value: str, index: int):
        return self._hand.play_card(value, index)

    @property
    def hash(self):
        return self._hash

    @hash.setter
    def hash(self, value: str):
        self._hash = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        self._name = value

    @property
    def hand(self):
        return self._hand

    @hand.setter
    def hand(self, value: Hand):
        self._hand = value

    def __str__(self):
        return f"{self.name}: {self.hand}"

    def __repr__(self):
        return f"Player(name={self.name}, hand={self.hand})"

    def __eq__(self, other):
        return (
            self.name == other.name and
            self.hash == other.hash
        )

    def __ne__(self, other):
        return not self.__eq__(other)
