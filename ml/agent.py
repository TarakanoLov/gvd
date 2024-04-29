import random
import numpy as np
import copy
import json
from joblib import dump, load

json_data = {'data' : []}

from keras.models import Model
from keras.layers import Dense, Input, concatenate, Flatten, Multiply
from keras.optimizers import SGD

import sys
sys.path.insert(0, '..')

from base_game import cards
import learn_ai
import helpers
from base_game import card_deck
from base_game import player
from base_game import game

from my_models.old_model_71.policy import Agent as OldAIagent
from my_models.new_model_78.policy import Agent as myNewAIaget

#from my_models.random_forest_actor_v1.policy import Agent as CurrentModel

from my_models.current_model_v2.policy import Agent as CurrentModel

#from my_models.current_model.policy import Agent as CurrentModel

import os
import copy

def get_json():
    print(json_data)
    return json_data


class TarakanAgent(player.Player):
    def nextCard(self, other, only_drop=False):
        arr_result = []
        for one_card in self.cards:
            if not only_drop and one_card.is_can_use(self):
                arr_result.append((1, one_card))
            arr_result.append((0, one_card))
        
        print('-----------')
        print('Я:', self)
        print('-----------')
        print('Соперник:', other)
        arr_result = sorted(arr_result, key=lambda x : x[0])
        
        for i, el in enumerate(arr_result):
            if el[0]:
                print(i, el[1].debug_str())
            else:
                print(i, 'Сброс', el[1].debug_str())
        ind = int(input())
                
        return arr_result[ind]

    def nextMove(self, other, only_drop=False):
        is_use, card = self.nextCard(other, only_drop)
        if is_use:
            return card.use(self, other)
        else:
            self.drop(card)
            return (False, False)



class RandomAgent(player.Player):
    def get_json(self):
        return json_data
    def nextCard(self, other, only_drop=False):
        arr_result = []
        for one_card in self.cards:
            if not only_drop and one_card.is_can_use(self):
                arr_result.append((1, one_card))
            arr_result.append((0, one_card))
        
        if len(arr_result) == 0:
            for one_card in self.cards:
                arr_result.append((0, one_card))
                
        return random.choices(arr_result)[0]

    def nextMove(self, other, only_drop=False):
        is_use, card = self.nextCard(other, only_drop)
        if is_use:
            return card.use(self, other)
        else:
            self.drop(card)
            return (False, False)
        
class CleverRandomAgent(player.Player):
    def get_json(self):
        return json_data
    def nextCard(self, other, only_drop=False):                   
        for one_card in reversed(self.cards):
            if not only_drop and one_card.is_can_use(self):
              return (1, one_card)
            
        return (0, self.cards[-1])

    def nextMove(self, other, only_drop=False):
        is_use, card = self.nextCard(other, only_drop)
        if is_use:
            return card.use(self, other)
        else:
            self.drop(card)
            return (False, False)
     
            
if __name__ == '__main__':
    win_ai_first = 0
    win_random_first = 0
    win_ai_second = 0
    win_random_second = 0
    
    win_first_random = False
    win_two_games_random = 0
    
    make_ai_agent = lambda card_deck : CurrentModel(card_deck)
    #make_ai_agent = lambda card_deck : OldAIagent(card_deck)
    #make_ai_agent = lambda card_deck : myNewAIaget(card_deck)
    
    #make_random_agent = lambda card_deck : OldAIagent(card_deck)
    make_random_agent = lambda card_deck : CleverRandomAgent(card_deck)
    #make_random_agent = lambda card_deck : TarakanAgent(card_deck)
    
    for i in range(10000):
        rc1, rc2 = card_deck.card_deck_for_two()
        
        cp_rc1, cp_rc2 = copy.deepcopy(rc1), copy.deepcopy(rc2)

        ai_agent = make_ai_agent(cp_rc1)
        random_agent = make_random_agent(cp_rc2)
        
        this_game = game.Game(ai_agent, random_agent)

        if this_game.startPlay() == 0:
            win_ai_first += 1
        else:
            win_random_first += 1
            win_first_random = True
        
        random_agent = make_random_agent(rc1)
        ai_agent = make_ai_agent(rc2)
        
        this_game = game.Game(random_agent, ai_agent)

        if this_game.startPlay() == 0:
            win_random_second += 1
            if win_first_random:
                win_two_games_random += 1
        else:
            win_ai_second += 1

        win_first_random = False
        
        if i != 0 and i % 100 == 0:
            win_ai = win_ai_first + win_ai_second
            win_random = win_random_first + win_random_second
            print('\rIteration: {}, winrate: {}%\tFirst: {}%, second {}%, win two games from random {}%'.format(i, win_ai/(win_ai + win_random) * 100, win_ai_first/(win_ai_first + win_random_first) * 100, win_ai_second/(win_ai_second + win_random_second) * 100, win_two_games_random/i * 100), end='')
 