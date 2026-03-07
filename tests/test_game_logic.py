from logic_utils import check_guess, update_score


def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert message == "🎉 Correct!"


def test_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"


def test_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"


def test_update_score_win_first_attempt():
    score = update_score(current_score=0, outcome="Win", attempt_number=1)
    assert score == 100


def test_update_score_win_has_minimum_points():
    score = update_score(current_score=0, outcome="Win", attempt_number=15)
    assert score == 10


def test_update_score_too_high_penalty_is_consistent():
    score_attempt_1 = update_score(current_score=0, outcome="Too High", attempt_number=1)
    score_attempt_2 = update_score(current_score=0, outcome="Too High", attempt_number=2)
    assert score_attempt_1 == -5
    assert score_attempt_2 == -5


def test_update_score_too_low_penalty_is_minus_five():
    score = update_score(current_score=0, outcome="Too Low", attempt_number=3)
    assert score == -5
