import socket
from protection import fiatshamir, basic

p, q = basic.get_prime_pair()
n = p * q

fd = open("scheme.auth", 'w')
fd.write(str(n))
fd.close()
print("[INFO]\tCreated authentication scheme file")

# Create client socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 8007
s.bind((host, port))
print("[INFO]\tServer host run at", host, 'with port', port)

# Connection
s.listen(1)

# Login
conn, addr = s.accept()
data = conn.recv(1000000)
print('[DEBUG]\tFrom client', addr, 'received:', data)
login = data.decode()

# Send N
fd = open("scheme.auth", 'r')
n = int(fd.readline())
fd.close()
conn.send(n.to_bytes(4, byteorder='big'))

# Receive public key V and write to file
data = conn.recv(1000000)
print('[DEBUG]\tFrom client', addr, 'received:', data)
v = int.from_bytes(data, byteorder='big')
print('[DEBUG]\tDecoded data:', v)
flog = open(login + ".login", 'w')
flog.write(str(v))
flog.close()

ok = fiatshamir.verify(conn, n, v)
if ok:
    print("[INFO]\tAccess for user", login, "at client", addr, "granted")
else:
    print("[ERROR]\tAccess for user", login, "at client", addr, "violated")

conn.close()
