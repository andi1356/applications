# Import socket module
import socket
import time


# local host IP '127.0.0.1'
host = '127.0.0.1'

# Define the port on which you want to connect
port = 50100

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	# connect to server on local computer
	s.connect((host, port))
	while True:
		msg = 'Keep Alive'
		print(msg)
		s.sendall(msg.encode())
		time.sleep(1)
s.close


