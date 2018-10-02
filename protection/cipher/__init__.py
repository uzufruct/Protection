from protection import basic


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


def elgamal_encode(m, p):
    return m


def elgamal_decode(msg, p):
    return msg


def rsa_encode(m, d, n):
    e = basic.quick_power(m, d, n)
    return e


def rsa_decode(e, c, n):
    m = basic.quick_power(e, c, n)
    return m
