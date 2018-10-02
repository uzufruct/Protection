from protection import basic
from protection import cipher
from math import sqrt


filename = "Немного новостей.pdf"
f = open(filename, 'rb')
out = open(filename + ".shamir", 'wb')

p = basic.get_prime()
# p = 5591
# print("Prime: " + str(p))

alice = basic.get_cd(basic.rand(3, int(sqrt(p))), p)
# alice = (7, 3993)
# print(alice)

bob = basic.get_cd(basic.rand(3, int(sqrt(p))), p)
# bob = (59, 379)
# print(bob)

# m = 250
# x = cipher.shamir_encode(m, alice, bob, p)
# print(x)
# print(m, cipher.shamir_decode(x, bob[1], p))

out.write(bob[1].to_bytes(2, byteorder='big'))
out.write(p.to_bytes(2, byteorder='big'))
while True:
    char = f.read(1)
    if not char:
        break
    out.write(cipher.shamir_encode(ord(char), alice, bob, p).to_bytes(2, byteorder='big'))

f.close()
out.close()

f = open(filename + ".shamir", 'rb')
out = open("decoded_" + filename, 'wb')

d_bob = int.from_bytes(f.read(2), byteorder='big')
print(d_bob)
p = int.from_bytes(f.read(2), byteorder='big')
print(p)
while True:
    char = f.read(2)
    # print(char)
    if not char:
        break
    out.write(cipher.shamir_decode(int.from_bytes(char, byteorder='big'), d_bob, p).to_bytes(1, byteorder='big'))
f.close()
out.close()
