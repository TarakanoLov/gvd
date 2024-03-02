import random
import os
from collections import deque
import copy

import keras
from keras import backend as K
from keras.models import Model
from keras.layers import Dense, Input, concatenate, Flatten, Multiply, Dropout
from keras.optimizers import SGD
from keras.callbacks import EarlyStopping, ModelCheckpoint
import tensorflow as tf

import lightgbm as lgb

from sklearn.metrics import mean_squared_error

from joblib import dump, load

import my_model


import numpy as np

import game
import player
import cards
import card_deck
import agent
import critic_model


n_inputs = 2 + 2 + 6 + 6 #+ (34 + 34 + 34) #* 2
n_games_per_update = 1000
n_max_steps = 100
n_iterations = 1000001
save_iterations = 100
discount_rate = 0.999
win_ai = 0
win_bot = 0
n_outputs = 1#(34 + 34 + 34) * 2
    
def choose_move_from_array(arr, player, only_drop=False, eps=0):
    arr_result = []
    for one_card in player.cards:
        if not only_drop and one_card.is_can_use(player):
            arr_result.append((1, arr[cards.id_of(one_card)], one_card))
        
        arr_result.append((0, arr[len(cards.all_cards) + cards.id_of(one_card)], one_card))

    # if len(arr_result) == 0:
        # for one_card in player.cards:
            # arr_result.append((0, arr[cards.id_of(one_card)], one_card))
        # el = min(arr_result, key=lambda x : x[1])
        # return (el[0], el[2])
        
    if random.random() < eps:
        #return random.choices([(is_use, card) for is_use, _, card in arr_result], weights=[sec for _, sec, _ in arr_result])[0]
        return random.choice([(is_use, card) for is_use, _, card in arr_result])
    else:
        el = max(arr_result, key = lambda x : x[1])
        return el[0], el[2]

    #return random.choices([(is_use, card) for is_use, _, card in arr_result], weights=[sec for _, sec, _ in arr_result])[0]
            

def gen_array_input(player1, player2):
    arr = np.zeros((1, n_inputs))
    #arr = np.zeros((1, 1))
    #arr[0][0] = 1
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

    # for one_card in player1.cards:
        # if one_card.is_can_use(player1):
            # arr[0][16 + cards.id_of(one_card)] = 1
        # else:
            # arr[0][16 + cards.id_of(one_card)] = -1
    return arr


def nextCard(player, other, only_drop=False):
    for one_card in reversed(player.cards):
        if not only_drop and one_card.is_can_use(player):
            return (1, one_card)
            
    return (0, player.cards[-1])

    
    # arr_result = []
    # for one_card in player.cards:
        # if not only_drop and one_card.is_can_use(player):
            # arr_result.append((1, one_card))
        # arr_result.append((0, one_card))
    
    # return random.choices(arr_result)[0]
    
def gen_my_all_card(player):
    result = np.zeros((1, 34 * 3 * 2))
    for one_card in player.cards:
        if one_card.is_can_use(player):
            result[0][cards.id_of(one_card)] = 1
        result[0][len(cards.all_cards) + cards.id_of(one_card)] = 1
    return result
    
    
def gen_array(model, player1, player2):
    return model.predict([gen_array_input(player1, player2), gen_my_all_card(player1)])
    #return model.predict_proba_separate(gen_array_input(player1, player2))

def make_agent_from_model(model):
    def fff(card_deck):
        ag = agent.AgentFromModel(card_deck)
        ag.model = model
        return ag
    return fff

