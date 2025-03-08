import pytest

from models.Card import Card

def test_card_init():
    card = Card('r0')
    assert card.color == 'r'
    assert card.number == 0

def test_card_init_invalid():
    with pytest.raises(ValueError):
        Card('invalid')

def test_card_init_wild():
    card = Card('w+4')
    assert card.wild is True
    assert card.draw_count == 4

def test_card_init_action():
    card = Card('r+2')
    assert card.color == 'r'
    assert card.action == '+2'
