from flask import request, jsonify

from src import cache, utils


def get_game_data(game_hash: str, player_name: str, player_hash: str):
	game_hash = request.args.get('game_hash')
	game = cache.get(game_hash)

	if not game:
		return jsonify({'error': utils.errors['no_game_data'](game_hash)})

	player_name = request.args.get('player_name')
	players_cards = game['players']
	if player_name not in players_cards:
		return jsonify({'error': f'Couldn\'t find data for in player {player}'})

	player_hash = request.args.get('player_hash')
	if not player_hash:
		return jsonify({'error': utils.errors['missing_request_data']('player hash')})
	elif player_hash != game['player_hashes'][player_name]:
		return jsonify({'error': utils.errors['incorrect_player_hash'](player_hash)})

	for player in players_cards:
		if player != player_name:
			players_cards[player] = len(players_cards[player]) * ['']
	del game['card_deck']
	del game['player_hashes']
	return jsonify({'gameData': game})

def play_card(*args, **kwargs):
	player_name = kwargs.get('player_name')
	game_hash = kwargs.get('game_hash')
	card_color = kwargs.get('color')
	card_type = kwargs.get('type')
	card_index = kwargs.get('index')
	card = card_color + card_type

	game = cache.get(game_hash)

	if not game:
		return jsonify({'error': utils.errors['no_game_data'](game_hash)})

	player = game['players'][player_name]
	if not player:
		return jsonify({'error': utils.errors['no_player_data'](player_name)})

	player_hash = kwargs.get('player_hash')
	if not player_hash:
		return jsonify({'error': utils.errors['missing_request_data']('player hash')})
	elif player_hash != game['player_hashes'][player_name]:
		return jsonify({'error': utils.errors['incorrect_player_hash'](player_hash)})

	game['players'][player_name].play_card(card_type, card_color)
