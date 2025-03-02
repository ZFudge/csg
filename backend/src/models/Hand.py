from typing import Iterable


class Hand:
    def __init__(self, cards: Iterable[str]=None):
        self._cards = tuple()
        if cards is not None:
            self.add_cards(cards)

    @property
    def cards(self):
        return tuple(self._cards)

    def play_card(self, card_value: str, index: int) -> str:
        """Play a card from the hand by value and index.
        Card value has already been validated against the previously played card."""
        if index < 0 or index >= len(self.cards):
            raise IndexError(f"Invalid index {index} for hand {self.cards}")
        card = self.cards[index]
        if card != card_value:
            raise ValueError(f"Card {card_value} not found in at index {index} of hand {self.cards}")
        self._cards = tuple(self._cards[:index] + self._cards[index+1:])
        return card

    def add_cards(self, cards):#: Iterable[str] | str):
        """Add the results of a single draw, draw 2 or draw 4 to the hand."""
        if isinstance(cards, (list, tuple)):
            self._cards = self._cards + tuple(cards)
        elif isinstance(cards, str):
            self._cards = self._cards + (cards,)
        else:
            raise ValueError(f"Invalid cards type {type(cards)} of {cards}")

    @property
    def card_count(self) -> int:
        return len(self.cards)

    def _as_mapped_counts(self) -> dict:#[str, int]:
        """Return a dictionary of card values and their counts."""
        result = {}
        for card in self.cards:
            result[card] = result.setdefault(card, 0) + 1
        return result

    def __eq__(self, other):
        """Two hands are equal if they have the same number of cards of each value."""
        if not isinstance(other, Hand):
            return False
        if len(self.cards) != len(other.cards):
            return False
        return self._as_mapped_counts() == other._as_mapped_counts()

    def __ne__(self, other):
        """Two hands are not equal if they have a different number of cards of any value."""
        return not self.__eq__(other)

    def __str__(self):
        return f"{self.cards}"

    def __repr__(self):
        return f"Hand(cards={self.cards})"
