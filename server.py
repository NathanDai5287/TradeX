from player import Player
from client import RED, GREEN, WHITE

import socket
from _thread import *

import pickle
from collections import deque as queue

server = '172.28.128.1'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.bind((server, port))
except socket.error as e:
	print(e)

s.listen(2)

print('Waiting for a connection; Server Started')

# players = [Player(), Player()]
players = []
price = 100
pendingbuys = queue()
pendingsells = queue()

def threaded_client(connection, iplayer):
	global price

	connection.send(pickle.dumps(players[iplayer]))

	reply = ''
	while (True):
		try:
			data = pickle.loads(connection.recv(2048)) # Order
		except:
			print('Lost Connection')
			connection.close() # BUG: this may lose track of which player is which
			# players.pop(iplayer)

		# print(data)
		# players[player] = data

		if (not(data)):
			print('Disconnected')
			break

		if (data.order == 1):
			if (pendingsells):
				sell = pendingsells.popleft()

				players[iplayer].owned += 1
				sell.owned -= 1

				players[iplayer].wallet -= price
				sell.wallet += price
			else:
				pendingbuys.append(players[iplayer])
				price *= 1.0001

		elif (data.order == -1):
			if (pendingbuys):
				buy = pendingbuys.popleft()

				players[iplayer].owned -= 1
				# players[iplayer].owned += 1
				buy.owned += 1

				# players[iplayer].wallet += price
				players[iplayer].wallet += price
				buy.wallet -= price
			else:
				pendingsells.append(players[iplayer])
				price *= 0.9999
		else:
			buy = bool(pendingbuys)
			sell = bool(pendingsells)

			if (buy and not sell): # TODO: make change based on the numbmer of orders open
				price *= 1.0001
			elif (sell and not buy):
				price *= 0.9999

		reply = players[iplayer], price
		# reply = 1, 2

		print('Received: ', data)
		print('Sending: ', reply)

		# connection.sendall(pickle.dumps(reply))
		try:
			print(iplayer)
			connection.sendall(pickle.dumps((players[iplayer], price)))
		# except IndexError:
		except:
			print(iplayer)
		# except:
			# print('Error in threaded client')

	print('Lost Connection')
	connection.close()

nplayers = 0
while (True):
	connection, address = s.accept()

	print('Connected to: ', address)
	players.append(Player())

	start_new_thread(threaded_client, (connection, nplayers))
	nplayers += 1
