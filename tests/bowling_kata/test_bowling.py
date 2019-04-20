from src.bowling_kata import bowling


def test_all_nines():
    game = bowling.Bowling()
    result = game.calculate_result('9-|9-|9-|9-|9-|9-|9-|9-|9-|9-||')
    assert result == 90

def test_mixed_example():
    game = bowling.Bowling()
    result = game.calculate_result('X|7/|9-|X|-8|8/|-6|X|X|X||81')
    assert result == 167

def test_all_strikes():
    game = bowling.Bowling()
    result = game.calculate_result('X|X|X|X|X|X|X|X|X|X||XX')
    assert result == 300

def test_meetup_example():
    game = bowling.Bowling()
    result = game.calculate_result('11|22|33|44|5/|32|X|32|X|X||XX')
    assert result == 118