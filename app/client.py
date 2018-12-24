import socket
from protection import basic, fiatshamir

# Connect to server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 8007
server.connect((host, port))

login = input("Please, log in: ")
server.send(login.encode())

# Receive N
data = server.recv(1000000)
n = int.from_bytes(data, byteorder='big')
# print(n)

# Create public key V and send to server
s = basic.get_common_inverse(n)
v = (s * s) % n
# print(s, v)
server.send(v.to_bytes(4, byteorder='big'))

print("Authentication scheme:\n\tn = " + str(n) + "\n\tv = " + str(v) + "\n\tLogin: " + login)

fiatshamir.prove(server, n, s + 1)

server.close()
