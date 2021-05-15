from player import Player

import secrets
from string import ascii_uppercase, digits

class Order:
	def __init__(self, player: Player, order: int, code: str):
		self.player = player
		self.order = order
		self.code = code # BUG: does server or client generate code
		self.iplayer = self.player.iplayer

class Join:
	def __init__(self, code: str):
		self.code = code

class Start:
	def __init__(self):
		self.code = Start.generate_code(8)

	@staticmethod
	def generate_code(length: int) -> str:
		sample = ascii_uppercase + digits
		rand = ''.join([secrets.choice(sample) for _ in range(length)])

		return rand
