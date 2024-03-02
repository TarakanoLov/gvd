import random
import os
import json

from keras.models import Model
from keras.layers import Dense, Input, concatenate, Flatten, Multiply, Dropout
from keras.optimizers import SGD
from keras.callbacks import EarlyStopping, ModelCheckpoint
import keras.callbacks as cb

import my_model

import tensorflow as tf

import numpy as np

import game
import player
import cards
import card_deck
import agent


n_inputs = 2 + 2 + 6 + 6 #+ (34 + 34 + 34) #* 2
n_games_per_update = 1000
n_max_steps = 100
n_iterations = 1000001
save_iterations = 100
discount_rate = 0.999
win_ai = 0
win_bot = 0
n_outputs = 1#(34 + 34 + 34) * 2


def read_from_file(name):
    with open(name) as json_file:
         data = json.load(json_file)
    
    
    
    data = data['data']
        
        
        
    new_all_game_situation = np.zeros((len(data), len(data[0]['array_input'][0])))
    for i in range(len(data)):
        new_all_game_situation[i] = data[i]['array_input'][0]
                

        
        
    new_card_to_use = np.zeros((len(data), len(data[0]['gen_my_all_card'][0])))
    #for i in range(len(data)):
    #    new_card_to_use[i] = data[i]['gen_my_all_card'][0]
    #new_card_to_use = np.ones((len(data), len(data[0]['gen_my_all_card'][0])))
        
        
        
        
        
        
    new_all_rewards = np.zeros((len(data), 1))
    for i in range(len(data)):
        new_all_rewards[i] = data[i]['reward']
    
    #print(new_all_rewards[:100])        
           
    new_action_val_array = np.zeros((len(data), len(data[0]['action_val'])))
    for i in range(len(data)):
        #for j in range(len(data[0]['action_val'])):
        #    new_action_val_array[i][j] = data[i]['action_val'][j] 
        ind = np.argmax(data[i]['action_val'])
        new_action_val_array[i][ind] = new_all_rewards[i]
        new_card_to_use[i][ind] = 1
        #print(new_action_val_array[0].sum())  
    return new_all_game_situation, new_card_to_use, new_action_val_array

if __name__ == '__main__':
    # 2 - башня и стена
    # 6 - ресурсы и их прирост
    # 34 + 34 + 34 - все карты в колоде
    
    model = my_model.make_model_test()

    #model.load_weights("model_from_data.h5")

    new_all_game_situation, new_card_to_use, new_action_val_array = read_from_file('data_big_4000.txt')
    new_all_game_situation_1, new_card_to_use_1, new_action_val_array_1 = read_from_file('data_big_8000.txt')
    new_all_game_situation_2, new_card_to_use_2, new_action_val_array_2 = read_from_file('data_big_12000.txt')
    new_all_game_situation_3, new_card_to_use_3, new_action_val_array_3 = read_from_file('data_big_16000.txt')
    
    new_all_game_situation = np.concatenate([new_all_game_situation, new_all_game_situation_1, new_all_game_situation_2, new_all_game_situation_3], axis=0)
    # new_all_game_situation.extend(new_all_game_situation_1)
    # new_all_game_situation.extend(new_all_game_situation_2)
    # new_all_game_situation.extend(new_all_game_situation_3)
    
    new_card_to_use = np.concatenate([new_card_to_use, new_card_to_use_1, new_card_to_use_2, new_card_to_use_3], axis=0)
    # new_card_to_use.extend(new_card_to_use_1)
    # new_card_to_use.extend(new_card_to_use_2)
    # new_card_to_use.extend(new_card_to_use_3)
    new_action_val_array = np.concatenate([new_action_val_array, new_action_val_array_1, new_action_val_array_2, new_action_val_array_3], axis=0)
    # new_action_val_array.extend(new_action_val_array_1)
    # new_action_val_array.extend(new_action_val_array_2)
    # new_action_val_array.extend(new_action_val_array_3)
    
    
    test_new_all_game_situation, test_new_card_to_use, test_new_action_val_array = read_from_file('data_big_20000.txt')   
    
    callbacks = [#cb.EarlyStopping(monitor = 'val_multiply_1_loss', patience = 6),
                 cb.EarlyStopping(monitor = 'val_loss', patience = 6),
                 ModelCheckpoint('model_from_data.h5', monitor='val_loss', save_best_only=True, mode='auto') ]
    #for i in range(10):
    model.fit([new_all_game_situation, new_card_to_use], new_action_val_array, epochs=1024, shuffle=True, batch_size=1024, callbacks = callbacks, validation_data=([test_new_all_game_situation, test_new_card_to_use], test_new_action_val_array))
        
    #model.save_weights("model_from_data.h5") 
        
        
        
        
        
        