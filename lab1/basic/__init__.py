import random
import math
import bisect
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


# def steps(y, a, p, m, k):
#     if m * k <= p:
#         print('Error: bad arguments')
#         return -1
#
#     row = []
#     y %= p
#     am = a % p
#     row.append([y, 0])
#     for i in (1, m):
#         row.append([(y * a) % p, i])
#         a = (a * am) % p
#
#     max = row[row.__len__() - 1]
#     maxi = 1
#     for i in (i, k + 1):
#         i_max = bisect.bisect_left(row, [a, 0])
#         if row[i_max][0] == a:
#             maxi = i
#             break
#         else:
#             max = row[row.__len__() - 1]
#         a = (a * am) % p
#     if max == row[row.__len__() - 1]:
#         print("Error: bad rows")
#     return (maxi * m) - max[1]


def check_prime(prime):
    ok = True
    for i in (2, int(math.sqrt(prime))):
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
