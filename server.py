from player import Player
from order import Join, Order, Start
from game import Game
from client import RED, GREEN, WHITE

import socket
from _thread import *

import pickle
from collections import deque as queue
from uuid import uuid4
import copy

# server = '172.28.128.1'
# server = '0.0.0.0'
# server = '172.22.192.1'
# server = '255.255.255.0'
server = '10.0.0.10'
# server = '151'

port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.bind((server, port))
except socket.error as e:
	print(e)

s.listen(5)

print('Waiting for a connection; Server Started')

games = {}

def threaded_client(connection):
	# if (code in games):
		# game = games[code]
	# else:
		# games[code] = Game()

	# game = games[1111]

	# connection.send(pickle.dumps(game.players[iplayer]))
	connection.send(pickle.dumps(True))

	while (True):
		try:
			data = pickle.loads(connection.recv(2048)) # Order
		except:
			# print('Lost Connection')
			connection.close()
			break

		if (not(data)):
			print('Disconnected')
			break

		category = type(data)

		if (category == Start):
			game = Game()
			games[data.code] = copy.deepcopy(game)

			player = Player()
			player.iplayer = 0
			games[data.code].players.append(player)

			connection.send(pickle.dumps((games[data.code].players[-1], games[data.code].price)))

		elif (category == Join):

			if (data.code in games):
				game = games[data.code]

				player = Player()
				player.iplayer = len(games[data.code].players)
				games[data.code].players.append(player) # TODO: somehow keep track of iplayer

				connection.send(pickle.dumps((games[data.code].players[-1], games[data.code].price)))
			else:
				connection.send(pickle.dumps((False, False)))


		elif (category == Order):
			game = games[data.code] # TODO: client should send iplayer data
			# player = game.players[iplayer]
			player = game.players[data.player.iplayer] # TEMP

			if (data.order == 1):
				if (game.pendingsells):
					seller = game.pendingsells.popleft()
					player.buy(seller, game.price)
				else:
					game.pendingbuys.append(player)

			elif (data.order == -1):
				if (game.pendingbuys):
					buyer = game.pendingbuys.popleft()
					buyer.buy(player, game.price)
				else:
					game.pendingsells.append(player)

			nbuyers = len(game.pendingbuys)
			nsellers = len(game.pendingsells)

			change = 1 + 0.0001 * (nbuyers - nsellers)
			game.price *= change # BUG: the price is changing in all lobbies

			try:
				connection.send(pickle.dumps((player, game.price)))
			except:
				# print(iplayer)
				pass

	print('Lost Connection')
	connection.close()

nplayers = 0
while (True):
	connection, address = s.accept()

	print('Connected to: ', address)
	# games[random_code(address)].players.append(Player())

	start_new_thread(threaded_client, (connection,))
	# nplayers += 1
