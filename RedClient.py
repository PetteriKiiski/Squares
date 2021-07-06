import socket, pygame, pickle, struct, sys, os
from pygame.locals import *
pygame.init()
canvas = pygame.display.set_mode((500, 500))
Address = ("10.0.0.147", 9653)
def main():
	Waiting = pygame.image.load("Waiting.png")
	mycolor = (255, 0, 0)
	handle_request("SET_ONLINE", (255, 0, 0), True)
	if not handle_request("GET_ONLINE", (0, 255, 0)):
		canvas.blit(Waiting, (0, 0))
		pygame.display.update()
		while not handle_request("GET_ONLINE", (0, 255, 0)):
			for event in pygame.event.get():
				if event.type == QUIT:
					handle_request("SET_ONLINE", (255, 0, 0), False)
					pygame.quit()
					sys.exit()
	while True:
		canvas.fill((255, 255, 255))
		handle_request("SET_ONLINE", (0, 255, 0), True)
		handle_request("CHANGE_LOCATION", (255, 0, 0), pygame.mouse.get_pos())
		position2 = handle_request("GET_POSITION", (0, 255, 0))
		pygame.draw.rect(canvas, (0, 255, 0), pygame.Rect(position2[0]-25, position2[1]-25, 50, 50))
		pygame.draw.rect(canvas, (255, 0, 0), pygame.Rect(pygame.mouse.get_pos()[0]-25, pygame.mouse.get_pos()[1]-25, 50, 50))
		if not handle_request("GET_ONLINE", (0, 255, 0)):
			canvas.blit(Waiting, (0, 0))
			pygame.display.update()
			while not handle_request("GET_ONLINE", (0, 255, 0)):
				for event in pygame.event.get():
					if event.type == QUIT:
						handle_request("SET_ONLINE", (255, 0, 0), False)
						pygame.quit()
						sys.exit()
		for event in pygame.event.get():
			if event.type == QUIT:
				handle_request("SET_ONLINE", (255, 0, 0), False)
				pygame.quit()
				sys.exit()
		pygame.display.update()
def handle_request(*data):
	SizeStruct = struct.Struct('!I')
	info = pickle.dumps(data)
	try:
		with SocketManager(Address) as sock:
			sock.sendall(SizeStruct.pack(len(info)))
			sock.sendall(info)
			size_info = sock.recv(SizeStruct.size)
			size = SizeStruct.unpack(size_info)
			rval = sock.recv(size[0])
		return pickle.loads(rval)
	except socket.error as err:
		print (err)
		sys.exit(1)
class SocketManager:
	def __init__(self, address):
		self.address = address
	def __enter__(self, *ignore):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect(self.address)
		return self.sock
	def __exit__(self, *ignore):
		self.sock.close()
main()
