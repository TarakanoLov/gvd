import sys
sys.path.insert(0, '.')

import numpy as np

from base_game import game
from base_game import player
from base_game import card_deck

def test_base_statisctic():
    st = game.OneGameStats()
    assert st.card_deck_hod == []
    assert st.all_game_situation == []
    assert st.card_to_use == []
    assert st.gen_all_card_other == []
    assert st.all_rewards == []
    assert st.game_before_end == []
    
    first, second = player.make_2_players(0)
    st.collect(first, second)
    assert len(st.card_deck_hod) == 1
    assert (st.card_deck_hod[0] == np.array([7, 42, 64, 25, 27, 92, 59, 10, 0, 47, -2, 13, 52, 53, 87, 149, 29, 16, 143, 233, 43, 24, 39, 33, 73, 181, -1, 40, 15, 6, 9, 3, 215, 111, 77, 5, 95, 241, 34, 89, -2, 136, 231, 1, 141, 30, 366, 4, 14, 63, 58, 18, 202, 76, 82, 11, 93, 38, 102, 36, 78, 32, 26, 37, -1, 68, 341, 49, -2, 161, 35, -2, 69, 138, 85, 21, 70, 114, 44, 62, 31, 12, 247, 90, 348, 22, 131, 100, 71, 96, 41, -1, 8, 20, 23, 163, 99, 2, 28, 65, 17, 19, 61, 97, 21, 133, 243, 42, -2, 45, 112, 18, 109, 159, 11, 29, 16, 40, 337, 52, 32, 3, 242, 72, 74, 94, -1, 38, 116, 64, 58, 191, 89, 132, 0, 30, 25, 46, 2, 34, 63, 22, 127, 26, 4, 60, 36, 48, -2, 235, 260, 13, 37, 59, 27, 10, 7, 202, 5, 91, 14, 50, -1, 83, 87, 85, 67, 39, 41, 35, 118, 15, 49, 117, 20, 8, 33, 149, 31, 17, 1, 9, 86, 126, -2, -1, 23, 99, 43, 24, 28, 12, 139, 186, 65, 71, 244, 6, 19, 160, 152, -1, 77, 84])).all()
    assert len(st.all_game_situation) == 1
    assert (st.all_game_situation[0] == np.array([20.,  5., 20.,  5.,  2.,  2.,  2.,  5.,  5.,  5.,  2.,  2.,  2.,
         5.,  5.,  5.])).all()
    assert len(st.card_to_use) == 1
    assert (st.card_to_use[0] == np.array([0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0.])).all()
    assert len(st.gen_all_card_other) == 1
    assert (st.gen_all_card_other[0] == np.array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0.,
    0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
    0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
    0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
    1., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
    0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
    0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0.,
    0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0.,
    0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
    0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0.,
    1., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
    0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.])).all()
    assert st.all_rewards == []
    assert st.game_before_end == []
    
    st.collect_win()
    assert st.all_rewards == [0.95]
    assert st.game_before_end == [1]
    
    st.all_rewards = []
    st.game_before_end = []
    st.collect_loose()
    assert st.all_rewards == [-0.95]
    assert st.game_before_end == [1]
    
    stats = st.dump()
    assert len(stats) == 6
    for one in stats:
        assert len(one) == 1
    
    st.clear()
    assert st.card_deck_hod == []
    assert st.all_game_situation == []
    assert st.card_to_use == []
    assert st.gen_all_card_other == []
    assert st.all_rewards == []
    assert st.game_before_end == []

def test_many_game_stats():
    stats = game.ManyGameStats()
    first, second = player.make_2_players(0)
    
    stats.collect(first, second)
    stats.collect(first, second)
    stats.collect_loose()
    
    stats.collect(second, first)
    stats.collect(second, first)
    stats.collect_win()
    
    st = stats.dump()
    assert len(st) == 6
    for one_stat in st:
        assert len(one_stat) == 4
    
    stats.clear()
    assert stats.games == []

def test_statistic_collector():
    sc = game.StatisticCollector()
    first, second = player.make_2_players(0)
    sc.collect_first(first, second)
    sc.collect_first(first, second)
    sc.collect_second(first, second)
    sc.win_first()
    first, second = player.make_2_players(1)
    sc.collect_second(first, second)
    sc.collect_second(first, second)
    sc.collect_first(first, second)
    sc.win_second()
    stats = sc.dump()
    assert len(stats) == 6
    for one_stat in stats:
        assert len(one_stat) == 6

def test_game():
    assert True