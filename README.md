# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

### Describe the game's purpose.
The game is a guessing game where users have options between a range of numbers based on the game's difficult. Also, there is a limit to how many geuesses have for a game.
### Detail which bugs you found.
- Hints pointed in the wrong direction for some guesses (high/low feedback mismatch).
- Guess range did not update correctly with selected difficulty.
- New Game button did not properly reset/start a fresh game state.
- Changing difficulty during a game did not regenerate the secret number.
- Score logic was inconsistent/incorrect in some outcomes.
- Guess input handling was fragile for empty or non-numeric values.
### Explain what fixes you applied.
- Difficulty-switch bug fixed in `app.py`: changing difficulty now resets the game state and generates a new secret number for the new range.
- Score logic fixed in `logic_utils.py`: win points now use 100 - 10 * (attempt_number - 1) with a floor of 10, and non-win penalties are consistently -5.
- Guess parsing improved in `logic_utils.py`: parse_guess now cleanly handles empty input and non-integer input with clear error messages.
- Tests added/expanded in `test_game_logic.py`: coverage now checks update_score behavior and parse_guess input handling so these regressions are caught automatically.


## 📸 Demo

- [X] <img width="1080" height="421" alt="Image" src="https://github.com/user-attachments/assets/e617e57c-a4e2-463e-974b-5a2760faca88" />
<img width="1258" height="648" alt="Image" src="https://github.com/user-attachments/assets/90e10b86-98bb-4f02-a386-d0f0512dce3b" />



## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
