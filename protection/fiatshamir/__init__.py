from protection import basic
import socket


def verify(sock, n, v, rounds_number=40):
    ok = True
    res = False
    sock.send(rounds_number.to_bytes(2, byteorder='big'))
    for i in range(0, rounds_number):
        data = sock.recv(1000000)
        x = int.from_bytes(data, byteorder='big')

        e = get_e()
        sock.send(e.to_bytes(1, byteorder='big'))

        data = sock.recv(1000000)
        y = int.from_bytes(data, byteorder='big')
        if y == 0:
            ok = False
        else:
            y1 = (y * y) % n
            y2 = (x * pow(v, e)) % n
            if not y1 == y2:
                ok = False

    if ok:
        p = 1 / (pow(2, rounds_number))
        ans = "Authentication is valid with probability " + str(1 - p) + "%\nAccess granted"
        res = True
    else:
        ans = "Invalid authentication! Access is forbidden"
        res = False
    sock.send(ans.encode())
    return res


def get_e():
    return basic.rand(0, 1)


def prove(sock, n, s):
    data = sock.recv(1000000)
    t = int.from_bytes(data, byteorder='big')
    # print(t)

    for i in range(0, t):
        r = basic.rand(1, n - 1)
        x = (r * r) % n
        sock.send(x.to_bytes(4, byteorder='big'))

        data = sock.recv(1000000)
        e = int.from_bytes(data, byteorder='big')

        y = (r * pow(s, e)) % n
        sock.send(y.to_bytes(4, byteorder='big'))

    data = sock.recv(1000000)
    ans = data.decode()
    print(ans)
