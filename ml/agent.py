import random
import numpy as np
import copy
import json
from joblib import dump, load

json_data = {'data' : []}

from keras.models import Model
from keras.layers import Dense, Input, concatenate, Flatten, Multiply
from keras.optimizers import SGD

import my_model

from base_game import cards
import learn_ai
from base_game import card_deck
from base_game import player
from base_game import game

from my_models.old_model_71.policy import Agent as OldAIagent
from my_models.new_model_78.policy import Agent as myNewAIaget

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
        for i, el in enumerate(arr_result):
            if el[0]:
                print(i, el[1])
            else:
                print(i, 'Сброс', el[1])
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
     


class NewAIagent(player.Player):
    n_outputs = (34 + 34 + 34) * 2
    def get_json(self):
        return json_data
    def nextCard(self, other, only_drop=False):
        if not NewAIagent.is_load:
            NewAIagent.is_load = True

            NewAIagent.model = my_model.make_model_test()
            NewAIagent.model.load_weights('actor.h5')
            
        action_val = learn_ai.gen_array(NewAIagent.model, self, other)
        action_val = action_val[0]    
        

        if False:        
            arr = []
            for i in range(self.n_outputs):
                if cards.all_cards[i % len(cards.all_cards)] in self.cards:
                    if i < len(cards.all_cards):
                        if cards.all_cards[i % len(cards.all_cards)].is_can_use(self):
                            arr.append((cards.all_cards[i].name, action_val[i]))
                    else:
                        arr.append(('сброс ' + cards.all_cards[i % len(cards.all_cards)].name, action_val[i]))
            arr.sort(key=lambda x : x[1])
            print('\n\n')
            print(self)
            print('\n\n')
                            
            for i in range(len(arr)):
               print(arr[i][0], arr[i][1])
            print('\n\n')

        return learn_ai.choose_move_from_array(action_val, self, only_drop, 0.0)
        
    is_load = False
    
    def nextMove(self, other, only_drop=False):
        is_use, card = self.nextCard(other, only_drop)
        #print(is_use, card)
        if is_use:
            return card.use(self, other)
        else:
            self.drop(card)
            return (False, False)
            
class AccamulateNewAIagent(player.Player):
    n_outputs = (34 + 34 + 34) * 2

    def nextCard(self, other, only_drop=False):
        if not NewAIagent.is_load:
            NewAIagent.is_load = True
            # NewAIagent.model = my_model.make_model()
            NewAIagent.model = my_model.make_model_74_5()
            NewAIagent.model.load_weights("model_74_5/model.h5")
            
        # q_value, action_val = NewAIagent.model.predict([learn_ai.gen_array_input(self, other), learn_ai.gen_my_all_card(self)])
        # q_value = q_value[0]
        # action_val = action_val[0]    

        # q_value2, action_val2 = NewAIagent.model2.predict([learn_ai.gen_array_input(self, other), learn_ai.gen_my_all_card(self)])
        # q_value2 = q_value2[0]
        # action_val2 = action_val2[0]         
        
        action_val3 = NewAIagent.model.predict([learn_ai.gen_array_input(self, other), learn_ai.gen_my_all_card(self)])
        action_val3 = action_val3[0]   

        # q_value4, action_val4 = NewAIagent.model4.predict([learn_ai.gen_array_input(self, other), learn_ai.gen_my_all_card(self)])
        # q_value4 = q_value4[0]
        # action_val4 = action_val4[0]         
        
        #action_val = action_val + action_val2 + action_val3 + action_val4
        global json_data
        if random.random() <= 0.1:
            json_data['data'].append({'array_input' : learn_ai.gen_array_input(self, other).tolist(),
                                 'gen_my_all_card' : learn_ai.gen_my_all_card(self).tolist(),
                                 'action_val' : action_val3.tolist(),
                                 'name' : self.name, 
                                 'gen_all_card_second' : learn_ai.gen_my_all_card(other).tolist(),
                                 'card_deck' : self.card_deck.to_array().tolist()})
        #print('aaaa ', len(json_data['data']))
        if False:        
            arr = []
            for i in range(self.n_outputs):
                if i < len(cards.all_cards):
                    #if cards.all_cards[i % len(cards.all_cards)].is_can_use(self):
                    arr.append((cards.all_cards[i].name, action_val[i]))
                else:
                    arr.append(('сброс ' + cards.all_cards[i % len(cards.all_cards)].name, action_val[i]))
            arr.sort(key=lambda x : x[1])
            print('\n\n')
            print(self)
            print('\n\n')
                            
            for i in range(len(arr)):
               print('\'', arr[i][0], '\',', sep='')#, arr[i][1])
            print('\n\n')
            print(0/0)
        return learn_ai.choose_move_from_array(action_val3, self, only_drop, 0.0)
        
    is_load = False
    def get_json(self):
        return json_data
    def nextMove(self, other, only_drop=False):
        is_use, card = self.nextCard(other, only_drop)
        #print(is_use, card)
        if is_use:
            return card.use(self, other)
        else:
            self.drop(card)
            return (False, False)
          
        
