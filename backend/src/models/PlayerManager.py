from models.Player import Player
from models.PlayerIndexer import PlayerIndexer


class PlayerManager:
    """Manages players instances and dealer actions."""

    def __init__(self, owner_name: str):
        self.owner = Player(owner_name)
        self.players = (self.owner,)
        self._indexer = PlayerIndexer()

    def add_player(self, player_name: str):
        """Add a player to the game."""
        if player_name in self.names:
            raise ValueError(f"Player {player_name} already exists")
        player = Player(player_name)
        self.players = self.players + (player,)
        self._indexer.add_player()
        return player

    def remove_player(self, player_name: str):
        """Remove a player from the game."""
        try:
            self.players = tuple(player for player in self.players if player.name != player_name)
            self._indexer.remove_player()
        except ValueError:
            raise ValueError("Cannot remove the last player")

    def next_player(self):
        self._indexer.increment()
        return self.players[self._indexer.index]

    def reverse_player_direction(self):
        self._indexer.reverse()

    def init_hashes(self):
        for player in self.players:
            player.init_hash()

    def player_is_current(self, player: Player) -> bool:
        """Check if the player is the current player."""
        return player == self.current_player
    # def player_is_current(self, player_name: str, player_hash: str) -> bool:
    #     """Check if the player is the current player."""
    #     return (
    #         player_name == self.current_player.name and
    #         player_hash == self.current_player.hash
    #     )

    def get_player(self, player_name: str, player_hash: str) -> Player:
        """Get a player by name and hash."""
        return next((player for player in self.players if player.name == player_name and player.hash == player_hash), None)

    @property
    def index(self):
        return self._indexer.index

    @property
    def names(self) -> tuple[str]:
        return tuple(player.name for player in self.players)

    @property
    def current_player(self):
        return self.players[self._indexer.index]

    @current_player.setter
    def current_player(self, value: Player):
        self._indexer.index = self.players.index(value)

    @property
    def owner(self):
        return self.players[0]

    @owner.setter
    def owner(self, value: Player):
        self._players = (value,)

    @property
    def players(self):
        return tuple(self._players)

    @players.setter
    def players(self, value: tuple[Player]):
        self._players = value

    def __get__(self):
        return tuple(self.players)

    def __getitem__(self, index: int):
        return self.players[index]

    def __len__(self):
        return len(self.players)
