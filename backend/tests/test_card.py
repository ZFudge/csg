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
    card = Card('w')
    assert card.wild is True
    assert card.draw_count == 0

def test_card_init_draw_four():
    card = Card('w+4')
    assert card.wild is True
    assert card.draw_count == 4
    assert card.action == '+4'

def test_card_init_action():
    card = Card('r+2')
    assert card.color == 'r'
    assert card.action == '+2'

def test_card_init_draw_two():
    card = Card('r+2')
    assert card.color == 'r'
    assert card.action == '+2'
    assert card.draw_count == 2

def test_card_init_reverse():
    card = Card('rr')
    assert card.color == 'r'
    assert card.action == 'r'
    assert card.reverse is True

def test_card_init_skip():
    card = Card('rs')
    assert card.color == 'r'
    assert card.action == 's'
    assert card.skip is True

def test_card_invalid():
    with pytest.raises(ValueError):
        Card('w+')
    with pytest.raises(ValueError):
        Card('g-1')
    with pytest.raises(ValueError):
        Card('+4')
    with pytest.raises(ValueError):
        Card('r11')
