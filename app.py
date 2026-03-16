import random
import streamlit as st
from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)


def get_proximity_label(guess: int, secret: int, low: int, high: int) -> str:
    """Return an emoji + label based on how close the guess is to the secret."""
    distance = abs(guess - secret)
    span = max(high - low, 1)
    ratio = distance / span
    if ratio <= 0.05:
        return "🔥 Burning Hot"
    if ratio <= 0.15:
        return "♨️ Hot"
    if ratio <= 0.30:
        return "🌡️ Warm"
    if ratio <= 0.50:
        return "🧊 Cold"
    return "❄️ Freezing"


def reset_game() -> None:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.last_difficulty = difficulty

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "last_difficulty" not in st.session_state:
    st.session_state.last_difficulty = difficulty
elif st.session_state.last_difficulty != difficulty:
    reset_game()
    st.info("Difficulty changed. New game started.")

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁", on_click=reset_game)
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# FIX: Corrected the logic to check for new game before processing the guess.
if new_game:
    st.success("New game started.")

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess, low=low, high=high)

    if not ok:
        history_entry = "" if raw_guess is None else str(raw_guess)
        if len(history_entry) > 60:
            history_entry = history_entry[:57] + "..."
        st.session_state.history.append(history_entry)
        st.error(err)
    else:
        st.session_state.attempts += 1
        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)
        proximity = get_proximity_label(guess_int, secret, low, high)

        if show_hint:
            if outcome == "Win":
                st.success(f"🎯 {message}")
            elif "Hot" in proximity or "Warm" in proximity:
                st.warning(f"{message} — {proximity}")
            else:
                st.info(f"{message} — {proximity}")

        score_before = st.session_state.score
        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )
        score_delta = st.session_state.score - score_before

        st.session_state.history.append({
            "Guess": guess_int,
            "Outcome": outcome,
            "Proximity": "🎯 Exact!" if outcome == "Win" else proximity,
            "Score Δ": f"{score_delta:+d}",
        })

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.divider()

valid_entries = [e for e in st.session_state.history if isinstance(e, dict)]
if valid_entries:
    st.subheader("📊 Session Summary")
    st.table(valid_entries)

st.caption("Built by an AI that claims this code is production-ready.")
