import streamlit as st
import random
import time
import pandas as pd
import json
import os
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Number Guessing Game",
    page_icon="🎮",
    layout="centered"
)

# Initialize session state variables if they don't exist
if 'random_number' not in st.session_state:
    st.session_state.random_number = random.randint(1, 100)
    
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
    
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
    
if 'message' not in st.session_state:
    st.session_state.message = ""
    
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
    
if 'elapsed_time' not in st.session_state:
    st.session_state.elapsed_time = 0
    
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = "Medium"
    
if 'min_range' not in st.session_state:
    st.session_state.min_range = 1
    
if 'max_range' not in st.session_state:
    st.session_state.max_range = 100
    
if 'hints_used' not in st.session_state:
    st.session_state.hints_used = 0
    
if 'theme' not in st.session_state:
    st.session_state.theme = "Light"
    
if 'leaderboard' not in st.session_state:
    st.session_state.leaderboard = []
    
if 'total_games' not in st.session_state:
    st.session_state.total_games = 0
    
if 'total_attempts' not in st.session_state:
    st.session_state.total_attempts = 0
    
if 'best_score' not in st.session_state:
    st.session_state.best_score = {"attempts": float('inf'), "time": float('inf')}
    
if 'history' not in st.session_state:
    st.session_state.history = []

# Function to set difficulty
def set_difficulty(difficulty):
    st.session_state.difficulty = difficulty
    if difficulty == "Easy":
        st.session_state.min_range = 1
        st.session_state.max_range = 50
    elif difficulty == "Medium":
        st.session_state.min_range = 1
        st.session_state.max_range = 100
    elif difficulty == "Hard":
        st.session_state.min_range = 1
        st.session_state.max_range = 200
    elif difficulty == "Expert":
        st.session_state.min_range = 1
        st.session_state.max_range = 500
    reset_game()

# Function to reset the game
def reset_game():
    st.session_state.random_number = random.randint(st.session_state.min_range, st.session_state.max_range)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.message = ""
    st.session_state.start_time = time.time()
    st.session_state.elapsed_time = 0
    st.session_state.hints_used = 0
    st.session_state.history = []
    print(f"New game started with number: {st.session_state.random_number}")

