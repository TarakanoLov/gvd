import sys
sys.path.insert(0, '.')

from base_game import player
from base_game import card_deck
from base_game import cards

def test_default_constructor():
    cd = card_deck.Random_card_deck(0)
    pl = player.Player(cd)
    assert pl.name == ''
    #assert pl.cards == []
    assert pl.tower == 20
    assert pl.wall == 5
    assert pl.mine == 2
    assert pl.monastery == 2
    assert pl.barracks == 2
    assert pl.ore == 5
    assert pl.mana == 5
    assert pl.squad == 5

def test_constructor():
    cd = card_deck.Random_card_deck(0)
    pl = player.Player(cd, 1, 2, 3, 4, 5, 6, 7, 8, 'some')
    assert pl.name == 'some'
    assert len(pl.cards) == 7
    assert pl.tower == 1
    assert pl.wall == 2
    assert pl.mine == 3
    assert pl.monastery == 4
    assert pl.barracks == 5
    assert pl.ore == 6
    assert pl.mana == 7
    assert pl.squad == 8

def test_str():
    cd = card_deck.Random_card_deck(0)
    pl = player.Player(cd)
    assert str(pl) == 'Персонаж: \n карты:[Карта: Рудная жила, Карта: Суккубы, Карта: Мягкий камень, Карта: Сад камней, Карта: Сердце дракона, Карта: Сияющий камень, Карта: Эмпатия], tower:20, wall:5, mine:2, monastery:2, barracks:2\n ore:5, mana:5, squad:5'
    
def test_add_tower():
    cd = card_deck.Random_card_deck(0)
    pl = player.Player(cd)
    assert pl.tower == 20
    pl.add_tower(10)
    assert pl.tower == 30
    pl.add_tower(-3)
    assert pl.tower == 27
    pl.add_tower(100)
    assert pl.tower == 127
    pl.add_tower(-200)
    assert pl.tower == 0
    
def test_make_damage():
    cd = card_deck.Random_card_deck(0)
    pl = player.Player(cd)
    assert pl.tower == 20
    assert pl.wall == 5
    pl.make_damage(1)
    assert pl.tower == 20
    assert pl.wall == 4
    pl.make_damage(4)
    assert pl.tower == 20
    assert pl.wall == 0
    pl.add_wall(10)
    assert pl.tower == 20
    assert pl.wall == 10
    pl.make_damage(15)
    assert pl.tower == 15
    assert pl.wall == 0
    
def test_drop():
    cd = card_deck.Random_card_deck(0)
    pl = player.Player(cd)
    assert len(pl.card_deck.all_cards) == 95
    assert len(pl.cards) == 7
    assert pl.cards[0] == cards.map_name_too_card['РУДНАЯ ЖИЛА']
    assert cards.map_name_too_card['РУДНАЯ ЖИЛА'] in pl.cards
    pl.drop(cards.map_name_too_card['РУДНАЯ ЖИЛА'])
    assert len(pl.card_deck.all_cards) == 94
    assert len(pl.cards) == 7
    assert cards.map_name_too_card['РУДНАЯ ЖИЛА'] not in pl.card_deck.all_cards
    assert cards.map_name_too_card['РУДНАЯ ЖИЛА'] not in pl.cards
    assert pl.cards[0] == cards.map_name_too_card['ЭМЕРАЛЬД']
    
def test_get_new_resource():
    cd = card_deck.Random_card_deck(0)
    pl = player.Player(cd, start_mine=3, start_monastery=4, start_barracks=5)
    assert pl.ore == 5
    assert pl.mana == 5
    assert pl.squad == 5
    assert pl.mine == 3
    assert pl.monastery == 4
    assert pl.barracks == 5
    pl.get_new_resource()
    assert pl.ore == 8
    assert pl.mana == 9
    assert pl.squad == 10
    assert pl.mine == 3
    assert pl.monastery == 4
    assert pl.barracks == 5
    
