import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 22291
message = 'Welcome, you are connect!'

s.bind((host, port))
s.listen(5)

while True:
    c,e = s.accept()
    print('Client connected', e)
    c.send(message.encode('ascii'))



