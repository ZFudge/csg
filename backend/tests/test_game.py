import pytest

from src.models.Card import Card
from src.models.Game import Game
from src.models.Player import Player


def test_game_init():
    game = Game("Cleo")
    owner = Player("Cleo")
    assert game.owner == owner
    assert game.players.names == (owner.name,)
    assert game.players.index == 0
    assert len(game.deck) == 112
    assert game.current_player == owner


def test_game_add_player():
    game = Game("Cleo")
    game.add_new_player("Mathias")
    assert game.players.players == (game.players.owner, Player("Mathias"))
    assert game.current_player == game.players.owner


def test_game_remove_player():
    game = Game("Cleo")
    game.add_new_player("Mathias")
    game.remove_player("Mathias")
    assert game.players.players == (game.players.owner,)


def test_game_str():
    game = Game("Cleo")
    game.add_new_player("Mathias")
    assert str(game).startswith("Game(current_player=Cleo: (), owner=Cleo: (), players=(Player(name=Cleo, hand=()), Player(name=Mathias, hand=())), deck=Deck(cards=(")


def test_game_repr():
    game = Game("Cleo")
    game.add_new_player("Mathias")
    assert str(game).startswith("Game(current_player=Cleo: (), owner=Cleo: (), players=(Player(name=Cleo, hand=()), Player(name=Mathias, hand=())), deck=Deck(cards=(")


def test_game_start():
    game = Game("Cleo")
    game.add_new_player("Mathias")
    assert game.started is False
    game.start()
    assert game.started is True


def test_game_deal_cards():
    game = Game("Cleo")
    game.add_new_player("Mathias")
    game.start()
    assert len(game.players.players[0].hand.cards) == 7
    assert len(game.players.players[1].hand.cards) == 7
    assert len(game.deck.cards) == 97


def test_game_choose_color():
    game = Game("Cleo")
    game.add_new_player("Mathias")
    game.start()

    game.choose_color(
        player="Cleo",
        player_hash=game.players.players[0].hash,
        color="r"
    )
    assert game.current_card == Card("r")

    game.players.next_player()
    game.choose_color(
        player="Cleo",
        player_hash=game.players.players[0].hash,
        color="g"
    )
    assert game.current_card == Card("g")

    game.players.next_player()
    game.choose_color(
        player="Cleo",
        player_hash=game.players.players[0].hash,
        color="b"
    )
    assert game.current_card == Card("b")

    game.players.next_player()
    game.choose_color(
        player="Cleo",
        player_hash=game.players.players[0].hash,
        color="y"
    )
    assert game.current_card == Card("y")


def test_game_play_wild_card():
    """Test that the card is played and the current player is updated."""
    # Don't shuffle the deck to make the test deterministic.
    game = Game("Cleo", shuffle=False)
    game.add_new_player("Mathias")
    game.start()

    current_player = game.current_player
    card = Card("w")
    assert card.wild is True
    assert card.draw_count == 0
    assert card.color is None
    assert card.number is None
    remaining_expected = current_player.hand.cards[1:]

    assert game.players.current_player == game.players.players[0]

    played_card = Card(game.play_card(
        player="Cleo",
        player_hash=current_player.hash,
        card=card.value,
        index=0
    ))
    assert played_card == card
    assert remaining_expected == game.players.players[0].hand.cards

    game.choose_color(
        player="Cleo",
        player_hash=current_player.hash,
        color="r"
    )
    assert game.current_card == Card("r")
    assert game.current_player == game.players.players[1]


def test_game_play_draw_four_wild_card():
    game = Game("Cleo", shuffle=False)
    game.add_new_player("Mathias")
    game.start()

    assert len(game.players.players[0].hand.cards) == 7
    assert len(game.players.players[1].hand.cards) == 7
    assert len(game.deck.cards) == 97

    current_player = game.current_player
    card = Card(current_player.hand.cards[4])
    assert card.wild is True
    assert card.draw_count == 4
    assert card.color is None
    assert card.number is None

    remaining_expected = current_player.hand.cards[:4] + current_player.hand.cards[5:]
    played_card = Card(game.play_card(
        player="Cleo",
        player_hash=current_player.hash,
        card=card.value,
        index=4
    ))
    assert played_card == card
    assert remaining_expected == game.players.players[0].hand.cards

    game.choose_color(
        player="Cleo",
        player_hash=current_player.hash,
        color="r"
    )

    assert len(game.players.players[1].hand.cards) == 11
    assert game.current_player == game.players.players[1]


def test_game_play_draw_two_card():
    game = Game("Cleo", shuffle=False)
    game.add_new_player("Mathias")
    game.start()

    current_player = game.current_player
    # Blue draw two card
    card = Card("b+2")
    current_player.accept_cards(card.value)

    assert len(game.players.players[1].hand.cards) == 7

    game.current_card = Card("b2")
    played_card = Card(game.play_card(
        player="Cleo",
        player_hash=current_player.hash,
        card=card.value,
        index=7
    ))
    assert played_card == card

    assert game.current_player == game.players.players[1]
    assert len(game.players.players[1].hand.cards) == 9


def test_game_play_reverse_card_two_players():
    game = Game("Cleo", shuffle=False)
    game.add_new_player("Mathias")
    game.start()

    current_player = game.current_player
    # Green reverse card
    card = Card("gr")
    current_player.accept_cards(card.value)

    # Manually set the current card to green to allow the green reverse card to be played
    game.current_card = Card("g")
    played_card = Card(game.play_card( 
        player="Cleo",
        player_hash=current_player.hash,
        card=card.value,
        index=7
    ))
    assert played_card == card
    assert game.current_player == game.players.players[0]


