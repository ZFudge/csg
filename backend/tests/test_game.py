from models.Card import Card
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

def test_game_play_wild_card():
    """Test that the card is played and the current player is updated."""
    # Don't shuffle the deck to make the test deterministic.
    game = Game("Cleo", shuffle=False)
    game.add_new_player("Mathias")
    game.start()

    current_player = game.current_player
    card = Card(current_player.hand.cards[0])
    assert card.wild is True
    assert card.draw_count is None
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
