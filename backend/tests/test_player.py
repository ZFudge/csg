from src.models.Player import Player

def test_player_init():
    player = Player("Cleo")
    assert player.name == "Cleo"
    assert player.hand.cards == ()

def test_player_name():
    player = Player("Cleo")
    player.name = "Cleo"
    assert player.name == "Cleo"

def test_player_accept_cards():
    player = Player("Cleo")
    player.accept_cards(['r1', 'g2', 'b3', 'y4', 'w', 's', 'w+4'])
    assert player.hand.cards == ('r1', 'g2', 'b3', 'y4', 'w', 's', 'w+4')

def test_player_repr():
    assert repr(Player("Cleo")) == "Player(name=Cleo, hand=())"

def test_player_play_card():
    player = Player("Cleo")
    player.accept_cards(['r1', 'g2', 'b3', 'y4', 'w', 's', 'w+4'])
    card = player.play_card(value='r1', index=0)
    assert card == 'r1'
    assert player.hand.cards == ('g2', 'b3', 'y4', 'w', 's', 'w+4')

def test_player_str():
    player = Player("Cleo")
    player.accept_cards(['r1', 'g2', 'b3', 'y4', 'w', 's', 'w+4'])
    assert str(player) == "Cleo: ('r1', 'g2', 'b3', 'y4', 'w', 's', 'w+4')"
