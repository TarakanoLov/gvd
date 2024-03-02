import json
from joblib import dump, load
import h5py

import my_model

import cards
import learn_ai
import card_deck
import player
import game

import agent

            
if __name__ == '__main__':
    #make_random_agent = lambda card_deck : TarakanAgent(card_deck)
    #make_random_agent = lambda card_deck : CleverRandomAgent(card_deck)
    #make_random_agent = lambda card_deck : RandomAgent(card_deck)
    make_random_agent = lambda card_deck : agent.AccamulateNewAIagent(card_deck, name='first')
    
    #make_ai_agent = lambda card_deck : RandomForestAgent(card_deck)
    #make_ai_agent = lambda card_deck : AccamulateNewAIagent(card_deck)
    #make_ai_agent = lambda card_deck : OrderAgent(card_deck)
    make_ai_agent = lambda card_deck : agent.AccamulateNewAIagent(card_deck, name='second')
    #make_ai_agent = lambda card_deck : NewAIagent(card_deck)
    #make_ai_agent = lambda card_deck : VeryCleverAIagent(card_deck)
    
    for i in range(1, 200001):
        this_card_deck = card_deck.Random_card_deck()

        ai_agent = make_ai_agent(this_card_deck)
        random_agent = make_random_agent(this_card_deck)
        
        this_game = game.Game(ai_agent, random_agent)
        this_game.startPlay()
       
        print('\rIteration: {}'.format(i), end='')
        if i % 10 == 0:
            print('dump start')
            with h5py.File('data_{}.h5'.format(i), 'w') as outfile:
                array_input, gen_my_all_card, action_val, gen_all_card_second, card_deck = agent.json_data['data'][j]['array_input'],
                                 agent.json_data['data'][j]['gen_my_all_card'],
                                 agent.json_data['data'][j]['action_val'],
                                 agent.json_data['data'][j]['gen_all_card_second'],
                                 agent.json_data['data'][j]['card_deck'] for j in range(len(agent.json_data['data']))
                array_input, gen_my_all_card, action_val, gen_all_card_second, card_deck
                    = np.ndarray(array_input), np.ndarray(gen_my_all_card), np.ndarray(action_val), np.ndarray(gen_all_card_second), np.ndarray(card_deck)
                outfile.create_dataset('array_input', data=array_input)
                outfile.create_dataset('gen_my_all_card', data=gen_my_all_card)
                outfile.create_dataset('action_val', data=action_val)
                outfile.create_dataset('gen_all_card_second', data=gen_all_card_second)
            print('dump')
            agent.json_data = {'data' : []}