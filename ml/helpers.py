import random
from base_game import cards
import numpy as np

def choose_move_from_array(arr, player, only_drop=False, eps=0.3):
    arr_result = []
    for one_card in player.cards:
        if not only_drop and one_card.is_can_use(player):
            arr_result.append((1, arr[cards.id_of(one_card)], one_card))
        
        arr_result.append((0, arr[len(cards.all_cards) + cards.id_of(one_card)], one_card))
        
    if random.random() < eps:
        return random.choice([(is_use, card) for is_use, _, card in arr_result])
    else:
        el = max(arr_result, key = lambda x : x[1])
        return el[0], el[2]

def print_for_learn(action_val, player1, player2, critic, all_game_situation, card_to_use, gen_all_card_other, card_deck_hod):
    arr = []
    for i in range(len(action_val)):
        if cards.all_cards[i % len(cards.all_cards)] in player1.cards:
            if i < len(cards.all_cards):
                if cards.all_cards[i % len(cards.all_cards)].is_can_use(player1):
                    arr.append((cards.all_cards[i].name, action_val[i]))
            else:
                arr.append(('------ ' + cards.all_cards[i % len(cards.all_cards)].name, action_val[i]))
    arr.sort(key=lambda x : x[1])
    print('\n\n')
    print(player1)
    print('\n\n')
    print(player2)
    print('\n\n')
    print('вероятность победы', (critic.predict(np.concatenate([all_game_situation[-1], card_to_use[-1], gen_all_card_other[-1], card_deck_hod[-1]], axis=0).reshape(1, -1), verbose=0) + 1) / 2, '%')
    for i in range(len(arr)):
        print(arr[i][0], arr[i][1])
    print('\n\n')
    
def print_for_agent(player, n_outputs=34*3*2):
    arr = []
    for i in range(n_outputs):
        if cards.all_cards[i % len(cards.all_cards)] in player.cards:
            if i < len(cards.all_cards):
                if cards.all_cards[i % len(cards.all_cards)].is_can_use(player):
                    arr.append((cards.all_cards[i].name, action_val[i]))
            else:
                arr.append(('сброс ' + cards.all_cards[i % len(cards.all_cards)].name, action_val[i]))
    arr.sort(key=lambda x : x[1])
    print('\n\n')
    print(player)
    print('\n\n')
                    
    for i in range(len(arr)):
       print(arr[i][0], arr[i][1])
    print('\n\n')