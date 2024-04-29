from keras.models import Model
from keras.layers import Dense, Input, concatenate, Flatten, Multiply, Dropout, BatchNormalization, LeakyReLU, Softmax, Add, Lambda, Reshape
from keras.optimizers import SGD, RMSprop, Adam, Nadam

import numpy as np
import pickle

from base_game import cards
from base_game import player
from ml import helpers

def make_model():
    n_inputs = 2 + 2 + 6 + 6 #+ (34 + 34 + 34) #* 2
    
    board_input = Input(shape=(n_inputs,), name='board_input')
    x = BatchNormalization()(board_input)
    x = Dense(16, activation='selu')(x)
    x = Dense(16, activation='selu')(x)
    
    action_input = Input(shape=(34 * 3 * 2,), name='action_input')
    
    policy_output = Multiply()([action_input, Dense(34 * 3 * 2, activation='tanh')(x)])
    

    model = Model(inputs=[board_input, action_input], outputs=policy_output)
    opt = Nadam(learning_rate=0.00001)
    model.compile(loss='mse', optimizer=opt)
    return model

class Agent(player.Player):
    n_inputs = 2 + 2 + 6 + 6
    n_outputs = 34 * 3 * 2
    is_load = False
    
    def nextCard(self, other, only_drop=False):
        if not Agent.is_load:
           Agent.is_load = True
           Agent.model = make_model()
           Agent.model.load_weights('my_models/current_model/variants/model.h5')
           with open('my_models/current_model/new_all_game_situation_scaller.pkl', 'rb') as file:
               Agent.new_all_game_situation_scaller = pickle.load(file)
        
        action_val = self.gen_array(other)
        action_val = action_val[0]    
        
        return helpers.choose_move_from_array(action_val, self, only_drop, 0.0)
    
    def nextMove(self, other, only_drop=False):
        is_use, card = self.nextCard(other, only_drop)

        if is_use:
            return card.use(self, other)
        else:
            self.drop(card)
            return (False, False)
    
    def fit(new_all_game_situation, new_card_to_use, new_action_val_array):
        new_all_game_situation = Agent.new_all_game_situation_scaller.transform(new_all_game_situation)
        
        Agent.model.fit([new_all_game_situation, new_card_to_use], new_action_val_array, batch_size=64, epochs=1, shuffle=True)
        Agent.model.save_weights('my_models/current_model/variants/model.h5')
        
    def make_predict(self, other):
        if not Agent.is_load:
           Agent.is_load = True
           Agent.model = make_model()
           Agent.model.load_weights('my_models/current_model/variants/model.h5')

        action_val = self.gen_array(other)  
        action_val = action_val[0]

        return action_val, action_val
    
    def gen_array(self, other):
        with open('my_models/current_model/new_all_game_situation_scaller.pkl', 'rb') as file:
               Agent.new_all_game_situation_scaller = pickle.load(file)
        return Agent.model.predict([Agent.new_all_game_situation_scaller.transform(self.gen_array_input(other)), self.gen_my_all_card()], verbose=0)