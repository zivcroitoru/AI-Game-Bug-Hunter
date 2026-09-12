from game_logic import take_damage


def test_player_takes_damage():
    assert take_damage(100, 20) == 80


def test_health_never_goes_below_zero():
    assert take_damage(10, 20) == 0
