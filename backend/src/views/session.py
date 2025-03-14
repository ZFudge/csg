from os import getenv

from dotenv import load_dotenv

from flask import Blueprint, jsonify, request

from app import cache, socket
import utils

load_dotenv()
MAX_PLAYERS = int(getenv('REACT_APP_MAX_PLAYERS') or 6)
MAX_NAME_LENGTH = int(getenv('REACT_APP_MAX_NAME_LENGTH') or 10)
GAME_HASH_LENGTH = int(getenv('REACT_APP_GAME_HASH_LENGTH') or 8)

session = Blueprint('session', __name__)


@session.route('/create_new_game', methods=['POST'])
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


@session.route('/add_player', methods=['POST'])
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


@session.route('/start_game', methods=['POST'])
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


@session.route('/exit', methods=['POST'])
def exit():
	"""Player rejected to rejoin the game, delete them from the
	   game object and broadcast the update to resessioning players.
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
