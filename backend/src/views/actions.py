from flask import Blueprint, jsonify, request

from app import cache, socket
import utils


misc = Blueprint('misc', __name__)


@misc.route('/set_color', methods=['POST'])
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
	)
	return jsonify({'success': f'Set color to {color}.'})


@misc.route('/sort_cards', methods=['POST'])
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


@misc.route('/draw_cards', methods=['POST'])
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
	)
	return jsonify({
		'myCards': player_cards,
	})
