from hashlib import md5
from protection import cipher
from protection import basic
from math import sqrt


def sign(filename, method='rsa'):
    with open(filename, 'rb') as fd:
        string = fd.read()
        m = md5(string)
        h = m.hexdigest()
        # print(h)

    if method == 'rsa':
        p = basic.get_prime()
        q = basic.get_prime()
        n = p * q
        phi = (p - 1) * (q - 1)

        keys = basic.get_cd(basic.rand(3, int(sqrt(phi))), phi + 1)

        c = keys[0]
        d = keys[1]
        with open(filename + '-sgn.rsa', 'wb') as sgn:
            sgn.write(c.to_bytes(4, byteorder='big'))
            sgn.write(n.to_bytes(4, byteorder='big'))
            for i in range(0, len(h), 2):
                x = int(h[i:i + 2], base=16)
                s = cipher.rsa_encode(x, d, n)
                sgn.write(s.to_bytes(4, byteorder='big'))

    elif method == 'elgamal':
        pair = basic.get_prime_pair()
        p = pair[1]
        q = pair[0]

        g = basic.get_g(p, q)
        c = basic.rand(2, p - 2)
        d = basic.quick_power(g, c, p)

        k = basic.rand(2, p - 2)
        k, inversed_k = basic.get_cd(k, p)
        r = basic.quick_power(g, k, p)

        with open(filename + '-sgn.elg', 'wb') as sgn:
            sgn.write(p.to_bytes(4, byteorder='big'))
            sgn.write(g.to_bytes(4, byteorder='big'))
            sgn.write(r.to_bytes(4, byteorder='big'))
            sgn.write(d.to_bytes(4, byteorder='big'))
            for i in range(0, len(h), 2):
                x = int(h[i:i + 2], base=16)
                u = (x - c * r) % (p - 1)
                s = (inversed_k * u) % (p - 1)
                sgn.write(s.to_bytes(4, byteorder='big'))

    elif method == 'gost':
        p, q, a = get_gost_base()

        c = basic.rand(1, q - 1)
        d = basic.quick_power(a, c, p)

        k = basic.rand(1, q - 1)
        r = basic.quick_power(a, k, p) % q
        while r == 0:
            k = basic.rand(1, q - 1)
            r = basic.quick_power(a, k, p) % q

        with open(filename + '-sgn.gost', 'wb') as sgn:
            sgn.write(p.to_bytes(4, byteorder='big'))
            sgn.write(q.to_bytes(4, byteorder='big'))
            sgn.write(r.to_bytes(4, byteorder='big'))
            sgn.write(d.to_bytes(4, byteorder='big'))
            sgn.write(a.to_bytes(4, byteorder='big'))
            for i in range(0, len(h), 2):
                x = int(h[i:i + 2], base=16)
                s = (k * x + c * r) % q
                if s == 0:
                    print("Error! Please, resign file.")
                    break
                else:
                    sgn.write(s.to_bytes(4, byteorder='big'))
    else:
        print('Unknown method!')
    return h


def check(filename):
    res = 'Signature is invalid'
    with open(filename, 'rb') as sgn:
        if filename[-len('-sgn.rsa'):] == '-sgn.rsa':
            c = int.from_bytes(sgn.read(4), byteorder='big')
            n = int.from_bytes(sgn.read(4), byteorder='big')
            w = ''
            while True:
                char = sgn.read(4)
                if not char:
                    break
                s = int.from_bytes(char, byteorder='big')
                x = cipher.rsa_decode(s, c, n)
                wi = str(hex(x))
                if len(wi[2:]) != 2:
                    w += '0' + wi[2:]
                else:
                    w += wi[2:]
            # print(w)
            with open(filename[:-len('-sgn.rsa')], 'rb') as fd:
                string = fd.read()
                m = md5(string)
                h = m.hexdigest()
                # print(h)
                if h == w:
                    res = 'Signature is valid'
        elif filename[-len('-sgn.elg'):] == '-sgn.elg':
            p = int.from_bytes(sgn.read(4), byteorder='big')
            g = int.from_bytes(sgn.read(4), byteorder='big')
            r = int.from_bytes(sgn.read(4), byteorder='big')
            d = int.from_bytes(sgn.read(4), byteorder='big')

            fd = open(filename[:-len('-sgn.elg')], 'rb')
            string = fd.read()
            m = md5(string)
            fd.close()
            h = m.hexdigest()

            ok = True
            i = 0
            while ok:
                char = sgn.read(4)
                if not char:
                    break
                s = int.from_bytes(char, byteorder='big')
                x = int(h[i:i + 2], base=16)
                if not (pow(d, r) * pow(r, s)) % p == basic.quick_power(g, x, p):
                    ok = False
                i += 2
            if ok:
                res = 'Signature is valid'
        elif filename[-len('-sgn.gost'):] == '-sgn.gost':
            p = int.from_bytes(sgn.read(4), byteorder='big')
            q = int.from_bytes(sgn.read(4), byteorder='big')
            r = int.from_bytes(sgn.read(4), byteorder='big')
            d = int.from_bytes(sgn.read(4), byteorder='big')
            a = int.from_bytes(sgn.read(4), byteorder='big')

            fd = open(filename[:-len('-sgn.gost')], 'rb')
            string = fd.read()
            m = md5(string)
            fd.close()
            h = m.hexdigest()

            ok = True
            i = 0
            while ok:
                char = sgn.read(4)
                if not char:
                    break
                s = int.from_bytes(char, byteorder='big')
                x = int(h[i:i + 2], base=16)
                u1 = (s * get_inverse(x, q)) % q
                u2 = (-1 * r * get_inverse(x, q)) % q
                v = ((pow(a, u1) * pow(d, u2)) % p) % q
                if not v == r:
                    ok = False
                i += 2
            if ok:
                res = 'Signature is valid'

    return res


def get_gost_base():
    while True:
        # prime number must be greater than any number can be represented in 1 byte
        q = basic.rand(2 ** 8, 2 ** 9 - 1)
        if basic.check_prime(q):
            for i in range(1, 1000):
                p = i * q + 1
                if basic.check_prime(p):
                    break
            break
    a = 2
    while True:
        if basic.quick_power(a, q, p) == 1:
            break
        else:
            a += 1
    return p, q, a


def get_inverse(h, q):
    ans = basic.common_euclid(h, q)
    if h * ans[2] % q == 1:
        return ans[2]
    else:
        print("Error of inverse")
        return 1
