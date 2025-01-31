from random import shuffle, random

# The deck consists of 108 cards:
# four each of "Wild" and "Wild Draw Four," and
# 25 each of four different colors (red, yellow, green, blue).
# Each color consists of one zero, two each of 1 through 9, and
# two each of "Skip," "Draw Two," and "Reverse."
# These last three types are known as "action cards."

colors = ['r', 'g', 'b', 'y']
actions = ['s', '+2', 'r']
draws_type_values = {
	'+4': 4,
	'+2': 2,
}

deck = []
deck += ['w'] * 4
deck += ['w+4'] * 4

for color in colors:
	deck += [f'{color}0']
	for n in range(1, 10):
		deck += [f'{color}{n}'] * 2
	for action in actions:
		deck += [f'{color}{action}'] * 2


def get_shuffled_deck(size):
	unshuffled_deck = deck * size
	shuffle(unshuffled_deck)
	return unshuffled_deck


def get_random_numeric_card():
	number = str(round(random() * 9))
	color = colors[round(random() * 3)]
	return color + number


def validate_card(card):
	return card in deck


def is_action(value):
	return value in actions


def get_draw_value(draw_type):
	return draws_type_values[draw_type]


def validate_color(color):
	return color in colors