if __name__ == '__main__':
    critic = lgb.Booster(model_file='model_critic_0.62.txt')
    #critic_derevo = load('critic_loss_0.6932.joblib')
    #critic = critic_model.make_critic_model()
    
    #critic = load("cr_model_bandit.joblib")
    
    
    #critic.load_weights("critic.h5")
    
    #model = my_model.make_model_74_5()
    
    
    model = my_model.make_model_79_5()
    model.load_weights("great_model_79_5/model_80.h5")
    
    #model = my_model.make_model()
    
    model.load_weights("model.h5")
    
    #model_to_learn = my_model.make_model_74_5()
    #model_to_learn.load_weights("model.h5")
    
    
    #model_best = keras.models.clone_model(model)
    #opt = SGD(lr=0.000001)
    #model_best.compile(loss='categorical_crossentropy', optimizer=opt)
    #model_best.set_weights(model.get_weights())
    
    last = 50
    last_iter = 0
    is_reload = True
    last_game_cnt_hod = None
    for iteration in range(n_iterations):
        all_rewards = []
        all_game_situation = []    
        card_to_use = []
        action_val_array = []
        array_index_hod = []
        card_deck_hod_second = []
        gen_all_card_other = []
        card_with_is_use = []
        all_data_for_critic = []
        
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
        all_data_for_critic_second = []
        #if iteration % 100 == 0:
        #    model = model2
        for n in range(n_games_per_update):
            card_deck_1, card_deck_2 = card_deck.card_deck_for_two()
        
            player1 = player.Player(card_deck_1)
            player2 = player.Player(card_deck_2)
            
            
            only_drop = False
            who_win = -1
            current_rewards = []
            current_rewards_second = []
            
            for i in range(n_max_steps):
                player1.get_new_resource()
                while True:
                    action_val = gen_array(model, player1, player2)  
                    
                    action_val = action_val[0]                    
                    
                    is_use, card_to_move = choose_move_from_array(action_val, player1, only_drop)
                    
                    if is_use:
                        card_with_is_use.append(cards.id_of(card_to_move))
                    else:
                        card_with_is_use.append(len(cards.all_cards) + cards.id_of(card_to_move))
                    
                    lt = []
                    lt.extend(gen_array_input(player1, player2)[0])
                    lt.extend(gen_my_all_card(player1)[0])
                    lt.extend(player1.card_deck.to_array()[0])
                    lt.extend(gen_my_all_card(player2)[0])
                    lt.extend(player2.card_deck.to_array()[0])
                    all_data_for_critic.append(lt)
    
                    if iteration % 1 == 0 and n == 0 and i == 10:
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
                        print('вероятность победы:', (critic.predict([all_data_for_critic[0]]) + 1) / 2)
                        for i in range(len(arr)):
                            print(arr[i][0], arr[i][1])
                        print('\n\n')


                                                        
                    only_drop = False
                    next_move_too = False
                    if is_use:
                        next_move_too, only_drop = card_to_move.use(player1, player2)
                        if player1.win(player2):
                            who_win = 1
                            current_rewards.append(player1.tower - player2.tower)
                            break
                    else:
                        player1.drop(card_to_move)
                        
                        
                    current_rewards.append(player1.tower - player2.tower)
                        
                    if not next_move_too:
                        break
                        
                if player1.win(player2):
                    break
                    
                only_drop = False
                next_move_too = False
                player2.get_new_resource()
                while True:
                    #is_use, card_to_move = nextCard(player2, player1)
                    
                    
                    action_val = gen_array(model, player2, player1)
                    action_val = action_val[0]
                    #print(action_val)
                    is_use, card_to_move = choose_move_from_array(action_val, player2, only_drop)
                    if is_use:
                        card_with_is_use_second.append(cards.id_of(card_to_move))
                    else:
                        card_with_is_use_second.append(len(cards.all_cards) + cards.id_of(card_to_move))
                    
                    lt = []                    
                    lt.extend(gen_array_input(player2, player1)[0])
                    lt.extend(gen_my_all_card(player2)[0])
                    lt.extend(player2.card_deck.to_array()[0])
                    lt.extend(gen_my_all_card(player1)[0])
                    lt.extend(player1.card_deck.to_array()[0])
                    all_data_for_critic_second.append(lt)
                    
                        
                    next_move_too = False
                    only_drop = False
                    if is_use:
                        next_move_too, only_drop = card_to_move.use(player2, player1)
                        if player2.win(player1):
                            who_win = 2
                            current_rewards_second.append(player1.tower - player2.tower)
                            if is_use:
                                #current_gradients_second.append(gradients_val)
                                pass
                            break
                    else:
                        player2.drop(card_to_move)
                    current_rewards_second.append(player1.tower - player2.tower)    
                    if not next_move_too:
                        break
                        
                if player2.win(player1):
                    break     
                               
            if who_win == 1 or player1.tower > player2.tower:
                if n == 0:
                    print('win first')
                win_ai += 1
                all_rewards.extend([1 for i in range(len(current_rewards))])
                
                all_rewards_second.extend([-1 for i in range(len(current_rewards_second))])
                
                game_before_end.extend([len(current_rewards) - i for i in range(len(current_rewards))])
                game_before_end_second.extend([len(current_rewards_second) - i for i in range(len(current_rewards_second))])
            #elif who_win == 2 or player1.tower < player2.tower:
            else:
                if n == 0:
                    print('win second')
                win_bot += 1
                all_rewards_second.extend([1 for i in range(len(current_rewards_second))])
                all_rewards.extend([-1 for i in range(len(current_rewards))])
                game_before_end.extend([len(current_rewards) - i for i in range(len(current_rewards))])
                game_before_end_second.extend([len(current_rewards_second) - i for i in range(len(current_rewards_second))])  
                
            if n != 0 and n % 20 == 0:    
                print('\r{} {}   {} %             '.format(iteration, n, (win_ai) / (win_ai + win_bot) * 100), end='')
            
        all_data_for_critic.extend(all_data_for_critic_second)   
        new_all_data_for_critic = np.asarray(all_data_for_critic)
        #new_all_data_for_critic = np.zeros((len(all_data_for_critic), len(all_data_for_critic[0])))
        #for i in range(len(all_data_for_critic)):
        #    for j in range(len(all_data_for_critic[0])):
        #        new_all_data_for_critic[i, j] = all_data_for_critic[i][j]
        
        all_rewards.extend(all_rewards_second)

        new_all_rewards = np.asarray(all_rewards)

        print('nn error:', mean_squared_error(critic.predict(new_all_data_for_critic), new_all_rewards))

        param = {'objective' : 'regression', 'learning_rate' : 0.1}
        param['metric'] = 'mse'
        train_data = lgb.Dataset(new_all_data_for_critic[:len(new_all_data_for_critic) // 10], label=new_all_rewards[:len(new_all_data_for_critic) // 10])
        test_data = lgb.Dataset(new_all_data_for_critic[-len(new_all_data_for_critic) // 10:], label=new_all_rewards[-len(new_all_data_for_critic) // 10:])
        critic = lgb.train(param, train_data, 1000, init_model=critic, valid_sets=test_data, early_stopping_rounds=1)
        critic.save_model('new_model_critic.txt')

