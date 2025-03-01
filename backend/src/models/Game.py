from typing import Iterable

from models.Player import Player, Deck


class Game:
	def __init__(self, owner: Player):
		self._owner = owner
		self._players = (owner,)
		self._current_player = owner
		self._deck = Deck()

	def get_owner(self):
		return self._owner

	def get_players(self):
		return self._players

	def get_current_player(self):
		return self._current_player

	def set_current_player(self, player: Player):
		self._current_player = player

	def add_new_player(self, new_player_name: str):
		new_player = Player(new_player_name)
		self._players = self._players + (new_player,)

	def remove_player(self, player: Player):
		self._players = tuple(player for player in self._players if player != player)