def test_game_play_reverse_card_three_players():
    game = Game("Cleo", shuffle=False)
    game.add_new_player("Mathias")
    aloysius = game.add_new_player("Aloysius")
    game.start()

    current_player = game.current_player
    # Green reverse card
    card = Card("gr")
    current_player.accept_cards(card.value)

    # Manually set the current card to green to allow the green reverse card to be played
    game.current_card = Card("g")
    played_card = Card(game.play_card( 
        player="Cleo",
        player_hash=current_player.hash,
        card=card.value,
        index=7
    ))
    assert played_card == card
    assert game.current_player == aloysius


def test_game_play_skip_card_two_players():
    game = Game("Cleo", shuffle=False)
    game.add_new_player("Mathias")
    game.start()

    current_player = game.current_player
    # Red skip card
    card = Card("rs")
    current_player.accept_cards(card.value)

    # Manually set the current card to red to allow the red skip card to be played
    game.current_card = Card("r")
    played_card = Card(game.play_card(
        player="Cleo",
        player_hash=current_player.hash,
        card=card.value,
        index=7
    ))
    assert played_card == card
    assert game.current_player == game.players.players[0]


def test_game_play_skip_card_three_players():
    game = Game("Cleo", shuffle=False)
    game.add_new_player("Mathias")
    aloysius = game.add_new_player("Aloysius")
    game.start()

    # Yellow skip card
    card = Card("ys")
    current_player = game.current_player
    current_player.accept_cards(card.value)

    # Manually set the current card to yellow to allow the yellow skip card to be played
    game.current_card = Card("y")
    played_card = Card(game.play_card(
        player="Cleo",
        player_hash=current_player.hash,
        card=card.value,
        index=7
    ))
    assert played_card == card
    assert game.current_player == aloysius


def test_game_dict():
    game = Game("Cleo", shuffle=False)
    game.add_new_player("Mathias")
    game.start()

    assert game.as_dict() == {
        'current_player': 'Cleo',
        'owner': 'Cleo',
        'players': (
            {
                'name': 'Cleo',
                'hand': (
                    'w',
                    'w',
                    'w',
                    'w',
                    'w+4',
                    'w+4',
                    'w+4'
                )
            },
            {
                'name': 'Mathias',
                'hand': (
                    'w+4',
                    'r0',
                    'r0',
                    'r1',
                    'r1',
                    'r2',
                    'r2',
                )
            }
        ),
        'deck': (
           'r3',
           'r4',
           'r4',
           'r5',
           'r5',
           'r6',
           'r6',
           'r7',
           'r7',
           'r8',
           'r8',
           'r9',
           'r9',
           'rs',
           'rs',
           'rr',
           'rr',
           'r+2',
           'r+2',
           'g0',
           'g0',
           'g1',
           'g1',
           'g2',
           'g2',
           'g3',
           'g3',
           'g4',
           'g4',
           'g5',
           'g5',
           'g6',
           'g6',
           'g7',
           'g7',
           'g8',
           'g8',
           'g9',
           'g9',
           'gs',
           'gs',
           'gr',
           'gr',
           'g+2',
           'g+2',
           'b0',
           'b0',
           'b1',
           'b1',
           'b2',
           'b2',
           'b3',
           'b3',
           'b4',
           'b4',
           'b5',
           'b5',
           'b6',
           'b6',
           'b7',
           'b7',
           'b8',
           'b8',
           'b9',
           'b9',
           'bs',
           'bs',
           'br',
           'br',
           'b+2',
           'b+2',
           'y0',
           'y0',
           'y1',
           'y1',
           'y2',
           'y2',
           'y3',
           'y3',
           'y4',
           'y4',
           'y5',
           'y5',
           'y6',
           'y6',
           'y7',
           'y7',
           'y8',
           'y8',
           'y9',
           'y9',
           'ys',
           'ys',
           'yr',
           'yr',
           'y+2',
           'y+2',
        )
    }


def test_game_validate_move_wild_card():
    game = Game("Cleo", shuffle=False)
    game.add_new_player("Mathias")
    game.start()

    current_player = game.current_player
    card = Card("w")
    assert card.wild is True
    assert game._validate_move(current_player, card) is True


def test_game_validate_move_draw_four_wild_card():
    game = Game("Cleo", shuffle=False)
    game.add_new_player("Mathias")
    game.start()

    current_player = game.current_player
    card = Card("w+4")
    assert card.wild is True
    assert card.draw_count == 4
    assert game._validate_move(current_player, card) is True


def test_game_validate_move_draw_two_card():
    game = Game("Cleo", shuffle=False)
    game.add_new_player("Mathias")
    game.start()
    game.current_card = Card("b")

    current_player = game.current_player
    card = Card("b+2")
    assert card.wild is False
    assert card.draw_count == 2
    assert game._validate_move(current_player, card) is True


def test_game_validate_move_reverse_card():
    game = Game("Cleo", shuffle=False)
    game.add_new_player("Mathias")
    game.start()

    game.current_card = Card("g")
    current_player = game.current_player
    card = Card("gr")
    assert card.wild is False
    assert card.reverse is True
    assert game._validate_move(current_player, card) is True


def test_game_player_turn_play_card():
    game = Game("Cleo", shuffle=False)
    game.add_new_player("Mathias")
    game.start()

    assert game.current_player == game.players.players[0]

    with pytest.raises(ValueError):
        game.play_card(
            player="Mathias",
            player_hash=game.players.players[1].hash,
            card=Card("w+4").value,
            index=0
        )


def test_game_player_turn_choose_color():
    game = Game("Cleo", shuffle=False)
    game.add_new_player("Mathias")
    game.start()

    assert game.current_player == game.players.players[0]

    with pytest.raises(ValueError):
        game.choose_color(
            player="Mathias",
            player_hash=game.players.players[1].hash,
            color="r"
        )
