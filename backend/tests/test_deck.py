import pytest

from src.models.Deck import Deck


def test_get_base_deck():
    base_deck = Deck.get_base_deck()
    assert len(base_deck) == 108

def test_draw_cards():
    deck = Deck()
    cards = deck.draw_cards(1)
    assert len(cards) == 1
    assert cards[0] in deck.cards

def test_draw_cards_invalid():
    deck = Deck()
    with pytest.raises(ValueError):
        deck.draw_cards(5)
