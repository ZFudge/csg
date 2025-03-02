from src.models import Player, PlayerManager

def test_player_manager_init():
    player_manager = PlayerManager("Cleo")
    assert player_manager.owner.name == "Cleo"
    assert player_manager.players == (Player("Cleo"),)

def test_player_manager_add_player():
    player_manager = PlayerManager("Cleo")
    player_manager.add_player("Aloysius")
    assert player_manager.players == (Player("Cleo"), Player("Aloysius"))

def test_player_manager_remove_player():
    player_manager = PlayerManager("Cleo")
    player_manager.remove_player("Cleo")
    assert player_manager.players == tuple()

def test_player_manager_next_player():
    player_manager = PlayerManager("Cleo")
    player_manager.add_player("Aloysius")
    assert player_manager.next_player() == Player("Aloysius")

def test_player_manager_reverse_player_direction():
    player_manager = PlayerManager("Cleo")
    player_manager.add_player("Aloysius")
    player_manager.reverse_player_direction()
    assert player_manager.next_player() == Player("Cleo")

def test_player_manager_get_item():
    player_manager = PlayerManager("Cleo")
    player_manager.add_player("Aloysius")
    assert player_manager[0] == Player("Cleo")
    assert player_manager[1] == Player("Aloysius")

def test_player_manager_len():
    player_manager = PlayerManager("Cleo")
    player_manager.add_player("Aloysius")
    assert len(player_manager) == 2

def test_player_manager_get():
    player_manager = PlayerManager("Cleo")
    player_manager.add_player("Aloysius")
    assert player_manager.names == ("Cleo", "Aloysius")

def test_player_manager_current_player():
    player_manager = PlayerManager("Cleo")
    assert player_manager.current_player.name == "Cleo"

def test_player_manager_owner():
    player_manager = PlayerManager("Cleo")
    assert player_manager.owner.name == "Cleo"

def test_player_manager_players():
    player_manager = PlayerManager("Cleo")
    player_manager.add_player("Aloysius")
    assert player_manager.players == (Player("Cleo"), Player("Aloysius"))
