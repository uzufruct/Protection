from protection import basic
from protection import cipher
from math import sqrt


def rsa_handler(filename, mode='encode'):
    fd = open(filename, 'rb')
    if mode == 'encode':
        out = open(filename + ".rsa", 'wb')

        p = basic.get_prime()
        q = basic.get_prime()
        n = p * q

        phi = (p - 1) * (q - 1)

        keys = basic.get_cd(basic.rand(3, int(sqrt(phi))), phi + 1)

        c = keys[0]
        d = keys[1]

        out.write(c.to_bytes(4, byteorder='big'))
        out.write(n.to_bytes(4, byteorder='big'))
        while True:
            char = fd.read(1)
            if not char:
                break
            out.write(cipher.rsa_encode(ord(char), d, n).to_bytes(4, byteorder='big'))
        fd.close()
        out.close()
        output = filename + ".rsa"

    elif mode == 'decode':
        out = open(filename[:-len(".rsa")], 'wb')

        c = int.from_bytes(fd.read(4), byteorder='big')
        n = int.from_bytes(fd.read(4), byteorder='big')

        while True:
            char = fd.read(4)
            if not char:
                break
            out.write(cipher.rsa_decode(int.from_bytes(char, byteorder='big'), c, n).to_bytes(1, byteorder='big'))
        fd.close()
        out.close()
        output = filename[:-len(".rsa")]

    else:
        print("Unknown parameter")
        output = ""
        fd.close()

    return output


def shamir_handler(filename, mode='encode'):
    fd = open(filename, 'rb')

    if mode == 'encode':
        out = open(filename + ".shmr", 'wb')

        p = basic.get_prime()
        alice = basic.get_cd(basic.rand(3, int(sqrt(p))), p)
        bob = basic.get_cd(basic.rand(3, int(sqrt(p))), p)

        out.write(bob[1].to_bytes(4, byteorder='big'))
        out.write(p.to_bytes(4, byteorder='big'))
        while True:
            char = fd.read(1)
            if not char:
                break
            out.write(cipher.shamir_encode(ord(char), alice, bob, p).to_bytes(2, byteorder='big'))
        fd.close()
        out.close()
        output = filename + ".shmr"

    elif mode == 'decode':
        out = open(filename[:-len(".shmr")], 'wb')

        d_bob = int.from_bytes(fd.read(4), byteorder='big')
        p = int.from_bytes(fd.read(4), byteorder='big')

        while True:
            char = fd.read(2)
            if not char:
                break
            out.write(cipher.shamir_decode(int.from_bytes(char, byteorder='big'), d_bob, p).to_bytes(1, byteorder='big'))
        fd.close()
        out.close()
        output = filename[:-len(".shmr")]

    else:
        print("Unknown parameter")
        fd.close()
        output = ""

    return output


def vernam_handler(filename, mode='encode'):
    fd = open(filename, 'rb')

    if mode == 'encode':
        out = open(filename + ".vrn", 'wb')
        key = basic.vernam_key(len("1000"))
        # print(key)
        out.write(key.to_bytes(2, byteorder='big'))
        while True:
            char = fd.read(1)
            if not char:
                break
            out.write(cipher.vernam_encode(1000 + ord(char), key).to_bytes(2, byteorder='big'))
        fd.close()
        out.close()
        output = filename + ".vrn"

    elif mode == 'decode':
        out = open(filename[:-len(".vrn")], 'wb')
        key = int.from_bytes(fd.read(2), byteorder='big')
        # print(key)
        while True:
            char = fd.read(2)
            if not char:
                break
            out.write((cipher.vernam_decode(int.from_bytes(char, byteorder='big'), key) - 1000).to_bytes(1, byteorder='big'))
        fd.close()
        out.close()
        output = filename[:-len(".vrn")]
    else:
        print("Unknown parameter")
        fd.close()
        output = ""
    return output


def elgamal_handler(filename, mode='encode'):
    fd = open(filename, 'rb')

    if mode == 'encode':
        out = open(filename + ".elg", 'wb')
        pair = basic.get_prime_pair()
        # print(pair)
        p = pair[1]
        q = pair[0]

        g = basic.get_g(p, q)
        # print(g)

        c = basic.rand(2, p - 2)
        d = basic.quick_power(g, c, p)
        # print(c, d)

        k = basic.rand(2, p - 2)
        r = basic.quick_power(g, k, p)

        out.write(r.to_bytes(2, byteorder='big'))
        out.write(p.to_bytes(2, byteorder='big'))
        out.write(c.to_bytes(2, byteorder='big'))

        while True:
            char = fd.read(1)
            if not char:
                break
            out.write(cipher.elgamal_encode(ord(char), d, k, p).to_bytes(2, byteorder='big'))
        fd.close()
        out.close()
        output = filename + ".elg"

    elif mode == 'decode':
        out = open(filename[:-len(".elg")], 'wb')

        r = int.from_bytes(fd.read(2), byteorder='big')
        p = int.from_bytes(fd.read(2), byteorder='big')
        c = int.from_bytes(fd.read(2), byteorder='big')

        while True:
            char = fd.read(2)
            if not char:
                break
            out.write(cipher.elgamal_decode(int.from_bytes(char, byteorder='big'), r, p, c).to_bytes(1, byteorder='big'))

        fd.close()
        out.close()
        output = filename[:-len(".elg")]

    else:
        print("Unknown parameter")
        fd.close()
        output = ""

    return output


# name = "Немного новостей.pdf"
name = "Немного новостей.pdf.rsa.elg.shmr"
# name = "file.sql"
# name = "file.sql.elg.shmr.shmr.rsa.vrn.elg"
# name = "lab1.py"
# name = "lab1.py.elg.rsa.elg.vrn.elg.shmr.shmr.elg.elg"

res = name[:]

print(res)
while res[-len(".rsa"):] == ".rsa" or res[-len(".shmr"):] == ".shmr" or res[-len(".vrn"):] == ".vrn" or res[-len(".elg"):] == ".elg":

        if res[-len(".rsa"):] == ".rsa":
            res = rsa_handler(res, mode='decode')
            print(res)
        elif res[-len(".shmr"):] == ".shmr":
            res = shamir_handler(res, mode='decode')
            print(res)
        elif res[-len(".vrn"):] == ".vrn":
            res = vernam_handler(res, mode='decode')
            print(res)
        elif res[-len(".elg"):] == ".elg":
            res = elgamal_handler(res, mode='decode')
            print(res)


# for i in range(0, 12):
#     mode = basic.rand(0, 4)
#     if mode == 0:
#         res = rsa_handler(res)
#         print(res)
#     elif mode == 1:
#         res = shamir_handler(res)
#         print(res)
#     elif mode == 2:
#         res = elgamal_handler(res)
#         print(res)
#     elif mode == 3:
#         res = vernam_handler(res)
#         print(res)
