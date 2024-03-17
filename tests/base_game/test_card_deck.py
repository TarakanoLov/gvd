import sys
sys.path.insert(0, '.')

from base_game import card_deck
from base_game import cards

import numpy as np

def test_fake_card_deck():
    cd = card_deck.Fake_card_deck(cards.all_cards)
    assert len(cd.cards) == 102
    start_cards = cd.generate_start_cards()
    assert len(cd.cards) == 95
    assert start_cards == [cards.map_name_too_card['ДРАКОН'], cards.map_name_too_card['ВСАДНИК НА ПЕГАСЕ'], cards.map_name_too_card['ВАМПИР'], cards.map_name_too_card['КАМЕННЫЙ ГИГАНТ'], cards.map_name_too_card['СУККУБЫ'], cards.map_name_too_card['ВОИТЕЛЬ'], cards.map_name_too_card['ВОР']]
    
def test_random_card_deck():
    cd = card_deck.Random_card_deck(0)
    assert len(cd.all_cards) == 102
    start_cards = cd.generate_start_cards()
    assert len(start_cards) == 7
    assert len(cd.all_cards) == 95
    card = cd.new_card()
    assert len(cd.all_cards) == 94
    assert card not in cd.all_cards
    
def test_rcd_new_card():
    cd = card_deck.Random_card_deck(0)
    picked_cards = []
    for i in range(101):
        picked_cards.append(cd.new_card())
        
    assert len(cd.all_cards) == 1
    last_card = cd.new_card()
    assert last_card not in picked_cards
    picked_cards.append(last_card)
    assert len(cd.all_cards) == 0
    
    from_new = cd.new_card()
    assert from_new in picked_cards
    assert len(cd.all_cards) == 101
    
def test_to_array():
    cd = card_deck.Random_card_deck(0)
    assert len(cd.all_cards) == 102
    assert np.all(cd.to_array() == np.array([48, 38, 84, 74, 56, 3, 69, 37, 96, 25, 76, 92, 17, 91, 59, 52, 94, 14, 22, 70, 54, 51, 73, 101, 80, 42, 33, 12, 63, 82, 75, 50, 19, 4, 62, 100, 15, 65, 8, 23, 32, 95, 26, 97, 85, 10, 40, 66, 89, 0, 45, 7, 44, 2, 72, 31, 35, 78, 55, 86, 27, 9, 6, 98, 13, 5, 90, 53, 20, 47, 83, 28, 57, 43, 11, 46, 61, 21, 49, 18, 29, 77, 67, 81, 24, 71, 58, 16, 99, 88, 93, 30, 34, 87, 68, 64, 79, 1, 39, 41, 36, 60])) 
    assert 120 not in cd.to_array()
    assert len(cd.all_cards) == 102
    
    assert len(cd.all_cards) == 102
    card = cd.new_card()
    assert card.index == 49
    assert np.all(cd.to_array() == np.array([47, 37, 83, 73, 55, 2, 68, 36, 95, 24, 75, 91, 16, 90, 58, 51, 93, 13, 21, 69, 53, 50, 72, 100, 79, 41, 32, 11, 62, 81, 74, 49, 18, 3, 61, 99, 14, 64, 7, 22, 31, 94, 25, 96, 84, 9, 39, 65, 88, 120, 44, 6, 43, 1, 71, 30, 34, 77, 54, 85, 26, 8, 5, 97, 12, 4, 89, 52, 19, 46, 82, 27, 56, 42, 10, 45, 60, 20, 48, 17, 28, 76, 66, 80, 23, 70, 57, 15, 98, 87, 92, 29, 33, 86, 67, 63, 78, 0, 38, 40, 35, 59]))
    assert len(cd.all_cards) == 101
    assert cd.to_array()[49] == 120
    
def test_card_deck_for_two():
    cards1, cards2 = card_deck.card_deck_for_two()
    assert len(cards1.all_cards) == 51
    assert len(cards2.all_cards) == 51
    for card in cards1.all_cards:
       assert card not in cards2.all_cards
    for card in cards2.all_cards:
       assert card not in cards1.all_cards
    