import random
import os
from collections import deque
import copy

import tensorflow as tf
from keras import backend as K
from keras.models import Model
from keras.layers import Dense, Input, concatenate, Flatten, Multiply, Dropout
from keras.optimizers import SGD
from keras.callbacks import EarlyStopping, ModelCheckpoint

from joblib import dump, load
from sklearn import preprocessing
from sklearn.metrics import mean_squared_error

import my_model
import pickle

import numpy as np

import game
import player
import cards
import card_deck
import agent
import critic_model


n_inputs = 2 + 2 + 6 + 6
n_games_per_update = 100
n_max_steps = 100
n_iterations = 1000001
    
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
            

def gen_array_input(player1, player2):
    arr = np.zeros((1, n_inputs))
    arr[0][0] = player1.tower
    arr[0][1] = player1.wall
    arr[0][2] = player2.tower
    arr[0][3] = player2.wall
    arr[0][4] = player1.mine
    arr[0][5] = player1.monastery
    arr[0][6] = player1.barracks
    arr[0][7] = player1.ore
    arr[0][8] = player1.mana
    arr[0][9] = player1.squad
    arr[0][10] = player2.mine
    arr[0][11] = player2.monastery
    arr[0][12] = player2.barracks
    arr[0][13] = player2.ore
    arr[0][14] = player2.mana
    arr[0][15] = player2.squad

    return arr

def isclose(a, b, abs_tol=0.001):
    return abs(a-b) <= abs_tol
    
def gen_my_all_card(player):
    result = np.zeros((1, 34 * 3 * 2))
    for one_card in player.cards:
        if one_card.is_can_use(player):
            result[0][cards.id_of(one_card)] = 1
        result[0][len(cards.all_cards) + cards.id_of(one_card)] = 1
    return result


with open('new_all_game_situation_scaller.pkl', 'rb') as file:
    new_all_game_situation_scaller = pickle.load(file)

with open('random_forest.pickle', 'rb') as file:
    random_forest = pickle.load(file)
    
def gen_array(model, player1, player2):
    return model.predict([new_all_game_situation_scaller.transform(gen_array_input(player1, player2)), gen_my_all_card(player1)], verbose=0)

#import my_models.new_model_78.policy as myNewAIaget
#model = my_model.make_model_79_5()
#model.load_weights('great_model_79_5/model_80.h5')
model = my_model.make_model_test()
model.load_weights('actor.h5')

def make_predict(player1, player2):
    action_val = gen_array(model, player1, player2)  
    action_val = action_val[0]

    return action_val, action_val


