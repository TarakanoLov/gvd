import sys
sys.path.insert(0, '.')

from ml import helpers

def test_target_to_model_1():
    sss = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
    new_all_rewards = [0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75]
    game_before_end = [7, 6, 5, 4, 3, 2, 1]
    
    res = helpers.calclulate_target_to_model(sss, new_all_rewards, game_before_end)
    assert res == [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9]
    
def test_target_to_model_2():
    sss = [0.60001, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
    new_all_rewards = [0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75]
    game_before_end = [7, 6, 5, 4, 3, 2, 1]

    res = helpers.calclulate_target_to_model(sss, new_all_rewards, game_before_end)
    assert res == [-0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9]
    
def test_target_to_model_3():
    sss = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, -0.1, -0.2]
    new_all_rewards = [0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, -0.3, -0.4]
    game_before_end = [7, 6, 5, 4, 3, 2, 1, 2, 1]
    
    res = helpers.calclulate_target_to_model(sss, new_all_rewards, game_before_end)
    assert res == [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, -0.9, -0.9]