import random
import math
import time


def quick_power(a, b, m):
    # print("a: " + str(a))
    # print("b: " + str(b))
    # print("m: " + str(m))
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
    # print("a: " + str(a))
    # print("b: " + str(b))
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
    # print(p)
    # print(m)
    # print(k)
    if m * k <= p:
        print('Error: bad arguments')
        return -1

    mrow = []
    t = y % p
    mrow.append([t, 0])
    for j in range(1, m):
        t = (t * a) % p
        mrow.append([t, j])
    # print(mrow)
    mrow.sort()
    # print(mrow)

    krow = []
    for i in range(1, k + 1):
        krow.append([quick_power(a, i * m, p), i])
    # print(krow)
    krow.sort()
    # print(krow)

    for i in krow:
        for j in mrow:
            if i[0] == j[0]:
                # print(i)
                # print(j)
                x = i[1] * m - j[1]
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
        time.sleep(0.00001)
        random.seed(time.time())
        # prime number must be greater than any number can be represented in 1 byte
        p = random.randint(256, 10000)
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
    time.sleep(0.0000001)
    random.seed(time.time())
    g = 2 + random.randint(1, p)
    ok = False
    while not ok:
        if quick_power(g, q, p) != 1 and (g > 1) and (g < (p - 1)):
            ok = True
        else:
            g = 2 + random.randint(1, p)
    return g


def get_cd(c, p):
    ans = common_euclid(c, p - 1)
    while c * ans[2] % (p - 1) != 1:
        random.seed(time.time())
        c = random.randint(2, int(math.sqrt(p)))
        if c % 2 == 0:
            c += 1
        ans = common_euclid(c, p - 1)
    return c, ans[2]


def rand(a, b):
    time.sleep(0.0000001)
    random.seed(time.time())
    return random.randint(a, b)
