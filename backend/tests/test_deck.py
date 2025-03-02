import pytest

from src.models.Deck import Deck


def test_get_base_deck():
    assert len(Deck.get_base_deck()) == 108

def test_enforce_sufficient_card_supply():
    assert len(Deck().cards) == 108

def test_add_cards():
    deck = Deck()
    deck._add_cards(('w', 'w+4'))
    assert len(deck.cards) == 110
    assert isinstance(deck.cards, tuple)

def test_add_cards_invalid():
    with pytest.raises(ValueError):
        Deck()._add_cards("pizza")

def test_draw_card():
    deck = Deck()
    cards = deck.draw_cards(1)
    assert len(cards) == 1
    assert len(deck.cards) == 107

def test_draw_cards():
    deck = Deck()
    cards = deck.draw_cards(4)
    assert len(cards) == 4
    assert len(deck.cards) == 104

def test_draw_cards_invalid():
    with pytest.raises(ValueError):
        Deck().draw_cards(5)

def test_enforce_sufficient_card_supply_invalid():
    with pytest.raises(ValueError):
        Deck().draw_cards(108)

def test_enforce_sufficient_card_supply_invalid_draw_count():
    with pytest.raises(ValueError):
        Deck().draw_cards(109)

def test_get_new_shuffled_deck():
    new_deck = Deck()._get_new_shuffled_deck()
    assert len(new_deck) == 108
    assert isinstance(new_deck, tuple)
