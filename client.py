import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 22291
s.connect((host, port))
data = s.recv(1024)
print(data.decode('ascii'))

