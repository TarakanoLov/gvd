import numpy as np

from . import player

class OneGameStats:
    def __init__(self):
        self.card_deck_hod = []
        self.all_game_situation = []
        self.card_to_use = []
        self.gen_all_card_other = []
        self.all_rewards = []
        self.game_before_end = []
        
    def clear(self):
        self.__init__()
        
    def dump(self):
        assert len(self.all_rewards) != 0
        return self.card_deck_hod, self.all_game_situation, self.card_to_use, self.gen_all_card_other, self.all_rewards, self.game_before_end
        
    def collect(self, player1, player2):
        self.card_deck_hod.append(np.concatenate([player1.card_deck.to_array(), player2.card_deck.to_array()], axis=0))
        self.all_game_situation.append(player1.gen_array_input(player2)[0])
        self.card_to_use.append(player1.gen_my_all_card()[0])
        self.gen_all_card_other.append(player2.gen_my_all_card()[0])

    def collect_win(self):
        self.all_rewards.extend([0.95**(len(self.card_deck_hod) - i) for i in range(len(self.card_deck_hod))])
        self.game_before_end.extend([len(self.card_deck_hod) - i for i in range(len(self.card_deck_hod))])

    def collect_loose(self):
        self.all_rewards.extend([-0.95**(len(self.card_deck_hod) - i)  for i in range(len(self.card_deck_hod))])
        self.game_before_end.extend([len(self.card_deck_hod) - i for i in range(len(self.card_deck_hod))])
    
class ManyGameStats:
    def __init__(self):
        self.games = [OneGameStats()]
        
    def clear(self):
        self.games = []
        
    def dump(self):
        stats = ([], [], [], [], [], [])
        for ind, one_game in enumerate(self.games):
            if ind == len(self.games) - 1:
                continue
            one_stat = one_game.dump()
            for i in range(len(one_stat)):
                stats[i].extend(one_stat[i])
        return stats

    def collect(self, player1, player2):
        self.games[-1].collect(player1, player2)
        
    def collect_win(self):
        self.games[-1].collect_win()
        self.games.append(OneGameStats())
        
    def collect_loose(self):
        self.games[-1].collect_loose()
        self.games.append(OneGameStats())

class StatisticCollector:
    def __init__(self):
        self.first = ManyGameStats()
        self.second = ManyGameStats()

    def collect_first(self, player1, player2):
        self.first.collect(player1, player2)

    def collect_second(self, player1, player2):
        self.second.collect(player1, player2)

    def win_first(self):
        self.first.collect_win()
        self.second.collect_loose()

    def win_second(self):
        self.first.collect_loose()
        self.second.collect_win()
    
    def clear(self):
        self.first.clear()
        self.second.clear()
        
    def dump(self):
        stats_first = self.first.dump()
        stats_second = self.second.dump()
        for i in range(len(stats_first)):
            stats_first[i].extend(stats_second[i])
            
        return stats_first

class Game:
    def __init__(self, player1, player2, statistic = None):
        self.player1 = player1
        self.player2 = player2
        self.statistic = statistic
        
    def dump_statistics():
        stats = self.statistic.dump()
        self.statistic.clear()
        return stats
        
    def startPlay(self):
        while not self.player1.win(self.player2) and not self.player2.win(self.player1):
            self.player1.get_new_resource()
            if self.statistic is not None:
                self.statistic.collect_first(self.player1, self.player2)
 
            (if_next_move_too, only_drop_next_move) = self.player1.nextMove(self.player2)
            
            self.player2.get_new_resource()  
            if self.statistic is not None:
                self.statistic.collect_second(self.player2, self.player1)            
        
            (if_next_move_too, only_drop_next_move) = self.player2.nextMove(self.player1)
                
        if self.player1.tower >= 50 or self.player2.tower <= 0:
            if self.statistic is not None:
                self.statistic.win_first()
            return 0
        else:
            if self.statistic is not None:
                self.statistic.win_second()
            return 1
            
# class FastGame:
    # def __init__(self, num_of_games = 1000, one_batch=100):
        # self.num_of_games = num_of_games
        # self.one_batch = 100
        
    # def StartPlay(self):
        
    