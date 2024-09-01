import sys
sys.path.insert(0, '.')

from base_game import cards
from base_game import player
from base_game import card_deck

def test_eq_cards():
    assert cards.map_name_too_card['САПФИР'] == cards.map_name_too_card['САПФИР']
    
    assert cards.map_name_too_card['САПФИР'] != cards.map_name_too_card['РУБИН']
    
def test_str_card():
    assert str(cards.map_name_too_card['САПФИР']) == 'Карта: Сапфир'
    
def test_is_can_use_ore():
    cd = card_deck.Random_card_deck(0)
    pl = player.Player(cd)
    
    card = cards.map_name_too_card['ТОЛЧКИ']
    assert card.cost == 7
    assert card.type_card == 0
    assert pl.ore == 5
    assert not card.is_can_use(pl)
    pl.ore = 6
    assert not card.is_can_use(pl)
    pl.ore = 7
    assert card.is_can_use(pl)
    pl.ore = 8
    assert card.is_can_use(pl)
    pl.ore = 100
    assert not cards.map_name_too_card['ПАРИТЕТ'].is_can_use(pl)
    assert not cards.map_name_too_card['ТРОЛЛЬ-НАСТАВНИК'].is_can_use(pl)
    
def test_is_can_use_mana():
    cd = card_deck.Random_card_deck(0)
    pl = player.Player(cd)
    
    card = cards.map_name_too_card['ПАРИТЕТ']
    assert card.cost == 7
    assert card.type_card == 1
    assert pl.mana == 5
    assert not card.is_can_use(pl)
    pl.mana = 6
    assert not card.is_can_use(pl)
    pl.mana = 7
    assert card.is_can_use(pl)
    pl.mana = 8
    assert card.is_can_use(pl)
    pl.mana = 100
    assert not cards.map_name_too_card['ТОЛЧКИ'].is_can_use(pl)
    assert not cards.map_name_too_card['ТРОЛЛЬ-НАСТАВНИК'].is_can_use(pl)
    
def test_is_can_use_squad():
    cd = card_deck.Random_card_deck(0)
    pl = player.Player(cd)
    
    card = cards.map_name_too_card['ТРОЛЛЬ-НАСТАВНИК']
    assert card.cost == 7
    assert card.type_card == 2
    assert pl.squad == 5
    assert not card.is_can_use(pl)
    pl.squad = 6
    assert not card.is_can_use(pl)
    pl.squad = 7
    assert card.is_can_use(pl)
    pl.squad = 8
    assert card.is_can_use(pl)
    pl.squad = 100
    assert not cards.map_name_too_card['ТОЛЧКИ'].is_can_use(pl)
    assert not cards.map_name_too_card['ПАРИТЕТ'].is_can_use(pl)
    
def test_use_ore():
    first, second = player.make_2_players(0)
    card = cards.map_name_too_card['ВЕЛИКАЯ СТЕНА']
    first.cards.append(card)
    first.ore = 8
    assert first.ore == 8
    assert first.mana == 5
    assert first.squad == 5
    assert second.ore == 5
    assert second.mana == 5
    assert second.squad == 5
    card.use(first, second)
    assert first.ore == 0
    assert first.mana == 5
    assert first.squad == 5
    assert second.ore == 5
    assert second.mana == 5
    assert second.squad == 5
    
def test_use_mana():
    first, second = player.make_2_players(4)
    card = cards.map_name_too_card['КОПЬЕ']
    first.cards.append(card)
    first.mana = 4
    assert first.ore == 5
    assert first.mana == 4
    assert first.squad == 5
    assert second.ore == 5
    assert second.mana == 5
    assert second.squad == 5
    card.use(first, second)
    assert first.ore == 5
    assert first.mana == 0
    assert first.squad == 5
    assert second.ore == 5
    assert second.mana == 5
    assert second.squad == 5
    
def test_use_squad():
    first, second = player.make_2_players(9)
    card = cards.map_name_too_card['КАРЛИК']
    first.cards.append(card)
    first.squad = 2
    assert first.ore == 5
    assert first.mana == 5
    assert first.squad == 2
    assert second.ore == 5
    assert second.mana == 5
    assert second.squad == 5
    card.use(first, second)
    assert first.ore == 5
    assert first.mana == 6
    assert first.squad == 0
    assert second.ore == 5
    assert second.mana == 5
    assert second.squad == 5
    
def test_cards_type():
    for ind, card in enumerate(cards.all_cards):
        assert card.type_card == ind // 34
        assert card.cost >= 0
        assert card.index >= 0
        
def test_test_card():
    card = cards.map_name_too_card['КАРЛИК']
    assert (cards.test_card(card) == [0, 3, 0, 0, 0, 0, 0, 0, 0, 0]).all()
    
    card = cards.map_name_too_card['РАДУГА']
    assert (cards.test_card(card) == [-1,  0,  0,  0,  0,  1,  0,  0,  0,  0]).all()
        