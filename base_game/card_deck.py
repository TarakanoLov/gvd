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
            
    def to_array(self, player):
        arr = np.full((34 * 3,), 120)
        for ind, one_card in enumerate(self.all_cards):
            arr[cards.id_of(one_card)] = len(self.all_cards) - ind - 1
        for in_hand in player.cards:
            if in_hand.is_can_use(player):
                arr[cards.id_of(in_hand)] = -2
            else:
                arr[cards.id_of(in_hand)] = -1
        return arr

def card_deck_for_two(seed = None):
    all_cards_first = []
    all_cards_second = []
    rcd = Random_card_deck(seed)
    rcd2 = Random_card_deck()
    for i in range(20):
        some_cd = Random_card_deck(seed + i if seed is not None else None)
        all_cards_second.extend([some_cd.new_card() for i in range(len(some_cd.all_cards)//2)])
        all_cards_first.extend(some_cd.all_cards)
    
    rcd.all_cards = all_cards_first
    rcd2.all_cards = all_cards_second
    return rcd, rcd2