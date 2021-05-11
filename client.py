from network import Network
from player import Player
from order import Order

import pygame
from pygame_button import Button

WIDTH = 500
HEIGHT = 500

CAPTION = 'TradeX'

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


LIGHT_GREEN = (100, 255,100)
LIGHT_RED = (255,102,102)
LIGHT_GREY = (204,204,204)
DARK_GREY = (130,130,130)

BUY = {
	'hover_color': LIGHT_GREEN,
	'clicked_color': GREEN,
	'clicked_font_color': BLACK,
	'hover_font_color': BLACK,
	'font_color': BLACK,
}

SELL = {
	'hover_color': LIGHT_RED,
	'clicked_color': RED,
	'clicked_font_color': BLACK,
	'hover_font_color': BLACK,
	'font_color': BLACK,
}

PRICE = {
	'hover_color': LIGHT_GREY,
	'clicked_color': DARK_GREY,
	'clicked_font_color': BLACK,
	'hover_font_color': BLACK,
	'font_color': BLACK,
}

def redraw(win: pygame.Surface, player: Player, price: int):
	win.fill(WHITE)
	player.draw(win)

	font = pygame.font.Font(None, 30)

	label_surface = font.render(str(round(price, 2)), 1, BLACK)

	wallet_surface = font.render('Wallet: ' + str(round(player.wallet, 2)), 1, BLACK)
	portfolio_surface = font.render('Owned: ' + str(player.owned), 1, BLACK)

	win.blit(label_surface, (75, 300))
	win.blit(wallet_surface, (250, 200))
	win.blit(portfolio_surface, (250, 250))

def main():
	run = True

	n = Network()
	p = n.get_p()
	price = 100

	clock = pygame.time.Clock()

	buy = Button(
		(0, 0, 100, 50), LIGHT_GREEN, lambda: n.send(Order(p, 1)), text='Buy', **BUY
	)
	sell = Button(
		(150, 0, 100, 50), LIGHT_RED, lambda: n.send(Order(p, -1)), text='Sell', **SELL
	)


	while (run):
		clock.tick(60)

		p, price = n.send(Order(p, 0))
		# print(price)

		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				run = False
				pygame.quit()

			buy.check_event(event)
			sell.check_event(event)


		redraw(win, p, price)

		buy.update(win)
		sell.update(win)

		pygame.display.update()

		# p.move()
		# redraw(win, p)

if __name__ == "__main__":
	win = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption(CAPTION)

	nclients = 0

	main()
