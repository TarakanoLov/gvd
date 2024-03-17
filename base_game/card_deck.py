import numpy as np

import random

from . import cards

class Fake_card_deck:
    def __init__(self, cards):
        self.cards = cards.copy()

    def generate_start_cards(self):
        return [self.new_card() for _ in range(7)]
        
    def new_card(self):
        if len(self.cards) != 0:
            return self.cards.pop()
        else:
            return None

class Random_card_deck:
    def __init__(self, seed = None):
        if seed is not None:
            random.seed(seed)
        self.all_cards = cards.all_cards.copy()
        random.shuffle(self.all_cards)
        
    def generate_start_cards(self):
        return [self.new_card() for _ in range(7)]
        
    def new_card(self):
        if len(self.all_cards) != 0:
            return self.all_cards.pop()
        else:
            self.all_cards = cards.all_cards.copy()
            random.shuffle(self.all_cards)
            return self.new_card()
            
    def to_array(self):
        arr = np.full((34 * 3,), 120)
        for ind, one_card in enumerate(self.all_cards):
            arr[cards.id_of(one_card)] = len(self.all_cards) - ind - 1
        return arr
        
def card_deck_for_two():
    rcd = Random_card_deck()
    arr_cards = [rcd.new_card() for i in range(len(rcd.all_cards)//2)]
    rcd2 = Random_card_deck()
    rcd2.all_cards = arr_cards
    return rcd, rcd2