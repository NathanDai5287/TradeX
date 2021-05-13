from player import Player
from client import RED, GREEN, WHITE

import socket
from _thread import *

import pickle
from collections import deque as queue

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

players = []
price = 100
pendingbuys = queue()
pendingsells = queue()

def threaded_client(connection, iplayer):
	global price

	connection.send(pickle.dumps(players[iplayer]))

	player = players[iplayer]
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

		if (data.order == 1):
			if (pendingsells):
				seller = pendingsells.popleft()
				player.buy(seller, price)
			else:
				pendingbuys.append(player)

		elif (data.order == -1):
			if (pendingbuys):
				buyer = pendingbuys.popleft()
				buyer.buy(player, price)
			else:
				pendingsells.append(player)

		nbuyers = len(pendingbuys)
		nsellers = len(pendingsells)

		change = 1 + 0.0001 * (nbuyers - nsellers)
		price *= change

		try:
			connection.sendall(pickle.dumps((player, price)))
		except:
			print(iplayer)

	print('Lost Connection')
	connection.close()

nplayers = 0
while (True):
	connection, address = s.accept()

	print('Connected to: ', address)
	players.append(Player())

	start_new_thread(threaded_client, (connection, nplayers))
	nplayers += 1
