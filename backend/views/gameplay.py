from flask import Blueprint, jsonify, request

from csg import cache, socket, utils


gameplay = Blueprint('gameplay', __name__)


@gameplay.route('/get_game_data', methods=['GET'])
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


@gameplay.route('/play_card', methods=['POST'])
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
			if card_data['action'] == 's' or (
				card_data['action'] == 'r' and game_data['num_players'] == 2
			):
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

	player_has_one_card_remaining = player_name if len(player_cards) == 1 else None

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
			'playerHasOneCardRemaining': player_has_one_card_remaining,
		},
		broadcast=True
	)

	return jsonify({
		'success': f"{game_data['card_type']} {game_data['card_color']}",
		'myCards': player_cards,
		'cardType': game_data['card_type'],
		'cardColor': game_data['card_color'],
	})
