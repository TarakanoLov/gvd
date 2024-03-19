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
    x = Dense(64, activation='selu')(board_input)
    x = Dense(64, activation='selu')(x)
    
    action_input = Input(shape=(34 * 3 * 2,), name='action_input')
    
    policy_output = Multiply()([action_input, Dense(34 * 3 * 2, activation='tanh')(x)])
    

    model = Model(inputs=[board_input, action_input], outputs=policy_output)
    opt = Nadam(learning_rate=0.001)
    model.compile(loss='mse', optimizer=opt)
    return model
    
with open('my_models/current_model/new_all_game_situation_scaller.pkl', 'rb') as file:
    new_all_game_situation_scaller = pickle.load(file)
    

class Agent(player.Player):
    n_inputs = 2 + 2 + 6 + 6
    n_outputs = 34 * 3 * 2
    is_load = False
    
    def nextCard(self, other, only_drop=False):
        if not Agent.is_load:
           Agent.is_load = True
           Agent.model = make_model()
           Agent.model.load_weights('my_models/current_model/variants/model.h5')
        
        action_val = gen_array(Agent.model, self, other)
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
        new_all_game_situation = new_all_game_situation_scaller.transform(new_all_game_situation)
        
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
    
    def gen_array_input(self, other):
        arr = np.zeros((1, 2 + 2 + 6 + 6))
        arr[0][0] = self.tower
        arr[0][1] = self.wall
        arr[0][2] = other.tower
        arr[0][3] = other.wall
        arr[0][4] = self.mine
        arr[0][5] = self.monastery
        arr[0][6] = self.barracks
        arr[0][7] = self.ore
        arr[0][8] = self.mana
        arr[0][9] = self.squad
        arr[0][10] = other.mine
        arr[0][11] = other.monastery
        arr[0][12] = other.barracks
        arr[0][13] = other.ore
        arr[0][14] = other.mana
        arr[0][15] = other.squad
        return arr
    
    def gen_array(self, other):
        return Agent.model.predict([new_all_game_situation_scaller.transform(self.gen_array_input(other)), self.gen_my_all_card()], verbose=0)

    def gen_my_all_card(self):
        result = np.zeros((1, 34 * 3 * 2))
        for one_card in self.cards:
            if one_card.is_can_use(self):
                result[0][cards.id_of(one_card)] = 1
            result[0][len(cards.all_cards) + cards.id_of(one_card)] = 1
        return result