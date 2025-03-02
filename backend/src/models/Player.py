from src.models.Hand import Hand


class Player:
    def __init__(self, name: str):
        self._name = name
        self._hand = Hand()

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
    def hand(self, *args):
        return

    def accept_cards(self, cards):# Iterable[str] | str):
        self._hand.add_cards(cards)

    def play_card(self, card_value: str, index: int):
        return self._hand.play_card(card_value, index)

    def __str__(self):
        return f"{self.name}: {self.hand}"

    def __repr__(self):
        return f"Player(name={self.name}, hand={self.hand})"

    def __eq__(self, other):
        return (
            self.name == other.name and
            self.hand == other.hand
        )

    def __ne__(self, other):
        return not self.__eq__(other)
