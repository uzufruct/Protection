from protection import finance


print("*** Welcome to Sberbank Online! ****")
print("\nLoading...\n")
print("Please, deposit money in your account:")
money = int(input())

n, d, c = finance.bank_init(client_value=money)
print("Loaded successfully!\n")

print("Please, enter size of cash you wish")
money = int(input())

cash = finance.split_money(money, n, c)
print(cash)

finance.payment(cash, n, d)

print("Sberbank accounts: " + str(finance.accounts))
