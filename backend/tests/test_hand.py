from src.models.Hand import Hand

def test_hand_init():
    hand = Hand(['r1', 'g2', 'b3', 'y4', 'w', 's', 'w+4'])
    assert hand.cards == ('r1', 'g2', 'b3', 'y4', 'w', 's', 'w+4')

def test_hand_add_cards():
    hand = Hand(['r1', 'g2', 'b3', 'y4', 'w', 's', 'w+4'])
    hand.add_cards("r1")
    assert hand.cards == ('r1', 'g2', 'b3', 'y4', 'w', 's', 'w+4', 'r1')

def test_hand_play_card():
    hand = Hand(['r1', 'g2', 'b3', 'y4', 'w', 's', 'w+4'])
    hand.add_cards("r1")
    hand.play_card("r1", 0)
    assert hand.cards == ('g2', 'b3', 'y4', 'w', 's', 'w+4', 'r1')

def test_hand_str():
    hand = Hand(['r1', 'g2', 'b3', 'y4', 'w', 's', 'w+4'])
    hand.add_cards("r1")
    assert str(hand) == "('r1', 'g2', 'b3', 'y4', 'w', 's', 'w+4', 'r1')"

def test_hand_repr():
    hand = Hand(['r1', 'g2', 'b3', 'y4', 'w', 's', 'w+4'])
    hand.add_cards("r1")
    assert repr(hand) == "Hand(cards=('r1', 'g2', 'b3', 'y4', 'w', 's', 'w+4', 'r1'))"

def test_hand_card_count():
    hand = Hand(['r1', 'g2', 'b3', 'y4', 'w', 's', 'w+4'])
    assert hand.card_count == 7

def test_hand_card_count_after_adding_cards():
    hand = Hand(['r1', 'g2', 'b3', 'y4', 'w', 's', 'w+4'])
    hand.add_cards("r1")
    assert hand.card_count == 8

def test_hand_card_count_after_playing_card():
    hand = Hand(['r1', 'g2', 'b3', 'y4', 'w', 's', 'w+4'])
    hand.play_card("r1", 0)
    assert hand.card_count == 6

def test_hand_card_count_after_playing_card_with_multiple_cards():
    hand = Hand([
        'r1',
        'r1',
        'g2',
        'b3',
        'w',
        'y4',
        'w',
        's',
        'w+4',
    ])
    assert hand._as_mapped_counts() == {
        'r1': 2,
        'g2': 1,
        'b3': 1,
        'y4': 1,
        'w': 2,
        's': 1,
        'w+4': 1,
    }

def test_hand_eq():
    hand1 = Hand(['r1', 'g2', 'b3', 'y4', 'w', 's', 'w+4'])
    hand2 = Hand(['r1', 'g2', 'b3', 'y4', 'w', 's', 'w+4'])
    assert hand1 == hand2

def test_hand_ne():
    hand1 = Hand(['r1', 'g2', 'b3', 'y4', 'w', 's', 'w+4'])
    hand2 = Hand(['r1', 'g2', 'b3', 'y4', 'w', 's', 'w+4', 'r1'])
    assert hand1 != hand2

def test_hand_ne_with_different_card_count():
    hand1 = Hand(['r1', 'g2', 'b3', 'y4', 'w', 's', 'w+4', 'r1'])
    hand2 = Hand(['r1', 'g2', 'b3', 'y4', 'w', 's', 'w+4'])
    assert hand1 != hand2
