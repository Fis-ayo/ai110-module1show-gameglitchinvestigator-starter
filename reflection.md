# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  - Secret hint was flunctuating (Goes high when number might be low)
  - Guessing instructions are not changing according to the difficulty level
  - Number attemps isn't defined for difficulty levels
  - New Game button does not restart the game
  Scores after each game is always negative and low indicating a possible error with its logic
  Secret number does not change when difficultly level changes mid game
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)? Copilot
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
AI suggested the switching of the statements of the if-else statements as a response to an issue I had presented.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
AI had suggested reseting some variables in regards to the New Game bugs. It seemed the suggestions made sense as there were some hardcoded values per the difficulty range. However, it suggested initializing some values which raised a streamlit exception.
I had previously accepted the solution as it seemed to be going in the right direction to fix the bug.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I considered a bug fixed when the app behaved correctly both manually and under pytest. For manual checks, I would reproduce the exact steps that caused the bug — like changing difficulty mid-game or clicking New Game — and confirm the broken behavior was gone. For logic bugs like the score calculation, I relied on pytest to confirm the function returned the expected values across multiple cases.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
I ran the tests in `tests/test_game_logic.py` using pytest. The tests covered `check_guess`, `parse_guess`, and `update_score`. Running them exposed that the score logic was subtracting points even on edge cases where the guess was valid, which helped pinpoint where `update_score` needed to be corrected.
- Did AI help you design or understand any tests? How?
AI did help understand how the pytest works. I encountered an issue with running the test_game_logic.py file because it was not in the same dir as the function it was importing which was logic_utils.py. We created a `conftest.py` in the root dir so pytest could resolve the import path to `logic_utils.py` correctly.
---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
Streamlit re-runs the entire Python script from top to bottom every time the user does anything — types in a box, clicks a button, or even moves a slider. In the original code, `random.randint()` was called unconditionally at the top of the script, so a brand-new secret was generated on every single rerun. This meant the target kept shifting under the player's feet with each interaction.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Imagine your app is a recipe card that gets re-read and re-executed from the first line every time you interact with the page. Normally that would reset everything — your score, your guess history, your secret number — back to zero each time. `st.session_state` is like a sticky note attached to that recipe card: values you write there survive each re-read, so the game can remember what happened in previous runs without resetting.
- What change did you make that finally gave the game a stable secret number?
The fix was guarding the secret initialization with `if "secret" not in st.session_state:`. This means `random.randint()` is only called once — the very first time the app loads — and every subsequent rerun just reads the already-stored value from session state instead of generating a new one.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  Verifying every AI suggestion manually before accepting it became a key habit. Because one of the AI suggestions looked correct but raised a Streamlit exception at runtime, I learned to read the proposed change, trace through what it would actually do, and test it in isolation before moving on. I also want to keep writing pytest tests for logic functions early — it made debugging the score and guess logic much faster than trying to reproduce everything through the UI.
- What is one thing you would do differently next time you work with AI on a coding task?
  Next time I would read and understand the full codebase before describing any bug to the AI. In this project I sometimes described symptoms without understanding the root cause, which led to AI suggestions that fixed the surface issue while leaving the underlying problem intact. Starting with a thorough read-through would let me give the AI more precise context and evaluate its suggestions more critically.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  I used to assume that AI-generated code was either obviously right or obviously wrong, but this project showed me it often lands in a more dangerous middle ground — code that looks plausible, runs without syntax errors, yet contains subtle logic or state management bugs. I now treat AI as a knowledgeable collaborator whose output still needs the same review and testing I would give any human-written code.
