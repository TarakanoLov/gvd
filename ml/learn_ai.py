import sys
sys.path.insert(0, '..')

import random

import tensorflow as tf
import numpy as np
import pickle

import my_model
from base_game import game
from base_game import player
from base_game import cards
from base_game import card_deck
import agent
import helpers

from my_models.current_model_v2.policy import Agent as CurrentModel
from my_models.random_forest_v3.policy import Critic

n_games_per_update = 100
n_max_steps = 1000

critic_data_x = []
critic_data_y = []

actor_data_x = [[] for i in range(204)]
actor_data_y = [[] for i in range(204)]

def isclose(a, b, abs_tol=0.001):
    return abs(a-b) <= abs_tol
    
def one_move_logic(player1, player2, card_with_is_use, card_deck_hod, all_game_situation, card_to_use, gen_all_card_other, current_rewards, n, i):
    action_val, base = player1.make_predict(player2)                   
                    
    is_use, card_to_move = helpers.choose_move_from_array(action_val, player1, False)
    
    if is_use:
        card_with_is_use.append(cards.id_of(card_to_move))
    else:
        card_with_is_use.append(len(cards.all_cards) + cards.id_of(card_to_move))
    
    
    card_deck_hod.append(np.concatenate([player1.card_deck.to_array(player1), player2.card_deck.to_array(player2)], axis=0))
    all_game_situation.append(player1.gen_array_input(player2)[0])
    card_to_use.append(player1.gen_my_all_card()[0])
    gen_all_card_other.append(player2.gen_my_all_card()[0])
       
    if n == 0 and i == 10:
        helpers.print_for_learn(action_val, player1, player2, critic, all_game_situation, card_to_use, gen_all_card_other, card_deck_hod)


    current_rewards.append(player1.tower - player2.tower)                                  
    only_drop = False
    next_move_too = False
    if is_use:
        next_move_too, only_drop = card_to_move.use(player1, player2)
    else:
        player1.drop(card_to_move)
        

def calc_reward(current_rewards, win):
    c = 1/(len(current_rewards) + 1)
    if win == 1:
        return [1 - c*(len(current_rewards) - i) for i in range(len(current_rewards))]
    elif win == -1:
        return [-1 + c*(len(current_rewards) - i) for i in range(len(current_rewards))]

