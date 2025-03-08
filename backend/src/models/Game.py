from logging import getLogger

from models.Card import Card
from models.Deck import Deck as SourceDeck
from models.Player import Player
from models.PlayerManager import PlayerManager

logger = getLogger(__name__)


class Game:
	def __init__(self, owner_name: str, shuffle: bool = True):
		self.players = PlayerManager(owner_name)
		self.deck = SourceDeck(shuffle=shuffle)
		self.started = False

	def add_new_player(self, new_player_name: str):
		if self.started:
			raise ValueError('Game already started')
		return self.players.add_player(new_player_name)

	def remove_player(self, player_name: str):
		if self.started:
			raise ValueError('Game already started')
		self.players.remove_player(player_name)

	def start(self):
		if self.started:
			raise ValueError('Game already started')
		if len(self.players.players) < 2:
			raise ValueError('Not enough players to start the game')
		if len(self.players.players) > 6:
			raise ValueError('Too many players to start the game')
		self.players.init_hashes()
		self.deck.deal_cards(self.players.players)
		self.current_card = Card(self.deck.draw_cards(1)[0])
		self.started = True

	def play_card(self, *, player: str, player_hash: str, card: str, index: int):
		if not self.started:
			raise ValueError('Game not started')
		logger.info(f'Playing card {card} for player {player}')

		player = self.players.get_player(player, player_hash)
		card = Card(card)
		try:
			self._validate_move(player, card)
		except ValueError as e:
			logger.error(e)
			return

		try:
			played_card = player.play_card(value=card.value, index=index)
			self.current_card = played_card
		except ValueError as e:
			logger.error(e)
			return

		self.current_card = played_card

		# Set current player, if needed
		if card.wild:
			# Next player will be set when the current player chooses a color
			pass
		elif card.reverse:
			# Reverse cards work as skip cards in 2-player games.
			if 2 < len(self.players):
				# Reverse the player direction
				self.players.reverse_player_direction()
				self.players.next_player()
		elif card.draw_count:
			self.players.next_player()
			# draw cards against the current player
			new_cards = self.deck.draw_cards(card.draw_count)
			self.players.current_player.accept_cards(new_cards)
		elif card.skip:
			self.players.next_player()
			self.players.next_player()

		return played_card

	def choose_color(self, *, player: str, player_hash: str, color: str):
		player = self.players.get_player(player, player_hash)
		if player != self.current_player:
			raise ValueError('Not your turn')

		last_card = Card(self.current_card)

		self.current_card = Card(color[0])

		self.players.next_player()

		if last_card.draw_count:
			# draw cards against the current player
			new_cards = self.deck.draw_cards(last_card.draw_count)
			self.players.current_player.accept_cards(new_cards)

		return self.current_card

	def _validate_move(self, player: Player, card: Card):
		if not player:
			raise ValueError('Player not found')

		if not self.players.player_is_current(player):
			raise ValueError('Not your turn')

		if not card.is_playable(self.current_card):
			raise ValueError('Invalid card')

	@property
	def current_card(self):
		return self._current_card

	@current_card.setter
	def current_card(self, value: str):
		self._current_card = value

	@property
	def players(self):
		return self._players

	@players.setter
	def players(self, value: PlayerManager):
		self._players = value

	@property
	def deck(self):
		return self._deck

	@deck.setter
	def deck(self, value: SourceDeck):
		self._deck = value

	@property
	def started(self):
		return self._started

	@started.setter
	def started(self, value: bool):
		self._started = value

	@property
	def owner(self):
		return self._players.owner

	@property
	def current_player(self):
		return self.players.current_player

	def __repr__(self):
		return (
			f"Game(current_player={self.current_player}, "
			f"owner={self.owner}, "
			f"players={self.players.players}, "
			f"deck={self.deck})"
		)

	def as_dict(self):
		return {
			'current_player': self.current_player.name,
			'owner': self.owner.name,
			'players': tuple([p.as_dict() for p in self.players.players]),
			'deck': self.deck.cards
		}