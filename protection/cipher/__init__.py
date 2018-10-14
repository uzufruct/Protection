from protection import basic
from math import sqrt


def shamir_encode(m, alice, bob, p):
    # alice = (c, d)
    # bob = (c, d)
    x = basic.quick_power(m, alice[0], p)   # First transmission
    x = basic.quick_power(x, bob[0], p)     # Second transmission
    x = basic.quick_power(x, alice[1], p)   # Third transmission
    return x


def shamir_decode(x, d_bob, p):
    m = basic.quick_power(x, d_bob, p)
    return m


def elgamal_encode(m, d, session_key, p):
    x = (m * basic.quick_power(d, session_key, p)) % p
    return x


def elgamal_decode(x, r, p, c):
    m = (x * basic.quick_power(r, p - 1 - c, p)) % p
    return m


def rsa_encode(m, d, n):
    e = basic.quick_power(m, d, n)
    return e


def rsa_decode(e, c, n):
    m = basic.quick_power(e, c, n)
    return m


def vernam_encode(m, key):
    x = m ^ key
    return x


def vernam_decode(x, key):
    m = x ^ key
    return m

def rsa_handler(filename, mode='encode'):
    fd = open(filename, 'rb')
    if mode == 'encode':
        out = open(filename + ".rsa", 'wb')
        kfile = open(filename + ".rsak", 'wb')

        p = basic.get_prime()
        q = basic.get_prime()
        n = p * q
        phi = (p - 1) * (q - 1)

        keys = basic.get_cd(basic.rand(3, int(sqrt(phi))), phi + 1)

        c = keys[0]
        d = keys[1]

        kfile.write(c.to_bytes(4, byteorder='big'))
        kfile.write(n.to_bytes(4, byteorder='big'))
        kfile.close()

        while True:
            char = fd.read(1)
            if not char:
                break
            out.write(rsa_encode(ord(char), d, n).to_bytes(4, byteorder='big'))
        fd.close()
        out.close()
        output = [filename + ".rsa", filename + ".rsak"]

    elif mode == 'decode':
        out = open(filename[:-len(".rsa")], 'wb')
        kfile = open(filename + "k", 'rb')

        c = int.from_bytes(kfile.read(4), byteorder='big')
        n = int.from_bytes(kfile.read(4), byteorder='big')
        kfile.close()

        while True:
            char = fd.read(4)
            if not char:
                break
            out.write(rsa_decode(int.from_bytes(char, byteorder='big'), c, n).to_bytes(1, byteorder='big'))
        fd.close()
        out.close()

        output = [filename[:-len(".rsa")], "DECODED"]

    else:
        print("Unknown parameter")
        output = ["", ""]
        fd.close()

    return output


def shamir_handler(filename, mode='encode'):
    fd = open(filename, 'rb')

    if mode == 'encode':
        out = open(filename + ".shmr", 'wb')
        kfile = open(filename + ".shmrk", 'wb')

        p = basic.get_prime()
        alice = basic.get_cd(basic.rand(3, int(sqrt(p))), p)
        bob = basic.get_cd(basic.rand(3, int(sqrt(p))), p)

        kfile.write(bob[1].to_bytes(4, byteorder='big'))
        kfile.write(p.to_bytes(4, byteorder='big'))
        kfile.close()

        while True:
            char = fd.read(1)
            if not char:
                break
            out.write(shamir_encode(ord(char), alice, bob, p).to_bytes(2, byteorder='big'))
        fd.close()
        out.close()

        output = [filename + ".shmr", filename + ".shmrk"]

    elif mode == 'decode':
        out = open(filename[:-len(".shmr")], 'wb')
        kfile = open(filename + "k", 'rb')

        d_bob = int.from_bytes(kfile.read(4), byteorder='big')
        p = int.from_bytes(kfile.read(4), byteorder='big')
        kfile.close()

        while True:
            char = fd.read(2)
            if not char:
                break
            out.write(shamir_decode(int.from_bytes(char, byteorder='big'), d_bob, p).to_bytes(1, byteorder='big'))
        fd.close()
        out.close()
        output = [filename[:-len(".shmr")], "DECODED"]

    else:
        print("Unknown parameter")
        fd.close()
        output = ["", ""]

    return output


def vernam_handler(filename, mode='encode'):
    fd = open(filename, 'rb')

    if mode == 'encode':
        out = open(filename + ".vrn", 'wb')
        kfile = open(filename + ".vrnk", 'wb')
        key = basic.vernam_key(len("1000"))
        # print(key)
        kfile.write(key.to_bytes(2, byteorder='big'))
        kfile.close()

        while True:
            char = fd.read(1)
            if not char:
                break
            out.write(vernam_encode(1000 + ord(char), key).to_bytes(2, byteorder='big'))
        fd.close()
        out.close()
        output = [filename + ".vrn", filename + ".vrnk"]

    elif mode == 'decode':
        out = open(filename[:-len(".vrn")], 'wb')

        kfile = open(filename + "k", 'rb')
        key = int.from_bytes(kfile.read(2), byteorder='big')
        kfile.close()

        while True:
            char = fd.read(2)
            if not char:
                break
            out.write((vernam_decode(int.from_bytes(char, byteorder='big'), key) - 1000).to_bytes(1, byteorder='big'))
        fd.close()
        out.close()
        output = [filename[:-len(".vrn")], "DECODED"]
    else:
        print("Unknown parameter")
        fd.close()
        output = ["", ""]
    return output


def elgamal_handler(filename, mode='encode'):
    fd = open(filename, 'rb')

    if mode == 'encode':
        out = open(filename + ".elg", 'wb')
        kfile = open(filename + ".elgk", 'wb')

        pair = basic.get_prime_pair()
        p = pair[1]
        q = pair[0]

        g = basic.get_g(p, q)

        c = basic.rand(2, p - 2)
        d = basic.quick_power(g, c, p)

        k = basic.rand(2, p - 2)
        r = basic.quick_power(g, k, p)

        kfile.write(r.to_bytes(2, byteorder='big'))
        kfile.write(p.to_bytes(2, byteorder='big'))
        kfile.write(c.to_bytes(2, byteorder='big'))
        kfile.close()

        while True:
            char = fd.read(1)
            if not char:
                break
            out.write(elgamal_encode(ord(char), d, k, p).to_bytes(2, byteorder='big'))
        fd.close()
        out.close()
        output = [filename + ".elg", filename + ".elgk"]

    elif mode == 'decode':
        out = open(filename[:-len(".elg")], 'wb')
        kfile = open(filename + "k", 'rb')

        r = int.from_bytes(kfile.read(2), byteorder='big')
        p = int.from_bytes(kfile.read(2), byteorder='big')
        c = int.from_bytes(kfile.read(2), byteorder='big')
        kfile.close()

        while True:
            char = fd.read(2)
            if not char:
                break
            out.write(elgamal_decode(int.from_bytes(char, byteorder='big'), r, p, c).to_bytes(1, byteorder='big'))

        fd.close()
        out.close()
        output = [filename[:-len(".elg")], "DECODED"]

    else:
        print("Unknown parameter")
        fd.close()
        output = ["", ""]

    return output