class RandomForestAgent(player.Player):
    n_outputs = (34 + 34 + 34) * 2
    def get_json(self):
        return json_data
    def nextCard(self, other, only_drop=False):
        if not RandomForestAgent.is_load:
            RandomForestAgent.is_load = True
            RandomForestAgent.model = load('actor.joblib') 

            
        action_val = RandomForestAgent.model.predict(np.concatenate([learn_ai.gen_array_input(self, other),
                                            learn_ai.gen_my_all_card(self)], axis=1))

        if False:        
            arr = []
            for i in range(self.n_outputs):
                if cards.all_cards[i % len(cards.all_cards)] in self.cards:
                    if i < len(cards.all_cards):
                        if cards.all_cards[i % len(cards.all_cards)].is_can_use(self):
                            arr.append((cards.all_cards[i].name, action_val[0][i]))
                    else:
                        arr.append(('сброс ' + cards.all_cards[i % len(cards.all_cards)].name, action_val[0][i]))
            arr.sort(key=lambda x : x[1])
            print('\n\n')
            print(self)
            print('\n\n')
                            
            for i in range(len(arr)):
               print(arr[i][0], arr[i][1])
            print('\n\n')

        return learn_ai.choose_move_from_array(action_val[0], self, only_drop, 0.0)
        
    is_load = False
    
    def nextMove(self, other, only_drop=False):
        is_use, card = self.nextCard(other, only_drop)
        #print(is_use, card)
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
    
    
    make_ai_agent = lambda card_deck : NewAIagent(card_deck)
    #make_ai_agent = lambda card_deck : OldAIagent(card_deck)
    #make_ai_agent = lambda card_deck : myNewAIaget(card_deck)
    
    #make_random_agent = lambda card_deck : OldAIagent(card_deck)
    make_random_agent = lambda card_deck : CleverRandomAgent(card_deck)
    
    
    for i in range(10000):
        this_card_deck = card_deck.Random_card_deck()
        
        first_batl = copy.deepcopy(this_card_deck)

        ai_agent = make_ai_agent(first_batl)
        random_agent = make_random_agent(first_batl)
        
        this_game = game.Game(ai_agent, random_agent)
        #print(json_data)
        if this_game.startPlay() == 0:
            win_ai_first += 1
        else:
            win_random_first += 1
        
        second_batl = this_card_deck
        random_agent = make_random_agent(second_batl)
        ai_agent = make_ai_agent(second_batl)
        
        this_game = game.Game(random_agent, ai_agent)

        if this_game.startPlay() == 0:
            win_random_second += 1
        else:
            win_ai_second += 1
        
        if i != 0 and i % 100 == 0:
            win_ai = win_ai_first + win_ai_second
            win_random = win_random_first + win_random_second
            print('\rIteration: {}, winrate: {}%\tFirst: {}%, second {}%'.format(i, win_ai/(win_ai + win_random) * 100, win_ai_first/(win_ai_first + win_random_first) * 100, win_ai_second/(win_ai_second + win_random_second) * 100), end='')
 