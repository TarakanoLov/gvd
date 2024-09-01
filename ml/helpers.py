import random
from base_game import cards
import numpy as np

def choose_move_from_array(arr, player, only_drop=False, eps=0.0):
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

def print_for_learn(action_val, player1, player2, critic, all_game_situation, card_to_use, gen_all_card_other, card_deck_hod, more_features):
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
    print('вероятность победы', (critic.predict(np.concatenate([all_game_situation[-1], card_deck_hod[-1], more_features[-1]], axis=0).reshape(1, -1), verbose=0) + 1) / 2, '%')
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
    step = 5
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
    
def second_calclulate_target_to_model(sss, new_all_rewards, game_before_end):
    assert len(sss) == len(new_all_rewards)
    assert len(new_all_rewards) == len(game_before_end)
    
    result = [0] * len(sss)
    step = 5
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

from base_game import cards

def more_features(player1, player2):
    can_use_first = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    all_first = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    for one_card in player1.cards:
        val = cards.test_card(one_card)
        if one_card.is_can_use(player1):
            can_use_first += val
        all_first += val
        
    can_use_second = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    all_second = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    for one_card in player2.cards:
        val = cards.test_card(one_card)
        if one_card.is_can_use(player2):
            can_use_second += val
        all_second += val
        
    cards_first = [*player1.cards, *reversed(player1.card_deck.all_cards)]
    first_more_cards_5 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    first_more_cards_10 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    first_more_cards_15 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    for i in range(len(player1.cards) + 15):
        val = cards.test_card(cards_first[i])
        if i < len(player2.cards) + 5:
            first_more_cards_5 += val
            first_more_cards_10 += val
            first_more_cards_15 += val
        elif i < len(player2.cards) + 10:
            first_more_cards_10 += val
            first_more_cards_15 += val
        else:
            first_more_cards_15 += val
            
    cards_second = [*player2.cards, *reversed(player2.card_deck.all_cards)]
    second_more_cards_5 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    second_more_cards_10 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    second_more_cards_15 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    for i in range(len(player2.cards) + 15):
        val = cards.test_card(cards_second[i])
        if i < len(player2.cards) + 5:
            second_more_cards_5 += val
            second_more_cards_10 += val
            second_more_cards_15 += val
        elif i < len(player2.cards) + 10:
            second_more_cards_10 += val
            second_more_cards_15 += val
        else:
            second_more_cards_15 += val
    return np.concatenate([can_use_first, all_first, can_use_second, all_second, first_more_cards_5, first_more_cards_10, first_more_cards_15, second_more_cards_5, second_more_cards_10, second_more_cards_15], axis=0)