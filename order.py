from player import Player

class Order:
	def __init__(self, player: Player, order: int, code: str):
		self.player = player
		self.order = order
		self.code = int(code)
		self.iplayer = self.player.iplayer

class Join:
	def __init__(self, code: str):
		self.code = int(code)
