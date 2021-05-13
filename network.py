import pickle

import socket

class Network:
	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# self.server = '172.28.128.1'
		self.server = '10.0.0.10'
		self.port = 5555
		self.address = (self.server, self.port)

		self.p = self.connect() # TODO: this is what information will be sent to the server

	def get_p(self):
		return self.p

	def connect(self):
		try:
			self.client.connect(self.address)
			return pickle.loads(self.client.recv(2048))
		except:
			pass

	def send(self, data):
		try:
			self.client.send(pickle.dumps(data))
			return pickle.loads(self.client.recv(2048))
		except socket.error as e:
			print(e)
