from typing import Iterable


class Hand:
    def __init__(self, cards: Iterable[str]):
        self.cards = tuple(cards)

    def play_card(self, card_value: str, index: int) -> str:
        """Play a card from the hand by value and index.
        Card value has already been validated against the previously played card."""
        if index < 0 or index >= len(self.cards):
            raise IndexError(f"Invalid index {index} for hand {self.cards}")
        card = self.cards[index]
        if card.value != card_value:
            raise ValueError(f"Card {card_value} not found in at index {index} of hand {self.cards}")
        self.cards = self.cards[:index] + self.cards[index+1:]
        return card

    def add_cards(self, cards: Iterable[str] | str):
        """Add the results of a single draw, draw 2 or draw 4 to the hand."""
        if isinstance(cards, (list, tuple)):
            self.cards.extend(cards)
        elif isinstance(cards, str):
            self.cards.append(cards)
        else:
            raise ValueError(f"Invalid cards type {type(cards)} of {cards}")
