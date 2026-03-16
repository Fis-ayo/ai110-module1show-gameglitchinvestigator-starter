from logic_utils import check_guess, parse_guess, update_score


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


def test_parse_guess_accepts_integer_input():
    ok, guess, err = parse_guess("42")
    assert ok is True
    assert guess == 42
    assert err is None


def test_parse_guess_rejects_empty_input():
    ok, guess, err = parse_guess("   ")
    assert ok is False
    assert guess is None
    assert err == "Enter a guess."


def test_parse_guess_rejects_decimal_input():
    ok, guess, err = parse_guess("12.9")
    assert ok is False
    assert guess is None
    assert err == "That is not a valid whole number."


def test_parse_guess_rejects_out_of_range_integer():
    ok, guess, err = parse_guess("999", low=1, high=100)
    assert ok is False
    assert guess is None
    assert err == "Enter a number between 1 and 100."


def test_parse_guess_rejects_overly_long_input():
    ok, guess, err = parse_guess("9" * 25, max_length=20)
    assert ok is False
    assert guess is None
    assert err == "Input is too long (max 20 chars)."


def test_parse_guess_rejects_unicode_numeric_forms():
    ok, guess, err = parse_guess("٤٢")
    assert ok is False
    assert guess is None
    assert err == "That is not a valid whole number."


def test_parse_guess_rejects_comma_formatted_number():
    ok, guess, err = parse_guess("1,000")
    assert ok is False
    assert guess is None
    assert err == "That is not a valid whole number."
