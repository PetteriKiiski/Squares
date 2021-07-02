import socketserver, threading, sys, struct, pickle
def main():
	try:
		server = SquaresServer(('10.0.0.147', 9653), RequestHandler)
		server.serve_forever()
	except Exception as err:
		print ('ERROR: {0}'.format(err))
		sys.exit(1)
class SquaresServer(socketserver.ThreadingMixIn, socketserver.TCPServer):pass
class RequestHandler(socketserver.StreamRequestHandler):
	def handle(self):
		SizeStruct = struct.Struct('!I')
		size_data = self.rfile.read(SizeStruct.size)
		size = SizeStruct.unpack(size_data)
		size = size[0]
		data = pickle.loads(self.rfile.read(size))
		with CallLock:
			reply = CallDict[data[0]](self, *data[1:])
		reply = pickle.dumps(reply, 3)
		self.wfile.write(SizeStruct.pack(len(reply)))
		self.wfile.write(reply)
	def set_online(self, color, value):
		Online[color] = value
	def get_online(self, color):
		return Online[color]
	def change_position(self, color, loc):
		Location[color] = loc
	def get_position(self, color):
		return Location[color]
CallLock = threading.Lock()
CallDict = {"SET_ONLINE":lambda self, color, value: self.set_online(color, value), \
	"GET_ONLINE": lambda self, color:self.get_online(color), \
	"CHANGE_LOCATION": lambda self, color, loc:self.change_location(color, loc), \
	"GET_POSITION": lambda self, color:self.get_position(color)}
Online = {(255, 0, 0):False, (0, 255, 0):False}
Location = {(255, 0, 0):(0, 0), (0, 255, 0):(0, 0)}
main()
