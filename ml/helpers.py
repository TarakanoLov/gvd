import random
from base_game import cards
import numpy as np

def choose_move_from_array(arr, player, only_drop=False, eps=0.2):
    arr_result = []
    count_can_use = 0
    for one_card in player.cards:
        if not only_drop and one_card.is_can_use(player):
            count_can_use += 1
            arr_result.append([1, arr[cards.id_of(one_card)], one_card])
        
        arr_result.append([0, arr[len(cards.all_cards) + cards.id_of(one_card)], one_card])
        
    if eps != 0.0:
        noise = np.random.normal(0, 0.2, len(arr_result))
        for i in range(len(arr_result)):
            arr_result[i][1] += noise[i]
        el = max(arr_result, key = lambda x : x[1])
        return el[0], el[2]   
        #return random.choices([(is_use, card) for is_use, _, card in arr_result], weights=[arr_result[i][1] + noise[i] for i in range(len(arr_result))])[0]
    else:
        #if count_can_use != 0:
        #    el = max([arr_result[i] for i in range(len(arr_result)) if arr_result[i][0]], key = lambda x : x[1])
        #    return el[0], el[2]
        #else:
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
    print('\n')
    print(player1)
    print('\n')
    print(player2)
    print('\n')
    print('вероятность победы', (critic.predict(np.concatenate([all_game_situation[-1], card_deck_hod[-1]], axis=0).reshape(1, -1), verbose=0) + 1) / 2, '%')
    #print('вероятность победы', (critic.predict(np.concatenate([all_game_situation[-1], card_to_use[-1], gen_all_card_other[-1], card_deck_hod[-1]], axis=0).reshape(1, -1), verbose=0)))
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
    
def calclulate_target_to_model(sss, new_all_rewards, game_before_end):
    assert len(sss) == len(new_all_rewards)
    assert len(new_all_rewards) == len(game_before_end)
    
    result = [0] * len(sss)
    step = 3
    for i in range(len(sss)):
        if i >= len(sss) - step or game_before_end[i] <= step:
            if new_all_rewards[i] > 0:
                result[i] = 0.9
            else:
                result[i] = -0.9
        else:
            if sss[i + step] > sss[i]:
                result[i] = 0.9
            elif sss[i + step] == sss[i]:
                result[i] = 0.0
            else:
                result[i] = -0.9
    return result
    
def new_calclulate_target_to_model(critic_prediction, new_all_rewards, game_before_end):
    assert len(critic_prediction) == len(new_all_rewards)
    assert len(new_all_rewards) == len(game_before_end)
    
    result = [0] * len(critic_prediction)
    step = 5
    for i in range(len(critic_prediction)):
        if i >= len(critic_prediction) - step or game_before_end[i] <= step:
            if 0 < critic_prediction[i][1] < 0.95:
                result[i] = 0.9
            elif 0 < critic_prediction[i][1] >= 0.95:
                result[i] = 0
            elif 0 > critic_prediction[i][1] > -0.95:
                result[i] = -0.9
            elif 0 > critic_prediction[i][1] <= -0.95:
                result[i] = 0
            else:
                print(critic_prediction[i][1])
                assert(False)
        else:
            if critic_prediction[i][1] > critic_prediction[i + step][0]:
                result[i] = -0.9
            elif critic_prediction[i][1] < critic_prediction[i + step][0]:
                result[i] = 0.9
            elif critic_prediction[i][1] == critic_prediction[i + step][0]:
                result[i] = 0.0
            else:
                print(critic_prediction[i], critic_prediction[i + step])
                assert(False)
    return result