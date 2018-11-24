from protection import basic, cipher
from math import sqrt
from random import shuffle


name_card = {0: '2', 1: '3', 2: '4', 3: '5', 4: '6', 5: '7', 6: '8', 7: '9', 8: '10',
             9: 'Valet', 10: 'Queen', 11: 'King', 12: 'A'}


def init_session(n_cards):
    p = basic.get_prime()
    pack = {basic.rand(2, p - 1): i for i in range(1, n_cards + 1)}
    return pack, p


def init_player(p):
    c, d = basic.get_cd(basic.rand(3, int(sqrt(p))), p)
    return c, d


def encode_pack(p, num_pack, players):
    encoded_pack = num_pack
    for player in players:
        encoded_pack = [cipher.rsa_encode(card, player[0], p) for card in encoded_pack]
        # print(encoded_pack)
    # print("\nEncoded pack:\n" + str(encoded_pack))
    return encoded_pack


def card_alloc(p, encoded_pack, for_player, players):
    player_packs = dict.fromkeys(players)
    for player in players:
        l = []
        for i in range(for_player):
            shuffle(encoded_pack)
            l.append(encoded_pack.pop())
        player_packs[player] = l[:]
    for player in players:
        for current_player in players:
            cards = player_packs[player]
            if not current_player == player:
                player_packs[player] = [cipher.rsa_decode(card, current_player[1], p) for card in cards]
    return player_packs, encoded_pack


def card_decode(p, player_packs, players, pack):
    for player in players:
        print("\nPlayer: " + str(player))
        cards = player_packs[player]
        cards = [cipher.rsa_decode(card, player[1], p) for card in cards]
        decoded = [pack[card] for card in cards]
        for dec in decoded:
            s = '\t'
            if 0 <= dec <= 52:
                if dec % 4 == 0:
                    s += 'Hearts '
                elif dec % 4 == 1:
                    s += 'Tiles '
                elif dec % 4 == 2:
                    s += 'Clovers '
                elif dec % 4 == 3:
                    s += 'Pikes '
                s += name_card[dec % 13]
                print(s)
            else:
                print('Joker')
