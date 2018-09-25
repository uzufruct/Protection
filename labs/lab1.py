from protection import basic
from math import sqrt
from random import randint

print("Quick power: " + str(basic.quick_power(randint(2, 100000000), randint(7, 20000000), basic.get_prime())))
print("Euclid: " + str(basic.common_euclid(basic.get_prime(), basic.get_prime())))
pair = basic.get_prime_pair()
g = basic.get_g(pair[0], pair[1])
print(pair)
print(g)
print("Check: " + str(basic.quick_power(g, pair[0], pair[1])))
print("Diffie " + str(basic.diff_hell([7, 13], [g, pair[1]])))
m = int(sqrt(pair[0])) + 1
k = m
print("Child & giant steps " + str(basic.steps(9, 2, pair[0], m, k)))
