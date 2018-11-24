from protection import mental
from random import shuffle

pack, prime = mental.init_session(54)
# print("Prime number:\n" + str(prime))
num_pack = list(pack.keys())
shuffle(num_pack)

print("Number of players: ")
num_players = int(input())

if 2 <= num_players <= 23:
    players = [mental.init_player(prime) for i in range(0, num_players)]
    # print("\nPack of cards:\n" + str(pack))
    # print("\nNumeric pack:\n" + str(num_pack))
    # print("\nPlayers:\n" + str(players))
    new_pack = mental.encode_pack(prime, num_pack, players)

    player_packs, rest_pack = mental.card_alloc(prime, new_pack, 2, players)
    # print("\nEncoded cards for each player:\n" + str(player_packs))
    # print("\nEncoded pack of cards:\n" + str(rest_pack))
    mental.card_decode(prime, player_packs, players, pack)
else:
    print("Error!")