if __name__ == '__main__':
    critic = Critic()
    more_data = True
    
    for iteration in range(1000001):
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
            rc1, rc2 = card_deck.card_deck_for_two()
            player1 = CurrentModel(rc1)
            player2 = CurrentModel(rc2)
            
            current_rewards = []
            current_rewards_second = []
            
            for i in range(n_max_steps):
                player1.get_new_resource()
                one_move_logic(player1, player2, card_with_is_use, card_deck_hod, all_game_situation, card_to_use, gen_all_card_other, current_rewards, n, i)
                        
                if player1.game_ended(player2):
                    break
                    

                player2.get_new_resource()
                one_move_logic(player2, player1, card_with_is_use_second, card_deck_hod_second, all_game_situation_second, card_to_use_second, gen_all_card_other_second, current_rewards_second, n, i)
                
                if player2.game_ended(player1):
                    break

            if i == n_max_steps - 1:
                continue
                
            if player1.tower >= 50 or player2.tower <= 0:
                assert player2.tower <= 0 or player1.tower >= 50
                win_ai += 1
                all_rewards.extend(calc_reward(current_rewards, 1))
                all_rewards_second.extend(calc_reward(current_rewards_second, -1))
                
                game_before_end.extend([len(current_rewards) - i for i in range(len(current_rewards))])
                game_before_end_second.extend([len(current_rewards_second) - i for i in range(len(current_rewards_second))])
            else:
                assert player2.tower >= 50 or player1.tower <= 0
                win_bot += 1
                all_rewards_second.extend(calc_reward(current_rewards_second, 1))
                all_rewards.extend(calc_reward(current_rewards, -1))
                
                game_before_end.extend([len(current_rewards) - i for i in range(len(current_rewards))])
                game_before_end_second.extend([len(current_rewards_second) - i for i in range(len(current_rewards_second))])
                
            if n != 0 and n % 10 == 0:
                print('\r{}  {}%  {} %             '.format(iteration, n / n_games_per_update * 100, (win_ai) / (win_ai + win_bot) * 100), end='')
            
            
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
        sss = critic.predict(np.concatenate([new_all_game_situation, new_card_deck_hod], axis=1))
        cp_critic_predict = sss
        sss = helpers.calclulate_target_to_model(sss, new_all_rewards, game_before_end)
        #sss = helpers.new_calclulate_target_to_model(sss, new_all_rewards, game_before_end)
        
        # new_critic_target = np.zeros((len(sss), 2), dtype=np.float)
        # step = 5
        # for i in range(len(sss)):
            # new_critic_target[i][0] = new_all_rewards[i]
            # if i >= len(sss) - step or game_before_end[i] <= step:
                # if new_all_rewards[i] > 0:
                    # new_critic_target[i][1] = 0.95
                # else:
                    # new_critic_target[i][1] = -0.95
            # else:
                # new_critic_target[i][1] = new_all_rewards[i + step]
        
        reward_for_critic = np.clip(new_all_rewards, -1, 1)

        new_action_val_array = np.zeros((len(sss), 204))
        new_card_to_use = np.zeros((len(sss), 204))
        for i in range(len(sss)):
            new_action_val_array[i][card_with_is_use[i]] = sss[i]
            new_card_to_use[i][card_with_is_use[i]] = 1
        
        #CurrentModel.fit(new_all_game_situation, new_card_to_use, new_action_val_array)
        #ok_index = np.logical_and(cp_critic_predict > -0.7, cp_critic_predict < 0.7)
        #CurrentModel.fit(new_all_game_situation[ok_index], new_card_to_use[ok_index], new_action_val_array[ok_index])
        
        # if more_data:
            # for i in range(len(sss)):
                # actor_data_x[card_with_is_use[i]].append([new_all_game_situation[i]])
                # actor_data_y[card_with_is_use[i]].append([sss[i]])

        # #if iteration == 2 or iteration == 100 or iteration == 500:
        # if iteration == 2 or iteration == 1500:
            # for i in range(204):
                # actor_input = np.concatenate(actor_data_x[i], axis=0)
                # actor_output = np.concatenate(actor_data_y[i], axis=0)
                # with open(f'train_data/current_train/x_train{i}_{iteration}.pkl', 'wb') as f:
                   # pickle.dump(actor_input, f)
                # with open(f'train_data/current_train/y_train{i}_{iteration}.pkl', 'wb') as f2:
                   # pickle.dump(actor_output, f2)
                   
            # actor_data_x = [[] for i in range(204)]
            # actor_data_y = [[] for i in range(204)]
            # if iteration == 1500:
                # more_data = False
        
        
        
        base_inp = np.concatenate([new_all_game_situation, new_card_deck_hod], axis=1)
        l = int(len(base_inp)*0.1)
        idx = np.random.randint(len(base_inp), size=l)
        critic_data_x.append(base_inp[idx, :])
        critic_data_y.append(new_all_rewards[idx])
        if iteration == 2 or iteration % 600 == 0:
            cr_input = np.concatenate(critic_data_x, axis=0)
            cr_output = np.concatenate(critic_data_y, axis=0)
            #with open(f'x_train{iteration}.pkl', 'wb') as f:
            #   pickle.dump(cr_input, f)
            np.savez_compressed(f'x_train{iteration}.npz', cr_input)
            #with open(f'y_train{iteration}.pkl', 'wb') as f2:
            #   pickle.dump(cr_output, f2)
            np.savez_compressed(f'y_train{iteration}.npz', cr_output)
            critic_data_x = []
            critic_data_y = []
        #critic.fit(base_inp, reward_for_critic, shuffle=True, batch_size=128, epochs=1, validation_split=0.9)