import json
from os import getenv

from dotenv import load_dotenv

from flask import Blueprint, jsonify, request
from flask.helpers import send_from_directory
from werkzeug.routing import BaseConverter

from . import utils
from . import cache, socket, app

load_dotenv()
MAX_PLAYERS = int(getenv('REACT_APP_MAX_PLAYERS'))
MAX_NAME_LENGTH = int(getenv('REACT_APP_MAX_NAME_LENGTH'))
GAME_HASH_LENGTH = int(getenv('REACT_APP_GAME_HASH_LENGTH'))
GAME_HASH_REGEX = getenv('REACT_APP_GAME_HASH_REGEX')

main = Blueprint('main', __name__)

class GameHashConverter(BaseConverter):
    regex = f'{GAME_HASH_REGEX}' + '{' + f'{MAX_NAME_LENGTH}' + '}'
app.url_map.converters['game_hash'] = GameHashConverter

# use the converter in the route
@app.route('/<game_hash>')
@main.route('/')
@main.route('/new_game')
@main.route('/join_game')
@main.route('/game')
def serve(game_hash=''):
	"""Serve static files."""
	return send_from_directory(app.static_folder, 'index.html')


@main.route('/create_new_game', methods=['POST'])
def create_new_game():
	"""Create an inactive game that players can join."""
	request_data = request.get_json()
	print(f"/create_new_game request_data: {request_data}")
	player_name = request_data.get('player_name')

	# Only used when starting a new game after a game has ended
	recycled_game = request_data.get('recycled_game')
	game_hash = request_data.get('game_hash')
	player_names = request_data.get('player_names')
	player_colors = request_data.get('player_colors', {})

	if not recycled_game:
		game_hash = utils.get_new_game_hash(GAME_HASH_LENGTH)
		player_names = [player_name]
		player_colors = utils.get_random_color(player_name, player_colors)

	game_data = {
		'active': False,
		'winner': None,
		'num_players': len(player_names),
		'card_deck': None,
		'card_type': None,
		'card_color': None,
		'players': dict([(p, []) for p in player_names]),
		'player_hashes': dict([(p, utils.get_new_player_hash()) for p in player_names]),
		'player_colors': player_colors,
		'player_order': [],
		'player_index': 0,
		'player_increment': 1,
		'current_player': None,
		'draw': None,
	}

	cache.set(game_hash, game_data)

	if recycled_game:
		socket.emit(
			f'{game_hash}_recycled_game',
			{
				'playerNames': player_names,
				'activatedPlayer': player_name,
				'setGameCreator': player_name,
			},
			broadcast=True
		)

	return jsonify({
		'gameHash': game_hash,
		'playerNames': [player_name],
		'playerHash': game_data['player_hashes'][player_name],
		'playerColors': game_data['player_colors'],
	})


@main.route('/add_player', methods=['POST'])
def add_player():
	"""Add a player to a pending game."""
	print('/add_player')
	request_data = request.get_json(force=True)

	# Only used when starting a new game after a game has ended
	recycled_game = request_data.get('recycled_game')
	game_hash = request_data.get('game_hash', '')
	player_name = request_data.get('player_name')

	game_data = cache.get(game_hash)

	if not game_data or game_data['active']:
		return jsonify({
			'error': f'Could not join game using code "{game_hash}". ' +
					  'Either the game code is invalid or the game is already in progress.'
		})
	elif not player_name:
		return jsonify({'error': utils.errors['no_player_name']})
	elif not recycled_game and player_name in game_data['players']:
		if game_data['active']:
			# TODO verify localStorage on client before redirecting
			return jsonify({'redirect': '/game'})
		return jsonify({'error': utils.errors['invalid_value']('name', player_name)})
	elif game_data['num_players'] > MAX_PLAYERS:
		return jsonify({'error': f'Can\'t exceed {MAX_PLAYERS} players.'})

	if len(player_name) > MAX_NAME_LENGTH:
		player_name = player_name[:MAX_NAME_LENGTH]

	player_hash = utils.get_new_player_hash()
	game_data['player_hashes'][player_name] = player_hash

	if not recycled_game:
		# add player with list for storing their cards
		# recycled games already did this in /create_new_game
		game_data['players'][player_name] = []
		game_data['num_players'] += 1
		utils.get_random_color(player_name, game_data['player_colors'])

	cache.set(game_hash, game_data)

	if recycled_game:
		socket.emit(
			f'{game_hash}_recycled_game',
			{
				'playerNames': list(game_data['players'].keys()),
				'activatedPlayer': player_name,
				'playerColors': game_data['player_colors'],
			},
			broadcast=True
		)
	else:
		socket.emit(
			game_hash,
			{
				'playerNames': list(game_data['players'].keys()),
				'playerColors': game_data['player_colors'],
			},
			broadcast=True
		)

	return jsonify({
		'playerNames': list(game_data['players'].keys()),
		'playerColors': game_data['player_colors'],
		'playerHash': player_hash,
	})


