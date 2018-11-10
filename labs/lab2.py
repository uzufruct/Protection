from protection import cipher


# name = "Немного новостей.pdf"
name = "Немного новостей.pdf.elg"

res = [name, ""]

print(res)
while (res[0][-len(".rsa"):] == ".rsa" or res[0][-len(".shmr"):] == ".shmr"
       or res[0][-len(".vrn"):] == ".vrn" or res[0][-len(".elg"):] == ".elg"):

        if res[0][-len(".rsa"):] == ".rsa":
            res = cipher.rsa_handler(res[0], mode='decode')
            print(res)
        elif res[0][-len(".shmr"):] == ".shmr":
            res = cipher.shamir_handler(res[0], mode='decode')
            print(res)
        elif res[0][-len(".vrn"):] == ".vrn":
            res = cipher.vernam_handler(res[0], mode='decode')
            print(res)
        elif res[0][-len(".elg"):] == ".elg":
            res = cipher.elgamal_handler(res[0], mode='decode')
            print(res)


# res = cipher.rsa_handler(name)
# print(res)
#
# res = cipher.shamir_handler(name)
# print(res)
#
# res = cipher.elgamal_handler(name)
# print(res)
#
# res = cipher.vernam_handler(name)
# print(res)
