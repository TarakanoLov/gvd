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

from my_models.current_model.policy import Agent as CurrentModel
from my_models.old_critic.policy import Critic

n_games_per_update = 100
n_max_steps = 1000

def isclose(a, b, abs_tol=0.001):
    return abs(a-b) <= abs_tol

if __name__ == '__main__':
    critic = Critic()
    
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
                for gggg in range(1):
                    action_val, base = player1.make_predict(player2)                   
                    
                    is_use, card_to_move = helpers.choose_move_from_array(action_val, player1, False)
                    
                    if is_use:
                        card_with_is_use.append(cards.id_of(card_to_move))
                    else:
                        card_with_is_use.append(len(cards.all_cards) + cards.id_of(card_to_move))
                    
                    card_deck_hod.append(np.concatenate([player1.card_deck.to_array(), player2.card_deck.to_array()], axis=0))
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
                        
                        
                    if not next_move_too:
                        break
                        
                if player1.game_ended(player2):
                    break
                    
                only_drop = False
                next_move_too = False
                player2.get_new_resource()
                for gggg in range(1):
                    action_val, base = player2.make_predict(player1)

                    is_use, card_to_move = helpers.choose_move_from_array(action_val, player2, only_drop)
                    if is_use:
                        card_with_is_use_second.append(cards.id_of(card_to_move))
                    else:
                        card_with_is_use_second.append(len(cards.all_cards) + cards.id_of(card_to_move))
                    all_game_situation_second.append(player2.gen_array_input(player1)[0])
                    card_to_use_second.append(player2.gen_my_all_card()[0])
                    card_deck_hod_second.append(np.concatenate([player2.card_deck.to_array(), player1.card_deck.to_array()], axis=0))
                    action_val_array_second.append(action_val - base)
                    gen_all_card_other_second.append(player1.gen_my_all_card()[0])
                    
                        
                    current_rewards_second.append(player1.tower - player2.tower)    
                    next_move_too = False
                    only_drop = False
                    if is_use:
                        next_move_too, only_drop = card_to_move.use(player2, player1)
                    else:
                        player2.drop(card_to_move)
                    
                    if not next_move_too:
                        break
                        
                if player2.game_ended(player1):
                    break     
                               
            if player1.tower >= 50 or player2.tower <= 0:
                assert player2.tower <= 0 or player1.tower >= 50
                win_ai += 1
                all_rewards.extend([0.9 for i in range(len(current_rewards))])
                all_rewards_second.extend([-0.9 for i in range(len(current_rewards_second))])
                
                game_before_end.extend([len(current_rewards) - i for i in range(len(current_rewards))])
                game_before_end_second.extend([len(current_rewards_second) - i for i in range(len(current_rewards_second))])
            else:
                assert player2.tower >= 50 or player1.tower <= 0
                win_bot += 1
                all_rewards_second.extend([0.9 for i in range(len(current_rewards_second))])
                all_rewards.extend([-0.9 for i in range(len(current_rewards))])
                game_before_end.extend([len(current_rewards) - i for i in range(len(current_rewards))])
                game_before_end_second.extend([len(current_rewards_second) - i for i in range(len(current_rewards_second))])
                
            if n != 0 and n % 100 == 0:
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
        sss = critic.predict(np.concatenate([new_all_game_situation, new_card_to_use, new_gen_all_card_other, new_card_deck_hod], axis=1))
        
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

        reward_for_critic = new_all_rewards
        
        new_action_val_array = np.zeros((len(sss), 204))
        new_card_to_use = np.zeros((len(sss), 204))
        for i in range(len(sss)):
            new_action_val_array[i][card_with_is_use[i]] = sss[i]
            new_card_to_use[i][card_with_is_use[i]] = 1
        
        callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=1)
        l = int(len(new_all_game_situation) * 0.8)
            
        CurrentModel.fit(new_all_game_situation, new_card_to_use, new_action_val_array)
        
        ### critic
        base_inp = np.concatenate([new_all_game_situation, new_card_to_use, new_gen_all_card_other, new_card_deck_hod], axis=1)
        print('точность критика =', np.isclose(critic.predict(base_inp).reshape(1, -1), reward_for_critic.reshape(1, -1), 0, 0.89).sum() / len(base_inp) * 100, '%')
        l = int(len(base_inp)*0.8)
        idx = np.random.randint(l, size=l // 10)
        inp = base_inp[idx, :]
        #print(reward_for_critic)
        #if iteration % 10 == 0:
        #    print('input for critic, input = ', critic_scaller.transform(inp[0].reshape(1, -1)), 'output =', reward_for_critic[0])
        #    critic.fit(inp, reward_for_critic[idx], shuffle=True, batch_size=64, epochs=1)
        
        #critic.fit(inp, reward_for_critic[idx], shuffle=True, batch_size=64, epochs=1)