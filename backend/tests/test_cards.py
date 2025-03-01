import src.deck as deck
import src.utils as utils

GAME_HASH_LENGTH = 8


def test_get_new_game_hash():
    new_game_hash = utils.get_new_game_hash(GAME_HASH_LENGTH)
    assert len(new_game_hash) == GAME_HASH_LENGTH


def test_get_new_deck():
    new_deck = utils.get_new_deck()
    assert len(new_deck) == 2 * len(deck.deck)

    new_deck = utils.get_new_deck(7)
    assert len(new_deck) == 7 * len(deck.deck)

    new_deck = utils.get_new_deck(9)
    assert len(new_deck) == 9 * len(deck.deck)


def test_sort_cards_by_type_and_color():
    unsorted_cards = ['b4', 'g0', 'y9', 'w+4', 'rs', 'r1', 'b0', 'yd', 'gr', 'w', 'g8', 'bd', 'y7']
    unsorted_cards += ['r0', 'bs', 'w', 'rs', 'gs',	'y3', 'w+4', 'b2', 'g5', 'g4', 'y1', 'r6', 'w']
    unsorted_cards += ['ys', 'rd', 'yr', 'bd', 'w', 'y9', 'g2', 'gd', 'bs', 'w+4', 'b5', 'w', 'y8']
    
    sorted_cards = utils.sort_cards_by_type_and_color(unsorted_cards)

    expected_cards = ['r0', 'r1', 'r6', 'rd', 'rs', 'rs', 'g0', 'g2', 'g4', 'g5', 'g8', 'gd', 'gr']
    expected_cards += ['gs', 'b0', 'b2', 'b4', 'b5', 'bd', 'bd', 'bs', 'bs', 'y1', 'y3', 'y7', 'y8']
    expected_cards += ['y9', 'y9', 'yd', 'yr', 'ys', 'w+4', 'w+4', 'w+4', 'w', 'w', 'w', 'w', 'w']

    assert sorted_cards == expected_cards

