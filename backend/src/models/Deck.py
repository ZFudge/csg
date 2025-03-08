import random
from typing import Iterable

from models.DeckAttrs import DeckAttrs
from models.Player import Player


class BaseDeck(DeckAttrs):
    BASE_DECK = DeckAttrs.get_base_deck()


class Deck(BaseDeck):
    """A deck of cards."""

    def __init__(self, shuffle: bool = True):
        self._cards = tuple()
        self._enforce_sufficient_card_supply(shuffle=shuffle)

    @property
    def cards(self):
        """Return copied tuple to further prevent external access or mutation."""
        return tuple(self._cards)

    @cards.setter
    def cards(self, value: Iterable[str]):
        if not isinstance(value, (tuple, list)):
            raise ValueError("Cards must be a tuple or list")
        self._cards = tuple(value)

    def deal_cards(self, players: Iterable[Player]):
        for player in players:
            player.hand.add_cards(self.draw_cards(7))

    def get_card_by_index(self, index: int) -> str:
        return self.cards[index]

    def get_card_by_value(self, value: str) -> str:
        return next((card for card in self.cards if card.value == value), None)

    def _add_cards(self, cards: Iterable[str]):
        """Add a tuple of cards to the deck."""
        if not isinstance(cards, (tuple, list)):
            raise ValueError("Cards must be a tuple or list")
        self._cards = tuple(self._cards) + tuple(cards)

    def draw_cards(self, num: int) -> tuple[str]:
        """Draw a number of cards from the deck."""
        if num not in Deck.DRAWS and not self._is_initial_deal(num):
            raise ValueError(f"Invalid number of cards to draw: {num}, must be one of {Deck.DRAWS}")

        self._enforce_sufficient_card_supply(draw_count=num)

        drawn_cards = self.cards[:num]
        self.cards = tuple(self.cards[num:])
        return tuple(drawn_cards)

    def _is_initial_deal(self, num: int):
        return num == Deck.INITIAL_DEAL_COUNT

    def _enforce_sufficient_card_supply(self, *, draw_count=0, shuffle: bool = True):
        """Adds a new shuffled deck when the current deck is at risk of complete depletion."""
        if draw_count >= len(self.cards):
            new_deck = Deck._get_new_deck(shuffle=shuffle)
            self._add_cards(new_deck)

    @staticmethod
    def _get_new_deck(shuffle: bool = True) -> tuple[str]:
        new_deck = list(Deck.BASE_DECK)
        if shuffle:
            random.shuffle(new_deck)
        return tuple(new_deck)

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return f"Deck(cards={self.cards})"

    def __repr__(self):
        return f"Deck(cards={self.cards})"
