from network import Network
from player import Player
from order import Order, Join, Start

import pygame
from pygame_button import Button

WIDTH = 500
HEIGHT = 500

CAPTION = 'TradeX'

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
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

HOME = {
	'hover_color': LIGHT_GREY,
	'clicked_color': DARK_GREY,
	'clicked_font_color': BLACK,
	'hover_font_color': BLACK,
	'font_color': BLACK,
}

n = Network()

# TODO: make these Player methods rather than functions
def join(code: str):
	global menu
	global n
	global p
	global display_invalid

	# p.join(code)
	# TODO: make player join private lobby

	player, price = n.send(Join(code))

	p = player
	display_invalid = not(bool(player))

	if (not(display_invalid)):
		menu = False
	else:
		menu = True

	return player

def create():
	global menu
	global n
	global p
	global joined_code
	global joined

	menu = False
	# print('created')

	start = Start()
	p, price = n.send(start)
	joined_code = start.code
	joined = True

font = pygame.font.Font(None, 30)

def redraw(win: pygame.Surface, player: Player, price: int, code: str):
	win.fill(WHITE)

	price_surface = font.render('{:.2f}'.format(price), 1, BLACK)
	wallet_surface = font.render('Wallet: ' + '{:.2f}'.format(player.wallet), 1, BLACK)
	portfolio_surface = font.render('Owned: ' + str(player.owned), 1, BLACK)
	total_surface = font.render('Net Value: ' + '{:.2f}'.format(player.wallet + player.owned * price), 1, BLACK)

	draw_code(win, code)

	win.blit(price_surface, (75, 200))
	win.blit(wallet_surface, (250, 200))
	win.blit(portfolio_surface, (250, 250))
	win.blit(total_surface, (250, 150))

def redraw_home(win: pygame.Surface, code: str, color: tuple, input_rect: pygame.Rect, go: Button, lobby: Button):
	win.fill(WHITE)

	pygame.draw.rect(win, color, input_rect)
	code_surface = font.render(code, True, BLACK)
	win.blit(code_surface, (input_rect.x + 5, input_rect.y + 5))

	go.update(win)
	lobby.update(win)
	input_rect.w = max(150, code_surface.get_width() + 10)

	# pygame.display.flip()

def draw_invalid(win: pygame.Surface, draw: bool):
	if (draw):
		text_surface = font.render('Code not valid', True, BLACK)
		win.blit(text_surface, (150, 430))
	else:
		# pygame.draw.rect(150, 420, 150, 25)
		pygame.draw.rect(win, WHITE, pygame.Rect(150, 430, 150, 25))

	# pygame.display.flip()

def draw_code(win: pygame.Surface, code: str):
	code_surface = font.render(f'Code: {code}', True, BLACK)
	win.blit(code_surface, (300, 450))

menu = True
def main():
	global p
	global display_invalid
	global menu
	global joined

	run = True

	# if (p is None):
		# raise Exception('Server is not running')

	price = 100

	clock = pygame.time.Clock()



	input_rect = pygame.Rect(150, 400, 150, 25)
	code = ''
	active = False
	display_invalid = False
	joined = False

	new_lobby = Button(
		(150, 360, 175, 25), LIGHT_GREY, lambda: create(), text='Create Private Lobby', **HOME
	)

	go = Button(
		(300, 400, 25, 25), LIGHT_GREY, lambda: join(code), text='GO', **HOME
	)

	while (menu):
		clock.tick(60)

		win.fill(WHITE)

		for event in pygame.event.get():
			keys = pygame.key.get_pressed()

			go.check_event(event)
			new_lobby.check_event(event)

			if (joined):
				break

			if (event.type == pygame.QUIT):
				pygame.quit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				display_invalid = False

				if input_rect.collidepoint(event.pos):
					active = True
				else:
					active = False

			if (active and event.type == pygame.KEYDOWN):
				if (keys[pygame.K_BACKSPACE]):
					if (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
						code = ''.join(code.split()[:-1]) # OPTIMIZE
					else:
						code = code[:-1] # OPTIMIZE

				else:
					if (len(code) < 8):
						code += event.unicode.upper()

		if (active):
			color = DARK_GREY
		else:
			color = LIGHT_GREY

		redraw_home(win, code, color, input_rect, go, new_lobby)

		if (display_invalid):
			draw_invalid(win, True)
		else:
			draw_invalid(win, False)

		pygame.display.update()

	#####################################################################

	buy = Button(
		(0, 0, 100, 50), LIGHT_GREEN, lambda: n.send(Order(p, 1, code)), text='Buy', **BUY
	)
	sell = Button(
		(150, 0, 100, 50), LIGHT_RED, lambda: n.send(Order(p, -1, code)), text='Sell', **SELL
	)

	try:
		code = joined_code
	except NameError:
		pass

	while (run): # TODO: displaye game code in bottom right
		clock.tick(60)

		p, price = n.send(Order(p, 0, code=code))

		# TODO: alert user that the code is invalid here

		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				run = False
				pygame.quit()

			buy.check_event(event)
			sell.check_event(event)


		redraw(win, p, price, code)

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
