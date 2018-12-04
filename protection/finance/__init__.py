from protection import basic
from math import sqrt

accounts = {"client": 0, "store": 0}
history = set()
banknote_types = (1, 5, 10, 20, 50, 100, 200, 500)


def bank_init(client_value=999999, store_value=0):
    p, q = basic.get_prime_pair()
    n = p * q
    phi = (p - 1) * (q - 1)
    c, d = basic.get_cd(basic.rand(3, int(sqrt(phi))), phi + 1)
    accounts["client"] = client_value
    accounts["store"] = store_value
    print("Sberbank accounts: " + str(accounts))
    return n, d, c


def account_handler(n, banknote, key, value, account='client', operation='withdraw'):
    # print(accounts)
    # print(value)
    if operation == 'withdraw':
        if value <= accounts[account]:
            accounts[account] -= value
            s = basic.quick_power(banknote, key, n)
            history.add(banknote)
            return s
        else:
            print("Not enough money for this operation!")
            return -1
    elif operation == 'deposit':
        s = basic.quick_power(banknote, key, n)
        if s in history:
            accounts[account] += value
            return s
        else:
            print("Invalid banknote!")
            return -1
    else:
        print("Invalid operation!")
        return -1


def split_money(value, n, c):
    banknotes = []
    j = banknote_types.__len__() - 1
    while value > 0:
        if j < 0:
            break
        elif int(value / banknote_types[j]) > 0:
            x = int(value / banknote_types[j])
            for i in range(0, x):
                h = int(hash(str(banknote_types[j] + i)) / pow(10, 14))
                if h < 0:
                    h *= -1
                print("\n" + str(banknote_types[j]) + ' euro with hash ' + str(h))
                s = account_handler(n, h, c, banknote_types[j], account='client', operation='withdraw')
                if s != -1:
                    value -= banknote_types[j]
                    print("Successful! Your cash is " + str(banknote_types[j]) + " euro with signature " + str(s))
                    banknotes.append((banknote_types[j], s))
                else:
                    print("\nFailed! :(")
                    j = -1
                    break
        else:
            j -= 1
    return banknotes


def payment(banknotes, n, d):
    for banknote in banknotes:
        err = account_handler(n, banknote[1], d, banknote[0], account='store', operation='deposit')
        if err == -1:
            print(str(banknote[0]) + " euro banknote with signature " + str(banknote[1]) + " is not valid")