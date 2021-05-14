from __future__ import annotations

import pygame

pygame.font.init()

myfont = pygame.font.SysFont('Arial', 30)

class Player:
	def __init__(self, wallet=500, owned=10):
		self.wallet = wallet
		self.owned = owned
		self.iplayer = None

	def buy(self, seller: Player, price: float):
		self.owned += 1
		self.wallet -= price

		seller.owned -= 1
		seller.wallet += price
