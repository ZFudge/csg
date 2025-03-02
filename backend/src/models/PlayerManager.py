from models import Player, PlayerIndexer


class PlayerManager:
    """Manages players instances and dealer actions."""

    def __init__(self, owner_name: str):
        self._owner = Player(owner_name)
        self._players = (self._owner,)
        self._indexer = PlayerIndexer()

    def add_player(self, player_name: str):
        """Add a player to the game."""
        if player_name in self.names:
            raise ValueError(f"Player {player_name} already exists")
        player = Player(player_name)
        self._players = self._players + (player,)
        self._indexer.add_player()

    def remove_player(self, player_name: str):
        """Remove a player from the game."""
        self._players = tuple(player for player in self._players if player.name != player_name)
        self._indexer.remove_player()

    def next_player(self):
        self._indexer.increment_handler()
        return self._players[self._indexer.index]

    def reverse_player_direction(self):
        self._indexer.reverse()
    
    @property
    def names(self) -> tuple:#[str]:
        return tuple(player.name for player in self._players)

    @property
    def current_player(self):
        return self._players[self._indexer.index]

    @property
    def owner(self):
        return self._players[0]

    @property
    def players(self):
        return tuple(self._players)

    def __get__(self):
        return tuple(self._players)

    def __getitem__(self, index: int):
        return self._players[index]

    def __len__(self):
        return len(self._players)