if __name__ == '__main__':
    #######critic = critic_model.make_shok_critic()
    critic = critic_model.make_critic_model()
    #######critic.load_weights('shok_critic.h5')
    #critic.load_weights('new_critic.h5')
    critic.load_weights('amazing_new_critic.h5')
    #model.load_weights('great_model_79_5/model_80.h5')
    #critic = critic_model.make_critic_model()
    #critic.load_weights("critic_nn_0_5811.h5")
    with open('critic_scaller.pkl', 'rb') as file:
        critic_scaller = pickle.load(file)

    last = 50
    last_iter = 0
    is_reload = True
    
    for iteration in range(n_iterations):
        all_rewards = []
        all_game_situation = []    
        card_to_use = []
        action_val_array = []
        array_index_hod = []
        card_deck_hod_second = []
        gen_all_card_other = []
        card_with_is_use = []
        
        all_rewards_second = []
        all_game_situation_second = []    
        card_to_use_second = []
        action_val_array_second = []
        array_index_hod_second = []
        card_deck_hod = []
        gen_all_card_other_second = []
        win_ai, win_bot = 0, 0
        card_with_is_use_second = []                
        game_before_end = []
        game_before_end_second = []
        
        for n in range(n_games_per_update):
            this_card_deck = card_deck.Random_card_deck()
            player1 = player.Player(this_card_deck, 20)
            player2 = player.Player(this_card_deck, 20)
            only_drop = False
            who_win = -1
            current_rewards = []
            current_rewards_second = []
            
            for i in range(n_max_steps):
                player1.get_new_resource()
                #while True:
                for gggg in range(1):
                    #action_val, base = myNewAIaget.make_predict(player1, player2)
                    action_val, base = make_predict(player1, player2)                   
                    
                    is_use, card_to_move = choose_move_from_array(action_val, player1, only_drop)
                    
                    if is_use:
                        card_with_is_use.append(cards.id_of(card_to_move))
                    else:
                        card_with_is_use.append(len(cards.all_cards) + cards.id_of(card_to_move))
                    
                    card_deck_hod.append(np.concatenate([player1.card_deck.to_array(), player2.card_deck.to_array()], axis=0))
                    all_game_situation.append(gen_array_input(player1, player2)[0])
                    card_to_use.append(gen_my_all_card(player1)[0])
                    gen_all_card_other.append(gen_my_all_card(player2)[0])
                    
                    #action_val_array.append(action_val - base)

                        
                    if n == 0 and i == 10:
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
                        #print('вероятность победы', (random_forest.predict(np.concatenate([all_game_situation[-1], card_to_use[-1], gen_all_card_other[-1], card_deck_hod[-1]], axis=0).reshape(1, -1)) + 1) / 2, '%')    
                        print('вероятность победы', (critic.predict(critic_scaller.transform(np.concatenate([all_game_situation[-1], card_to_use[-1], gen_all_card_other[-1], card_deck_hod[-1]], axis=0).reshape(1, -1)), verbose=0) + 1) / 2, '%')
                        for i in range(len(arr)):
                            print(arr[i][0], arr[i][1])
                        print('\n\n')


                    current_rewards.append(player1.tower - player2.tower)                                  
                    only_drop = False
                    next_move_too = False
                    if is_use:
                        next_move_too, only_drop = card_to_move.use(player1, player2)
                        if player1.win(player2):
                            who_win = 1
                            break
                    else:
                        player1.drop(card_to_move)
                        
                        
                    if not next_move_too:
                        break
                        
                if player1.win(player2):
                    break
                    
                only_drop = False
                next_move_too = False
                player2.get_new_resource()
                #while True:
                for gggg in range(1):
                    #action_val, base = myNewAIaget.make_predict(player2, player1)
                    action_val, base = make_predict(player2, player1)

                    is_use, card_to_move = choose_move_from_array(action_val, player2, only_drop)
                    if is_use:
                        card_with_is_use_second.append(cards.id_of(card_to_move))
                    else:
                        card_with_is_use_second.append(len(cards.all_cards) + cards.id_of(card_to_move))
                    all_game_situation_second.append(gen_array_input(player2, player1)[0])
                    card_to_use_second.append(gen_my_all_card(player2)[0])
                    card_deck_hod_second.append(np.concatenate([player2.card_deck.to_array(), player1.card_deck.to_array()], axis=0))
                    action_val_array_second.append(action_val - base)
                    gen_all_card_other_second.append(gen_my_all_card(player1)[0])
                    
                        
                        
                    
                    current_rewards_second.append(player1.tower - player2.tower)    
                    next_move_too = False
                    only_drop = False
                    if is_use:
                        next_move_too, only_drop = card_to_move.use(player2, player1)
                        if player2.win(player1):
                            who_win = 2
                            if is_use:
                                pass
                            break
                    else:
                        player2.drop(card_to_move)
                    
                    if not next_move_too:
                        break
                        
                if player2.win(player1):
                    break     
                               
            if who_win == 1 or player1.tower > player2.tower:
                win_ai += 1
                all_rewards.extend([0.9 for i in range(len(current_rewards))])
                all_rewards_second.extend([-0.9 for i in range(len(current_rewards_second))])
                
                game_before_end.extend([len(current_rewards) - i for i in range(len(current_rewards))])
                game_before_end_second.extend([len(current_rewards_second) - i for i in range(len(current_rewards_second))])
            else:
                win_bot += 1
                all_rewards_second.extend([0.9 for i in range(len(current_rewards_second))])
                all_rewards.extend([-0.9 for i in range(len(current_rewards))])
                game_before_end.extend([len(current_rewards) - i for i in range(len(current_rewards))])
                game_before_end_second.extend([len(current_rewards_second) - i for i in range(len(current_rewards_second))])
            if n == 0:
                print('В первой игре победил =', all_rewards[0])
                
            if n != 0 and n % 1 == 0:    
                print('\r{}  {}  {} %             '.format(iteration, n / n_games_per_update * 100, (win_ai) / (win_ai + win_bot) * 100), end='')
            
            
        game_before_end.extend(game_before_end_second)    
        card_deck_hod.extend(card_deck_hod_second)    
        all_game_situation.extend(all_game_situation_second)
        card_to_use.extend(card_to_use_second)
        all_rewards.extend(all_rewards_second)
        gen_all_card_other.extend(gen_all_card_other_second)
        card_with_is_use.extend(card_with_is_use_second)
        
        print('\n', len(all_rewards) / 2 / n_games_per_update)

        new_gen_all_card_other = np.asarray(gen_all_card_other)
        
        new_card_deck_hod = np.asarray(card_deck_hod)
        
        new_all_game_situation = np.asarray(all_game_situation)

        new_card_to_use = np.asarray(card_to_use)
        new_all_rewards = np.asarray(all_rewards)
        sss = critic.predict(critic_scaller.transform(np.concatenate([new_all_game_situation, new_card_to_use, new_gen_all_card_other, new_card_deck_hod], axis=1)))
        
        need_to_delete = []
        step = 5
        for i in range(len(sss)):
            if i >= len(sss) - step:
                if isclose(new_all_rewards[i], sss[i]):
                    need_to_delete.append(i)
                    continue
                if new_all_rewards[i] > sss[i]:
                    sss[i] = 0.9
                else:
                    sss[i] = -0.9
            elif game_before_end[i] >= step:
                if isclose(sss[i + step], sss[i]):
                    need_to_delete.append(i)
                    continue
                if sss[i + step] > sss[i]:
                    sss[i] = 0.9
                else:
                    sss[i] = -0.9
            else:
                if isclose(new_all_rewards[i], sss[i]):
                    need_to_delete.append(i)
                    continue
                if new_all_rewards[i] == 0.9:
                    sss[i] = 0.9
                else:
                    sss[i] = -0.9
        
        print('колличество удаленных элементов =', len(need_to_delete))
        sss = np.delete(sss, need_to_delete, axis=0)
        new_all_game_situation = np.delete(new_all_game_situation, need_to_delete, axis=0)
        new_card_to_use = np.delete(new_card_to_use, need_to_delete, axis=0)
        new_gen_all_card_other = np.delete(new_gen_all_card_other, need_to_delete, axis=0)
        new_card_deck_hod = np.delete(new_card_deck_hod, need_to_delete, axis=0)
        new_all_rewards = np.delete(new_all_rewards, need_to_delete, axis=0)
        
        #conv = lambda inp : 1 if inp == 1 else -1
        reward_for_critic = new_all_rewards
        #for i in range(len(reward_for_critic)):
        #    reward_for_critic[i] = conv(reward_for_critic[i])
        
        new_action_val_array = np.zeros((len(sss), 204))
        new_card_to_use = np.zeros((len(sss), 204))
        for i in range(len(sss)):
            new_action_val_array[i][card_with_is_use[i]] = sss[i]
            new_card_to_use[i][card_with_is_use[i]] = 1
        
        callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=1)
        l = int(len(new_all_game_situation) * 0.8)
            
        new_all_game_situation = new_all_game_situation_scaller.transform(new_all_game_situation)
        
        #print('input to actor', 'new_all_game_situation =', new_all_game_situation[0], 'new_card_to_use =', new_card_to_use[0], 'new_action_val_array =', new_action_val_array[0])
        model.fit([new_all_game_situation, new_card_to_use], new_action_val_array, batch_size=64, epochs=1, shuffle=True)
        model.save_weights("actor.h5")
        
        ### critic
        base_inp = np.concatenate([new_all_game_situation, new_card_to_use, new_gen_all_card_other, new_card_deck_hod], axis=1)
        print('точность критика =', np.isclose(critic.predict(critic_scaller.transform(base_inp)).reshape(1, -1), reward_for_critic.reshape(1, -1), 0, 0.89).sum() / len(base_inp) * 100, '%')
        l = int(len(base_inp)*0.8)
        idx = np.random.randint(l, size=l // 10)
        inp = base_inp[idx, :]
        #print(reward_for_critic)
        #if iteration % 10 == 0:
        #    print('input for critic, input = ', critic_scaller.transform(inp[0].reshape(1, -1)), 'output =', reward_for_critic[0])
        #    critic.fit(critic_scaller.transform(inp), reward_for_critic[idx], shuffle=True, batch_size=64, epochs=1)
        #    critic.save_weights('amazing_new_critic.h5')
        
        #critic.fit(critic_scaller.transform(inp), reward_for_critic[idx], shuffle=True, batch_size=64, epochs=1)
        #critic.save_weights('amazing_new_critic.h5')