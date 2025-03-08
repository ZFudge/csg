import pytest
from src.models.PlayerIndexer import PlayerIndexer


def test_player_indexer_init():
    indexer = PlayerIndexer()
    assert indexer.index == 0
    assert indexer.count == 1
    assert indexer.step == 1
    assert indexer.skip is False

def test_player_indexer_add_player():
    indexer = PlayerIndexer()
    assert indexer.count == 1
    indexer.add_player()
    assert indexer.count == 2
    indexer.add_player()
    assert indexer.count == 3

def test_player_indexer_remove_player():
    indexer = PlayerIndexer()
    assert indexer.count == 1
    indexer.add_player()
    assert indexer.count == 2
    indexer.remove_player()
    assert indexer.count == 1

def test_player_indexer_remove_player_last_player():
    indexer = PlayerIndexer()
    assert indexer.count == 1
    with pytest.raises(ValueError):
        indexer.remove_player()

def test_player_indexer_reverse():
    indexer = PlayerIndexer()
    assert indexer.step == 1
    indexer.reverse()
    assert indexer.step == -1
    indexer.reverse()
    assert indexer.step == 1

def test_player_indexer_step():
    # 8 player game
    indexer = PlayerIndexer()
    indexer.add_player()
    indexer.add_player()
    indexer.add_player()
    indexer.add_player()
    indexer.add_player()
    indexer.add_player()
    indexer.add_player()
    assert indexer.index == 0
    indexer.increment()
    assert indexer.index == 1
    indexer.increment()
    assert indexer.index == 2
    indexer.increment()
    assert indexer.index == 3
    indexer.increment()
    assert indexer.index == 4
    indexer.increment()
    assert indexer.index == 5
    indexer.increment()
    assert indexer.index == 6
    indexer.increment()
    assert indexer.index == 7
    indexer.increment()
    assert indexer.index == 0
    indexer.increment()
    assert indexer.index == 1
    indexer.reverse()
    assert indexer.index == 1
    indexer.increment()
    assert indexer.index == 0
    indexer.increment()
    assert indexer.index == 7
    indexer.increment()
    assert indexer.index == 6
    indexer.increment()
    assert indexer.index == 5
    indexer.increment()
    assert indexer.index == 4

def test_player_indexer_skip():
    indexer = PlayerIndexer()
    indexer.add_player()
    indexer.add_player()
    assert indexer.index == 0

    indexer.skip_player()

    indexer.increment()
    assert indexer.index == 0

    indexer.increment()
    assert indexer.index == 1

    indexer.increment()
    assert indexer.index == 2

    indexer.skip_player()
    indexer.increment()
    assert indexer.index == 2
