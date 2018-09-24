import random
import math
import time


def quick_power(a, b, m):
    res = 1
    a %= m
    while b != 0:
        if b & 0x1:
            res = (res * a) % m
        a = (a * a) % m
        b >>= 1
    return res


def gcd(a, b):
    if a == b:
        return a

    if a < b:
        a, b = b, a

    while b > 0:
        t = b
        b = a % b
        a = t
    return a


def common_euclid(a, b):
    if a < b:
        a, b = b, a

    u = [a, 1, 0]
    v = [b, 0, 1]

    while v[0] != 0:
        q = int(u[0] / v[0])
        t = [u[0] % v[0], u[1] - q * v[1], u[2] - q * v[2]]
        u = v
        v = t

    if u[2] <= 0:
        u[2] += a

    return u


def diff_hell(key_a, key_b):
    y_a = quick_power(key_b[0], key_a[0], key_b[1])
    y_b = quick_power(key_b[0], key_a[1], key_b[1])

    return quick_power(y_b, key_a[0], key_b[1]), quick_power(y_a, key_a[1], key_b[1])


def steps(y, a, p, m, k):
    if m * k <= p:
        print('Error: bad arguments')
        return -1

    mrow = []
    t = y % p
    mrow.append([t, 0])
    for j in range(1, m):
        t = (t * a) % p
        mrow.append([t, 0])
    print(mrow)

    krow = []
    for i in range(1, k + 1):
        krow.append([quick_power(a, i * m, p), 1])
    print(krow)

    for i in range(1, k + 1):
        for j in range(0, m):
            if krow[i - 1][0] == mrow[j][0]:
                print(krow[i - 1], i)
                print(mrow[j], j)
                x = i * m - j
                new = mrow + krow
                print(new)
                new.sort()
                print(new)
                return x

    return -1


def check_prime(prime):
    ok = True
    for i in range(2, int(math.sqrt(prime))):
        if prime % i == 0:
            ok = False
    return ok


def get_prime():
    while 1:
        random.seed(time.time())
        p = random.randint(1, 10000)
        if check_prime(p):
            return p


def get_prime_pair():
    ok = False
    while not ok:
        p = get_prime()
        q = 2 * p + 1
        if check_prime(q):
            ok = True
    return p, q


def get_g(p, q):
    random.seed(time.time())
    g = 2 + random.randint(1, p)
    ok = False
    while not ok:
        if quick_power(g, q, p) == 1 and (g > 1) and (g < (p - 1)):
            ok = True
        g = 2 + random.randint(1, p)
    return g


def get_cd(c, p):
    random.seed(time.time())
    ans = common_euclid(c, p - 1)
    while ans[0] != 1:
        c = 1 + random.randint(1, p - 1)
        ans = common_euclid(c, ans[2])
    return c, ans[2]
