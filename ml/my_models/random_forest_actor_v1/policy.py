import numpy as np
import pickle

from base_game import cards
from base_game import player
from ml import helpers

import lightgbm as lgb

class Agent(player.Player):
    n_inputs = 2 + 2 + 6 + 6
    n_outputs = 34 * 3 * 2
    is_load = False
    
    def nextCard(self, other, only_drop=False):
        if not Agent.is_load:
           Agent.is_load = True
           Agent.models = []
           for i in range(204):
               Agent.models.append(lgb.Booster(model_file=f'my_models/random_forest_actor_v1/variants/v3/model{i}.txt'))
        
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
        None
        
    def make_predict(self, other):
        if not Agent.is_load:
           Agent.is_load = True
           Agent.models = []
           for i in range(204):
               Agent.models.append(lgb.Booster(model_file=f'my_models/random_forest_actor_v1/variants/v3/model{i}.txt'))

        action_val = self.gen_array(other)  
        action_val = action_val[0]

        return action_val, action_val
    
    def gen_array(self, other):
        input_array = np.ndarray((1, 204))
        my_cards = self.gen_my_all_card()
        for i in range(len(my_cards)):
            if my_cards[0][i]:
                input_array[i] = Agent.models[i].predict(self.gen_array_input(other))
        return input_array