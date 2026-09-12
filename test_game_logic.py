from game_logic import take_damage


def test_player_takes_damage():
    assert take_damage(100, 20) == 80