from player import Player
from client import RED, GREEN, WHITE

import socket
from _thread import *

import pickle
from collections import deque as queue

class Game:
	def __init__(self, players=[], price=100, pendingbuys=queue(), pendingsells=queue()):
		self.price = price
		self.players = players
		self.pendingbuys = pendingbuys
		self.pendingsells = pendingsells