# Function to update leaderboard
def update_leaderboard(name, attempts, time_taken, difficulty):
    new_entry = {
        "name": name,
        "attempts": attempts,
        "time": round(time_taken, 2),
        "difficulty": difficulty,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    st.session_state.leaderboard.append(new_entry)
    st.session_state.leaderboard.sort(key=lambda x: (x["difficulty"], x["attempts"], x["time"]))
    
    # Update best score
    if attempts < st.session_state.best_score["attempts"] or \
       (attempts == st.session_state.best_score["attempts"] and time_taken < st.session_state.best_score["time"]):
        st.session_state.best_score = {"attempts": attempts, "time": time_taken}

# Function to get a hint
def get_hint():
    if st.session_state.hints_used < 3 and not st.session_state.game_over:
        st.session_state.hints_used += 1
        current_range = st.session_state.max_range - st.session_state.min_range
        hint_range = current_range // 4
        
        if st.session_state.random_number <= st.session_state.min_range + hint_range:
            return f"The number is in the lower quarter of the range ({st.session_state.min_range}-{st.session_state.min_range + hint_range})"
        elif st.session_state.random_number <= st.session_state.min_range + 2*hint_range:
            return f"The number is in the lower-middle quarter of the range ({st.session_state.min_range + hint_range + 1}-{st.session_state.min_range + 2*hint_range})"
        elif st.session_state.random_number <= st.session_state.min_range + 3*hint_range:
            return f"The number is in the upper-middle quarter of the range ({st.session_state.min_range + 2*hint_range + 1}-{st.session_state.min_range + 3*hint_range})"
        else:
            return f"The number is in the upper quarter of the range ({st.session_state.min_range + 3*hint_range + 1}-{st.session_state.max_range})"
    else:
        return "No more hints available!"

# Apply theme
if st.session_state.theme == "Dark":
    st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: #FFFFFF;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and instructions
st.title("🎮 Number Guessing Game")
st.markdown(f"""
Try to guess the number between {st.session_state.min_range} and {st.session_state.max_range}!
I'll tell you if your guess is too high or too low.
""")

# Game settings
with st.expander("Game Settings"):
    col1, col2 = st.columns(2)
    
    with col1:
        difficulty = st.selectbox(
            "Select Difficulty:",
            ["Easy", "Medium", "Hard", "Expert"],
            index=["Easy", "Medium", "Hard", "Expert"].index(st.session_state.difficulty)
        )
        if difficulty != st.session_state.difficulty:
            set_difficulty(difficulty)
    
    with col2:
        theme = st.selectbox(
            "Select Theme:",
            ["Light", "Dark"],
            index=["Light", "Dark"].index(st.session_state.theme)
        )
        if theme != st.session_state.theme:
            st.session_state.theme = theme
            # Replace experimental_rerun with rerun
            st.rerun()

# Game interface
col1, col2 = st.columns([3, 1])

with col1:
    # Input for user's guess
    guess = st.number_input(
        "Enter your guess:", 
        min_value=st.session_state.min_range, 
        max_value=st.session_state.max_range, 
        step=1, 
        key="guess"
    )

with col2:
    # Button to submit guess
    if st.button("Guess!", disabled=st.session_state.game_over):
        st.session_state.attempts += 1
        
        # Add to history
        st.session_state.history.append(guess)
        
        if guess < st.session_state.random_number:
            st.session_state.message = "Too low! Try a higher number."
        elif guess > st.session_state.random_number:
            st.session_state.message = "Too high! Try a lower number."
        else:
            st.session_state.elapsed_time = time.time() - st.session_state.start_time
            st.session_state.message = f"🎉 Congratulations! You guessed the number in {st.session_state.attempts} attempts and {st.session_state.elapsed_time:.2f} seconds!"
            st.session_state.game_over = True
            st.session_state.total_games += 1
            st.session_state.total_attempts += st.session_state.attempts

# Display message
if st.session_state.message:
    if st.session_state.game_over:
        st.success(st.session_state.message)
    else:
        st.info(st.session_state.message)

# Display attempts and timer
if st.session_state.attempts > 0:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Attempts", st.session_state.attempts)
    
    with col2:
        current_time = time.time() - st.session_state.start_time if not st.session_state.game_over else st.session_state.elapsed_time
        st.metric("Time", f"{current_time:.2f}s")
    
    with col3:
        st.metric("Hints Used", f"{st.session_state.hints_used}/3")

# Visual hint - thermometer showing how close the guess is
if len(st.session_state.history) > 0 and not st.session_state.game_over:
    last_guess = st.session_state.history[-1]
    total_range = st.session_state.max_range - st.session_state.min_range
    
    if last_guess < st.session_state.random_number:
        distance = st.session_state.random_number - last_guess
        closeness = 1 - (distance / total_range)
        color = "orange"
    else:
        distance = last_guess - st.session_state.random_number
        closeness = 1 - (distance / total_range)
        color = "blue"
    
    st.write("How close is your guess?")
    st.progress(max(0.05, min(0.95, closeness)))
    
    # Add emoji indicators
    if closeness > 0.9:
        st.write("🔥 You're burning hot!")
    elif closeness > 0.7:
        st.write("😎 Getting very warm!")
    elif closeness > 0.5:
        st.write("😊 Getting warmer")
    elif closeness > 0.3:
        st.write("😐 Still cold")
    else:
        st.write("🥶 Ice cold")

# Hint button
if not st.session_state.game_over and st.session_state.attempts > 0:
    if st.button(f"Get Hint ({3 - st.session_state.hints_used} left)"):
        hint = get_hint()
        st.info(hint)

# Guess history
if len(st.session_state.history) > 0:
    with st.expander("Guess History"):
        history_df = pd.DataFrame({
            "Attempt": range(1, len(st.session_state.history) + 1),
            "Guess": st.session_state.history
        })
        st.dataframe(history_df)

# Save score when game is over
if st.session_state.game_over:
    with st.form("save_score"):
        st.write("Save your score to the leaderboard!")
        player_name = st.text_input("Your Name:", max_chars=20)
        submit = st.form_submit_button("Save Score")
        
        if submit and player_name:
            update_leaderboard(
                player_name, 
                st.session_state.attempts, 
                st.session_state.elapsed_time,
                st.session_state.difficulty
            )
            st.success("Score saved!")

# Reset button
if st.session_state.game_over or st.session_state.attempts > 0:
    if st.button("Play Again"):
        reset_game()

# Leaderboard
with st.expander("Leaderboard"):
    if len(st.session_state.leaderboard) > 0:
        leaderboard_df = pd.DataFrame(st.session_state.leaderboard)
        st.dataframe(leaderboard_df)
    else:
        st.write("No scores yet. Be the first to get on the leaderboard!")

# Statistics
with st.expander("Your Statistics"):
    if st.session_state.total_games > 0:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Games Played", st.session_state.total_games)
        
        with col2:
            avg_attempts = st.session_state.total_attempts / st.session_state.total_games
            st.metric("Avg. Attempts", f"{avg_attempts:.1f}")
        
        with col3:
            if st.session_state.best_score["attempts"] < float('inf'):
                st.metric("Best Score", f"{st.session_state.best_score['attempts']} attempts in {st.session_state.best_score['time']:.2f}s")
            else:
                st.metric("Best Score", "N/A")
    else:
        st.write("Play your first game to see statistics!")

# Add a fun fact about binary search
with st.expander("Want a tip to guess efficiently?"):
    st.write("""
    Using a binary search strategy, you can always find the number in log₂(n) or fewer guesses!
    
    For example, in the Medium difficulty (1-100), you can always find the number in 7 or fewer guesses.
    
    Start with the middle number. If it's too high, try the middle of the lower half. If it's too low, try the middle of the upper half.
    Each time, pick the middle of your new range.
    """)

# Export/Import game data
with st.expander("Export/Import Game Data"):
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Export Game Data"):
            game_data = {
                "leaderboard": st.session_state.leaderboard,
                "total_games": st.session_state.total_games,
                "total_attempts": st.session_state.total_attempts,
                "best_score": st.session_state.best_score
            }
            st.download_button(
                "Download JSON",
                data=json.dumps(game_data, indent=4),
                file_name="number_game_data.json",
                mime="application/json"
            )
    
    with col2:
        uploaded_file = st.file_uploader("Import Game Data", type=["json"])
        if uploaded_file is not None:
            try:
                game_data = json.load(uploaded_file)
                st.session_state.leaderboard = game_data.get("leaderboard", [])
                st.session_state.total_games = game_data.get("total_games", 0)
                st.session_state.total_attempts = game_data.get("total_attempts", 0)
                st.session_state.best_score = game_data.get("best_score", {"attempts": float('inf'), "time": float('inf')})
                st.success("Game data imported successfully!")
            except Exception as e:
                st.error(f"Error importing data: {e}")

# Easter egg - secret code
with st.expander("Secret Code 🤫"):
    secret_code = st.text_input("Enter the secret code:", type="password")
    if secret_code == "42istheanswer":
        st.balloons()
        st.success("You found the secret! Here's a hint: The current number is divisible by " + str(st.session_state.random_number % 10 or 10))

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit | v1.2.0")

print(f"Current game state: Number={st.session_state.random_number}, Attempts={st.session_state.attempts}, Difficulty={st.session_state.difficulty}")