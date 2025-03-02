import random
from typing import Iterable


class DeckAttrs:
    COLORS = ('r', 'g', 'b', 'y')
    DRAWS = (1, 2, 4)
    ACTIONS = ('s', '+2', 'r')
    DRAWS_TYPE_VALUES = {
        '+2': 2,
        '+4': 4,
    }

    @staticmethod
    def get_base_deck():
        """Returns a tuple of all the cards expected in a basic deck."""
        base_deck = []
        base_deck.extend(('w',) * 4)
        base_deck.extend(('w+4',) * 4)
        for color in DeckAttrs.COLORS:
            base_deck.append(f'{color}0')
            for n in range(1, 10):
                base_deck.extend((f'{color}{n}',) * 2)
            for action in DeckAttrs.ACTIONS:
                base_deck.extend((f'{color}{action}',) * 2)
        return tuple(base_deck)


class BaseDeck(DeckAttrs):
    BASE_DECK = DeckAttrs.get_base_deck()


class Deck(BaseDeck):
    """A deck of cards."""

    def __init__(self):
        self._cards = tuple()
        self._enforce_sufficient_card_supply()

    @property
    def cards(self):
        """Return copied tuple to further prevent external access or mutation."""
        return tuple(self._cards)

    @cards.setter
    def cards(self, value: Iterable[str]):
        if not isinstance(value, (tuple, list)):
            raise ValueError("Cards must be a tuple or list")
        self._cards = tuple(value)

    def _add_cards(self, cards: Iterable[str]):
        """Add a tuple of cards to the deck."""
        if not isinstance(cards, (tuple, list)):
            raise ValueError("Cards must be a tuple or list")
        self._cards = tuple(self._cards) + tuple(cards)

    def draw_cards(self, num: int):# -> tuple[str]:
        """Draw a number of cards from the deck."""
        if num not in Deck.DRAWS:
            raise ValueError(f"Invalid number of cards to draw: {num}, must be one of {Deck.DRAWS}")

        self._enforce_sufficient_card_supply(draw_count=num)

        drawn_cards = self.cards[:num]
        self.cards = tuple(self.cards[num:])
        return tuple(drawn_cards)

    def _enforce_sufficient_card_supply(self, *, draw_count=0):
        """Adds a new shuffled deck when the current deck is at risk of complete depletion."""
        if draw_count >= len(self.cards):
            new_deck = Deck._get_new_shuffled_deck()
            self._add_cards(new_deck)

    @staticmethod
    def _get_new_shuffled_deck():# -> tuple[str]:
        new_deck = list(Deck.BASE_DECK)
        random.shuffle(new_deck)
        return tuple(new_deck)

    def __len__(self):
        return len(self.cards)
