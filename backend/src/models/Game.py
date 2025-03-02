from models import Deck, Player, PlayerManager


class Game:
	def __init__(self, owner_name: str):
		self._players = PlayerManager(owner_name)
		self._deck = Deck()

	def add_new_player(self, new_player: Player):
		if not isinstance(new_player, Player):
			raise ValueError("new_player must be a Player instance")
		if new_player.name in self._players:
			raise ValueError("new_player must be a unique Player instance")
		self._players = self._players + (new_player,)

	def remove_player(self, player: Player):
		self._players = tuple(player for player in self._players if player != player)

	@property
	def owner(self):
		return self._players.owner

	@property
	def players(self):
		return self._players

	@property
	def deck(self):
		return self._deck

	@property
	def current_player(self):
		return self._player_manager.current_player

	def __str__(self):
		return f"Game(players={self._players}, deck={self._deck}, current_player={self._current_player})"

	def __repr__(self):
		return f"Game(players={self._players}, deck={self._deck}, current_player={self._current_player})"

