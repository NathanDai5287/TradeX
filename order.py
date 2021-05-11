from player import Player

class Order:
	def __init__(self, player: Player, order: int):
		self.player = player
		self.order = order