@main.route('/start_game', methods=['POST'])
def start_game():
	"""Set game object's active property to true, create card_deck, and deal player cards."""
	print('/start_game')
	request_data = request.get_json()

	game_hash = request_data.get('game_hash')
	# Only used when starting a new game after a game has ended
	recycled_game = request_data.get('recycled_game')

	game_data = cache.get(game_hash)
	if not game_data:
		return jsonify({'error': utils.errors['no_game_data'](game_hash)})

	player_name = request_data.get('player_name')
	if not player_name:
		return jsonify({'error': utils.errors['missing_request_data']('player name')})

	player_hash = request_data.get('player_hash')
	if not player_hash:
		return jsonify({'error': utils.errors['missing_request_data']('player hash')})
	elif player_hash != game_data['player_hashes'][player_name]:
		return jsonify({'error': utils.errors['incorrect_player_hash'](player_hash)})

	if game_data['active']:
		return jsonify({'error': 'Game has already started.'})

	num_players = game_data['num_players']
	if num_players < 2:
		return jsonify({
			'error': 'At least two players must join before game can start.',
			'gameData': game_data,
		})

	players_data = game_data['players']

	game_data['card_deck'] = utils.get_new_deck(size=num_players)
	utils.deal_starter_cards(players_data, game_data['card_deck'])

	game_data['active'] = True
	game_data['player_order'] = utils.draw_play_order_cards(players_data)
	game_data['current_player'] = game_data['player_order'][0][0]

	# [player][card][substring]
	game_data['card_color'] = game_data['player_order'][0][1][0]
	game_data['card_type'] = game_data['player_order'][0][1][1]

	cache.set(game_hash, game_data)
	if recycled_game:
		socket.emit(f'{game_hash}_recycled_game', {'active': True}, broadcast=True)
	else:
		socket.emit(game_hash, {'active': True}, broadcast=True)

	return jsonify({
		'playersData': list(players_data.keys()),
	})


@main.route('/exit', methods=['POST'])
def exit():
	"""Player rejected to rejoin the game, delete them from the
	   game object and broadcast the update to remaining players.
	"""
	request_data = request.get_json()

	game_hash = request_data.get('game_hash')
	player_name = request_data.get('player_name')

	game_data = cache.get(game_hash)
	if not game_data:
		return jsonify({'error': utils.errors['no_game_data'](game_hash)})

	player_hash = request_data.get('player_hash')
	if not player_hash:
		return jsonify({'error': utils.errors['missing_request_data']('player hash')})
	elif player_hash != game_data['player_hashes'][player_name]:
		return jsonify({'error': utils.errors['incorrect_player_hash'](player_hash)})

	players_data = game_data['players']
	if player_name in players_data:
		del players_data[player_name]
		game_data['num_players'] -= 1

	cache.set(game_hash, game_data)

	player_names = list(players_data.keys())

	abort = len(player_names) < 2
	if abort:
		cache.delete(game_hash, game_data)
	else:
		cache.set(game_hash, game_data)


	socket.emit(
		f'{game_hash}_recycled_game',
		{
			'abort': abort,
			'playerNames': player_names,
		},
		broadcast=True
	)

	return jsonify({'message': 'success'})


