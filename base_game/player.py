from base_game import card_deck

class Player:
    def __init__(self, card_deck, start_tower = 20, start_wall = 5, start_mine = 2, start_monastery = 2, start_barracks = 2, start_ore = 5, start_mana = 5, start_squad = 5, name = ''):
        self.name = name
        self.cards = card_deck.generate_start_cards()
        self.card_deck = card_deck
        self.tower, self.wall = start_tower, start_wall
        self.mine, self.monastery, self.barracks = start_mine, start_monastery, start_barracks
        self.ore, self.mana, self.squad = start_ore, start_mana, start_squad
        
    def __str__(self):
        return 'Персонаж: \n карты:{}, tower:{}, wall:{}, mine:{}, monastery:{}, barracks:{}\n ore:{}, mana:{}, squad:{}'.format(self.cards,
            self.tower, self.wall, self.mine, self.monastery, self.barracks, self.ore, self.mana, self.squad)

    def add_tower(self, integer):
        #assert self.tower >= 1
        self.tower = max(0, self.tower + integer)

    def add_wall(self, integer):
        assert self.wall >= 0
        self.wall = max(0, self.wall + integer)
        
    def add_mine(self, integer):
        assert self.mine >= 0
        self.mine = max(0, self.mine + integer)
        
    def add_monastery(self, integer):
        assert self.monastery >= 0
        self.monastery = max(0, self.monastery + integer)
        
    def add_barracks(self, integer):
        assert self.barracks >= 0
        self.barracks = max(0, self.barracks + integer)

    def add_ore(self, integer):
        assert self.ore >= 0
        self.ore = max(0, self.ore + integer)
        
    def add_mana(self, integer):
        assert self.mana >= 0
        self.mana = max(0, self.mana + integer)
        
    def add_squad(self, integer):
        assert self.squad >= 0
        self.squad = max(0, self.squad + integer)
        
    def make_damage(self, damage):
        assert damage >= 0
        if damage > self.wall:
           self.add_tower(-(damage - self.wall))
           self.wall = 0
        else:
           self.add_wall(-damage)
           
    def drop(self, card):
        assert card in self.cards
        self.cards[self.cards.index(card)] = self.card_deck.new_card()
        
    def get_new_resource(self):
        self.add_ore(self.mine)
        self.add_mana(self.monastery)
        self.add_squad(self.barracks)
        
    def game_ended(self, player2):
        return self.tower >= 50 or self.tower <= 0 or player2.tower >= 50 or player2.tower <= 0
    
    def win(self, player2):
        return self.tower >= 50 or player2.tower <= 0
        
def make_2_players(seed = None):
    cd1, cd2 = card_deck.card_deck_for_two(seed)
    return Player(cd1), Player(cd2)