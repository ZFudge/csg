from os import environ, system
from sys import exit
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def set_port():
	available_ports = [
		3075,	# node server
		5075	# flask server
	]
	for port in available_ports:
		print(f'Checking port: {port}')
		if system(f'curl -I http://localhost:{port}/') == 0:
			return port
	print(f'No usable ports. Exitting...')
	exit()

PORT = set_port()


DRIVER_PATH = environ['HOME'] + '/Downloads/chromedriver'
BRAVE_BINARY_LOCATION = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'

WINDOW_SIZE_WH = 'window-size=500,700'
WINDOW_POSITIONS_XY = (
	(250, 0),
	(750, 0)
)
STEP_SPEED = 0.5

# each driver instance represents a browser window
all_drivers = []

def run_method_on_all_drivers(method):
	for driver in all_drivers:
		getattr(driver, method)()

def _close_on_failure(method):
	"""class method decorator for closing the browsers between Exception and raise statement"""
	def run(self, *args, **kwargs):
		try:
			method(self)
		except Exception as e:
			run_method_on_all_drivers('close_and_quit')
			raise e
	return run


class Driver(object):
	"""Webdriver that takes on the role of an individual game player"""
	host = f'http://localhost:{PORT}/'
	game_hash = ''

	def __init__(self, player_name, driver_path, binary_location=None, position=(0, 0), options=[]):
		self.player_name = player_name
		driver_options = webdriver.ChromeOptions()
		if binary_location:
			driver_options.binary_location = binary_location
		for option in options:
			driver_options.add_argument(option)
		# driver_path passed to constructor to allow use of separate browsers
		self.driver = webdriver.Chrome(executable_path=driver_path, options=driver_options)
		[x, y] = position
		self.driver.set_window_position(x, y, windowHandle='current')
		all_drivers.append(self)

	def close_and_quit(self):
		print('close_and_quit')
		self.driver.close()
		self.driver.quit()

	@_close_on_failure
	def open_app(self):
		self.driver.get(self.host)
		print(f'self.driver.current_url: {self.driver.current_url} == Driver.host: {Driver.host}')
		assert self.driver.current_url == Driver.host

	@_close_on_failure
	def create_new_game(self):
		print('create_new_game')
		new_game_link = self.driver.find_element_by_name('new-game')
		new_game_link.click()

		print(self.driver.current_url)
		assert self.driver.current_url == Driver.host + 'new'
		name_input = self.driver.find_element_by_name('player-name')
		name_input.send_keys(self.player_name)
		sleep(STEP_SPEED)
		create_game_button = self.driver.find_element_by_name('create-game')
		create_game_button.click()

		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "game-hash-container")))
		game_hash = self.driver.find_element_by_id('game-hash').text
		assert len(game_hash) == 8
		Driver.game_hash = game_hash

	@_close_on_failure
	def join_game(self):
		print('join_game')
		join_button = self.driver.find_element_by_name('join-game')
		join_button.click()
		sleep(STEP_SPEED)
		assert self.driver.current_url == Driver.host + 'join'
		game_hash_input = self.driver.find_element_by_name('game-hash')
		game_hash_input.send_keys(Driver.game_hash)
		sleep(STEP_SPEED)
		name_input = self.driver.find_element_by_name('player-name')
		name_input.send_keys(self.player_name)
		sleep(STEP_SPEED)
		join_button = self.driver.find_element_by_name('join-game')
		join_button.click()
		sleep(STEP_SPEED)

	@_close_on_failure
	def start_game(self):
		print('start_game')
		player_names = self.driver.find_elements_by_class_name('joined-player-name')
		print(f'len(player_names): {len(player_names)} == len(all_drivers): {len(all_drivers)}')
		assert len(all_drivers) == len(player_names)
		start_button = self.driver.find_element_by_name('start-game')
		start_button.click()
		sleep(STEP_SPEED)

	@_close_on_failure
	def validate_in_game(self):
		print('validate_in_game')
		assert self.driver.current_url == Driver.host + 'game'


def main():
	primary_driver = Driver(
		'Primary',
		DRIVER_PATH,
		binary_location=BRAVE_BINARY_LOCATION,
		position=WINDOW_POSITIONS_XY[0],
		options=(WINDOW_SIZE_WH,)
	)
	secondary_driver = Driver(
		'Secondary',
		DRIVER_PATH,
		binary_location=BRAVE_BINARY_LOCATION,
		position=WINDOW_POSITIONS_XY[1],
		options=(WINDOW_SIZE_WH, '--incognito')
	)

	run_method_on_all_drivers('open_app')
	primary_driver.create_new_game()
	secondary_driver.join_game()
	primary_driver.start_game()
	run_method_on_all_drivers('validate_in_game')
	sleep(STEP_SPEED)
	run_method_on_all_drivers('close_and_quit')


if __name__ == '__main__':
	main()