@main.route('/get_game_data', methods=['GET'])
def get_game_data():
	game_hash = request.args.get('game_hash')
	game_data = cache.get(game_hash)
	if not game_data:
		return jsonify({'error': utils.errors['no_game_data'](game_hash)})

	player_name = request.args.get('player_name')
	players_cards = game_data['players']
	if player_name not in players_cards:
		return jsonify({'error': f'Couldn\'t find data for in player {player}'})

	player_hash = request.args.get('player_hash')
	if not player_hash:
		return jsonify({'error': utils.errors['missing_request_data']('player hash')})
	elif player_hash != game_data['player_hashes'][player_name]:
		return jsonify({'error': utils.errors['incorrect_player_hash'](player_hash)})

	for player in players_cards:
		if player != player_name:
			players_cards[player] = len(players_cards[player]) * ['']
	del game_data['card_deck']
	del game_data['player_hashes']
	return jsonify({'gameData': game_data})


@main.route('/draw_cards', methods=['POST'])
def draw_cards():
	request_data = request.get_json()

	game_hash = request_data.get('game_hash')
	player_name = request_data.get('player_name')
	draw_number = request_data.get('draw_number')

	game_data = cache.get(game_hash)
	if not game_data:
		return jsonify({'error': utils.errors['no_game_data'](game_hash)})

	player_hash = request_data.get('player_hash')
	if not player_hash:
		return jsonify({'error': utils.errors['missing_request_data']('player hash')})
	elif player_hash != game_data['player_hashes'][player_name]:
		return jsonify({'error': utils.errors['incorrect_player_hash'](player_hash)})


	current_player = game_data['current_player']
	if player_name != current_player:
		return jsonify({'error': f'{player_name} can\'t draw cards. Current player is {current_player}'})

	player_cards = game_data['players'][player_name]

	card_deck = game_data['card_deck']

	if not card_deck:
		return jsonify({'error': 'No cards in deck.'})

	utils.draw_cards_from_deck(player_cards, card_deck)

	cache.set(game_hash, game_data)

	socket.emit(
		game_hash,
		{
			'players': game_data['players'],
			'cardType': game_data['card_type'],
			'currentPlayer': game_data['current_player'],
			'drawCount': 1,
		},
		broadcast=True
	)
	return jsonify({
		'myCards': player_cards,
	})


@main.route('/play_card', methods=['POST'])
def play_card():
	"""Update game object's card type and color. Handle
	   check for winner, card draws, and player increment.
	"""
	request_data = request.get_json()
	player_name = request_data.get('player_name')
	game_hash = request_data.get('game_hash')
	card_color = request_data.get('color')
	card_type = request_data.get('type')
	card_index = request_data.get('index')
	card = card_color + card_type

	if not card:
		return jsonify({'error': utils.errors['missing_request_data']('card data')})
	if not utils.validate_card(card):
		return jsonify({'error': utils.errors['invalid_value']('card', card)})

	game_data = cache.get(game_hash)
	if not game_data:
		return jsonify({'error': utils.errors['no_game_data'](game_hash)})

	player_hash = request_data.get('player_hash')
	if not player_hash:
		return jsonify({'error': utils.errors['missing_request_data']('player hash')})
	elif player_hash != game_data['player_hashes'][player_name]:
		return jsonify({'error': utils.errors['incorrect_player_hash'](player_hash)})

	current_player = game_data['current_player']
	if player_name != current_player:
		return jsonify({'error': f'{player_name} can\'t play, current player is {current_player}'})

	player_cards = game_data['players'][player_name]
	if card not in player_cards:
		return jsonify({'error': f'{player_name} doesn\'t have {card} in {player_cards}"'})

	if player_cards[card_index] != card:
		return jsonify({
			'error': f"Unable to find {card} at index {card_index}. Found {player_cards[card_index]} instead."
		})

	card_data = utils.get_card_data(card)

	if card_color != 'w' and not (
		card_color == game_data['card_color'] or
		card_type == game_data['card_type']
	):
		return jsonify({
			'error': f"Unable to play {card} following {game_data['card_color']}{game_data['card_type']}"
		})

	game_data['card_color'] = card_color
	game_data['card_type'] = card_type

	if 'wild' in card_data:
		if 'draw' not in card_data:
			game_data['card_type'] = card_color
	elif 'color' in card_data:
		game_data['card_color'] = card_data['color']
		if 'action' in card_data:
			# draw 2 handled above
			game_data['card_type'] = card_data['action']
			if card_data['action'] == 's' or (card_data['action'] == 'r' and game_data['num_players'] == 2):
				utils.increment_player_index(game_data)
			elif card_data['action'] == 'r':
				game_data['player_increment'] *= -1
		elif 'number' in card_data:
			game_data['card_type'] = card_data['number']
	else:
		return jsonify({'error': utils.errors['invalid_value']('card data', card)})

	draw_count = card_data.get('draw', 0)
	if 'wild' in card_data:
		# handle draw 2/4
		if 'draw' in card_data:
			game_data['draw'] = card_data['draw']
	else:
		utils.increment_player_index(game_data)
		if 'draw' in card_data:
			draw_target_player_cards = game_data['players'][game_data['current_player']]
			utils.draw_cards_from_deck(
				draw_target_player_cards,
				game_data['card_deck'],
				card_data['draw']
			)

	# remove card from player cards
	del player_cards[card_index]
	if not len(player_cards):
		game_data['active'] = False
		game_data['winner'] = player_name

	player_has_uno = player_name if len(player_cards) == 1 else None

	cache.set(game_hash, game_data)

	socket.emit(
		game_hash,
		{
			'cardType': game_data['card_type'],
			'cardColor': game_data['card_color'],
			'currentPlayer': game_data['current_player'],
			'players': game_data['players'],
			'active': game_data['active'],
			'winner': game_data['winner'],
			'increment': game_data['player_increment'],
			'drawCount': draw_count,
			'playerHasUno': player_has_uno,
		},
		broadcast=True
	)

	return jsonify({
		'success': f"{game_data['card_type']} {game_data['card_color']}",
		'myCards': player_cards,
		'cardType': game_data['card_type'],
		'cardColor': game_data['card_color'],
	})


