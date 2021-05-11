import pygame

pygame.font.init()

myfont = pygame.font.SysFont('Arial', 30)

class Player:
	def __init__(self, wallet=500, owned=10):
		self.wallet = wallet
		self.owned = owned

	def draw(self, win):
		# textsurface = myfont.render(f'Wallet: {self.wallet}\nOwned: {self.owned}', False, (0, 0, 0))

		# win.blit(textsurface, (0, 200))

		pass

	# def move(self):
	# 	keys = pygame.key.get_pressed()

	# 	if (keys[pygame.K_w]):
	# 		self.y -= self.velocity
	# 	if (keys[pygame.K_a]):
	# 		self.x -= self.velocity
	# 	if (keys[pygame.K_s]):
	# 		self.y += self.velocity
	# 	if (keys[pygame.K_d]):
	# 		self.x += self.velocity
