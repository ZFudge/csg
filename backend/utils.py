import base64
import hashlib
import random
import time

import deck


player_colors = [
	'#2299ce',	# turquoise
	'#01af6e',	# green cyan
	'#880202',	# dark red
	'#9c00ff',	# purple
	'#dd139f',	# pink
	'#f47e01',	# orange
]

def get_random_color(player_name, color_dict):
	random_color = random.choice([c for c in player_colors if c not in [v for k,v in color_dict.items()]])
	color_dict[player_name] = random_color
	return color_dict


def get_new_hash(input_value: int) -> str:
	input_value_bytes = str(time.time()).encode()
	hashed_input_value = hashlib.sha224(input_value_bytes).hexdigest().encode("ascii")
	encoded_hashed_input_value = base64.b64encode(hashed_input_value).decode()
	return encoded_hashed_input_value


def get_new_game_hash(game_hash_length):
	encoded_hashed_ts = get_new_hash(time.time())
	return encoded_hashed_ts[:game_hash_length]


def get_new_player_hash():
	encoded_hashed_ts = get_new_hash(time.time() / random.random())
	return encoded_hashed_ts[:5]


def get_new_deck(size=2):
	return deck.get_shuffled_deck(size)


def deal_starter_cards(players, card_deck):
	number_of_cards = 7
	for player in players:
		players[player] += card_deck[-number_of_cards:]
		del card_deck[-number_of_cards:]


def draw_play_order_cards(players):
	''' Determines what order players will play in '''
	player_order = []
	for player in players:
		player_order.append([
			player,
			deck.get_random_numeric_card()
		])
	# sort list by card number
	return sorted(
		player_order,
		key=lambda x: x[1][1],
		reverse=True
	)


def validate_card(card):
	return deck.validate_card(card)


def get_card_data(card):
	color = card[0]
	card_type = card[1:]
	card_data = {
		'color': color,
		'card_type': card_type,
	}

	if color == 'w':
		card_data['wild'] = True
		if card_type:
			card_data['draw'] = int(card_type[-1])
		return card_data

	if deck.is_action(card_type):
		card_data['action'] = card_type
		if card_type in ['+4', '+2']:
			card_data['draw'] = deck.get_draw_value(card_type)
			return card_data

	card_data['number'] = card_type
	return card_data


def increment_player_index(game_data):
	player_index = game_data['player_index']
	num_players = game_data['num_players']
	player_increment = game_data['player_increment']
	player_index += player_increment
	if player_index < 0:
		player_index = num_players - 1
	elif player_index >= num_players:
		player_index = 0
	game_data['player_index'] = player_index
	game_data['current_player'] = game_data['player_order'][player_index][0]


def validate_color(color):
	return deck.validate_color(color)


def draw_cards_from_deck(player_cards, card_deck, draw_number=0):
	if draw_number:
		# allow card_deck len check on each card draw to avoid index errors
		for x in range(draw_number):
			player_cards.append(card_deck.pop())
			if not card_deck:
				# augmented assignment operator to update list by reference/avoid local overwrite
				card_deck += get_new_deck()
	else:
		player_cards.append(card_deck.pop())
		if not card_deck:
			card_deck += get_new_deck()


def sort_cards_by_type_and_color(cards):
	color_order = 'rgbyw'
	return sorted(
		sorted(
			cards,
			# sort by type
			key=lambda x: x[0] if len(x) < 2 else x[1],
		),
		# sort by color
		key=lambda x: color_order.index(x[0]),
	)


errors = {
	'no_game_data': lambda game_hash: f'Cannot retrieve game data for {game_hash}.',
	'incorrect_player_hash': lambda player_hash: f'Incorrect player hash received: {player_hash}.',
	'missing_request_data': lambda value: f'No {value} found in request data.',
	'invalid_value': lambda x, y: f'Invalid {x}, "{y}".',
}