@main.route('/set_color', methods=['POST'])
def set_color():
	"""Set color from player's wild card choice."""
	request_data = request.get_json()

	game_hash = request_data.get('game_hash')

	game_data = cache.get(game_hash)
	if not game_data:
		return jsonify({'error': utils.errors['no_game_data'](game_hash)})

	player_name = request_data.get('player_name')
	if player_name != game_data['current_player']:
		return jsonify({'error': f"Not {player_name}'s turn"})

	player_hash = request_data.get('player_hash')
	if not player_hash:
		return jsonify({'error': utils.errors['missing_request_data']('player hash')})
	elif player_hash != game_data['player_hashes'][player_name]:
		return jsonify({'error': utils.errors['incorrect_player_hash'](player_hash)})

	if game_data['card_color'] != 'w':
		return jsonify({'error': 'Not wild card'})

	color = request_data.get('color')
	if not utils.validate_color(color):
		return jsonify({'error': utils.errors['invalid_value']('color', color)})

	game_data['card_color'] = color

	utils.increment_player_index(game_data)
	if game_data['draw']:
		draw_target_player_cards = game_data['players'][game_data['current_player']]
		utils.draw_cards_from_deck(
			draw_target_player_cards,
			game_data['card_deck'],
			game_data['draw']
		)
		game_data['card_type'] = ''
		game_data['draw'] = None

	cache.set(game_hash, game_data)

	socket.emit(
		game_hash,
		{
			'currentPlayer': game_data['current_player'],
			'cardColor': game_data['card_color'],
			'cardType': game_data['card_type'],
			'players': game_data['players'],
			'playerName': player_name,
		},
		broadcast=True
	)
	return jsonify({'success': f'Set color to {color}.'})


@main.route('/sort_cards', methods=['POST'])
def sort_cards():
	"""Sort the player's cards by type and color"""
	request_data = request.get_json()

	game_hash = request_data.get('game_hash')

	game_data = cache.get(game_hash)
	if not game_data:
		return jsonify({'error': utils.errors['no_game_data'](game_hash)})

	player_name = request_data.get('player_name')
	if not player_name:
		return jsonify({'error': utils.errors['missing_request_data']('player name')})

	player_hash = request_data.get('player_hash')
	if not player_hash:
		return jsonify({'error': utils.errors['missing_request_data']('player hash')})
	elif player_hash != game_data['player_hashes'][player_name]:
		return jsonify({'error': utils.errors['incorrect_player_hash'](player_hash)})

	player_cards = game_data['players'][player_name]
	player_cards = utils.sort_cards_by_type_and_color(player_cards)
	game_data['players'][player_name] = player_cards
	cache.set(game_hash, game_data)

	return jsonify({'myCards': player_cards})

