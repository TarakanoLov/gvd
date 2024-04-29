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
    assert (st.card_deck_hod[0] == np.array([120, 120,  26,  16, 120, 120,  11, 120,  38, 120,  18,  34, 120,
                33,   1, 120,  36, 120, 120,  12, 120, 120,  15,  43,  22, 120,
               120, 120,   5,  24,  17, 120, 120, 120,   4,  42, 120,   7, 120,
               120, 120,  37, 120,  39,  27, 120, 120,   8,  31, 120, 120, 120,
               120, 120,  14, 120, 120,  20, 120,  28, 120, 120, 120,  40, 120,
               120,  32, 120, 120, 120,  25, 120, 120, 120, 120, 120,   3, 120,
               120, 120, 120,  19,   9,  23, 120,  13,   0, 120,  41,  30,  35,
               120, 120,  29,  10,   6,  21, 120, 120, 120, 120,   2, 120,   5,
               120, 120, 120,  40, 120,   6, 120,  18, 120, 120,  26, 120, 120,
               120, 120,  29,  21, 120, 120, 120, 120, 120, 120,   1,  10,  31,
               120, 120, 120, 120,  24,  39, 120, 120,  28, 120,  35,  20,  11,
               120,  17, 120, 120,  33,   3, 120, 120,  43, 120,  36, 120,  41,
               120,  12,   8, 120, 120, 120,  16,  34,  37, 120,  30,  38, 120,
               120,  23, 120, 120,  15, 120,   0,  32, 120, 120,  22, 120,  25,
                14, 120, 120, 120,  19, 120, 120,  27, 120, 120, 120,  13,   9,
               120, 120, 120, 120,  42,   4,   2,   7, 120])).all()
    assert len(st.all_game_situation) == 1
    assert (st.all_game_situation[0] == np.array([20.,  5., 20.,  5.,  2.,  2.,  2.,  5.,  5.,  5.,  2.,  2.,  2.,
         5.,  5.,  5.])).all()
    assert len(st.card_to_use) == 1
    assert (st.card_to_use[0] == np.array([0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0.,
        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
        0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
        0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0.,
        0., 0., 0., 1., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
        0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 1.,
        0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.])).all()
    assert len(st.gen_all_card_other) == 1
    assert (st.gen_all_card_other[0] == np.array([1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
        0., 1., 0., 0., 0., 0., 0., 1., 0., 0., 1., 0., 0., 0., 0., 0., 0.,
        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
        1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0.,
        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.,
        0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
        0., 1., 0., 0., 0., 0., 0., 1., 0., 0., 1., 0., 0., 0., 0., 0., 0.,
        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.])).all()
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