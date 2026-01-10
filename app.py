import streamlit as st
import requests

# 1. Page Config
st.set_page_config(page_title="H-J-B-R-L", layout="centered")

# 2. Game Memory (Session State)
if 'p1_score' not in st.session_state:
    st.session_state.p1_score = 0
    st.session_state.p2_score = 0
    st.session_state.turn = 1

# 3. Load Word List
@st.cache_data
def load_words():
    url = "https://raw.githubusercontent.com/tahmid02016/bangla-wordlist/master/words.txt"
    return set(requests.get(url).text.split())

words_db = load_words()

# 4. Symmetric Scoreboard
st.title("𝐇-𝐉-𝐁-𝐑-𝐋 𝐁𝐃")
c1, c2 = st.columns(2)
c1.metric("Player 1", st.session_state.p1_score)
c2.metric("Player 2", st.session_state.p2_score)
st.divider()

# 5. Game Engine
POINTS = {'ক্ষ': 10, 'জ্ঞ': 10, 'ঞ্চ': 10, 'স্ত': 8, 'খ': 5, 'ঘ': 5}
current_player = st.session_state.turn
word_input = st.text_input(f"Player {current_player}, enter your word:", key="input")

if st.button("Confirm Move"):
    if word_input in words_db:
        # Calculate points
        score = sum(POINTS.get(char, 1) for char in word_input)
        
        # Update specific player
        if current_player == 1:
            st.session_state.p1_score += score
            st.session_state.turn = 2
        else:
            st.session_state.p2_score += score
            st.session_state.turn = 1
            
        st.success(f"Added {score} points!")
        st.rerun()
    else:
        st.error("Invalid word. Try again!")
