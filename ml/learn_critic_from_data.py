import random
import os
import json

# from keras.models import Model
# from keras.layers import Dense, Input, concatenate, Flatten, Multiply, Dropout
# from keras.optimizers import SGD
# from keras.callbacks import EarlyStopping, ModelCheckpoint
# import keras.callbacks as cb

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


import critic_model

import numpy as np

import game
import player
import cards
import card_deck
import agent


if __name__ == '__main__':
    # 2 - башня и стена
    # 6 - ресурсы и их прирост
    # 34 + 34 + 34 - все карты в колоде
    
    model = critic_model.make_critic_model()

    #model.load_weights("model_from_data.h5")

    
    with open('data.txt') as json_file:
         data = json.load(json_file)
    
    
    data = data['data']
        
        
        
    new_all_game_situation = np.zeros((len(data), len(data[0]['array_input'][0])))
    for i in range(len(data)):
        new_all_game_situation[i] = data[i]['array_input'][0]
                

        
        
    new_card_to_use = np.zeros((len(data), len(data[0]['gen_my_all_card'][0])))
    for i in range(len(data)):
        new_card_to_use[i] = data[i]['gen_my_all_card'][0]
    new_card_to_use = np.ones((len(data), len(data[0]['gen_my_all_card'][0])))
        
        
        
        
        
        
    new_all_rewards = np.zeros((len(data), 1))
    for i in range(len(data)):
        new_all_rewards[i] = data[i]['reward']
             
    X_train, X_test, y_train, y_test = train_test_split(new_all_game_situation, new_all_rewards.ravel(), test_size=0.99)
    #callbacks = [cb.EarlyStopping(monitor = 'val_loss', patience = 6),
    #             ModelCheckpoint('model_critic_from_data.h5', monitor='val_loss', save_best_only=True, mode='min') ]
        
    X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.1)
    #model.fit([new_all_game_situation, new_card_to_use], new_all_rewards, validation_split=0.1, epochs=10000, batch_size=1024, callbacks = callbacks)
    model.fit(X_train, y_train)
    #model.save_weights("model_from_data.h5") 
    print(mean_squared_error(y_test, model.predict(X_test)))
        
        
        
        
        