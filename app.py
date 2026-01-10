import streamlit as st
import requests

# 1. Setup & Session State (The "Game Memory")
st.set_page_config(page_title="H-J-B-R-L", page_icon="🎮")

if 'p1_score' not in st.session_state:
    st.session_state.p1_score = 0
    st.session_state.p2_score = 0
    st.session_state.turn = "Player 1"

# 2. Loading the Dictionary
@st.cache_data
def load_dictionary():
    url = "https://raw.githubusercontent.com/tahmid02016/bangla-wordlist/master/words.txt"
    r = requests.get(url)
    return set(r.text.split())

words_db = load_dictionary()

# 3. Sidebar Scoreboard
st.sidebar.title("🏆 Borno-Baji Score")
st.sidebar.write(f"**Player 1:** {st.session_state.p1_score}")
st.sidebar.write(f"**Player 2:** {st.session_state.p2_score}")
st.sidebar.divider()
st.sidebar.subheader(f"👉 Current Turn: {st.session_state.turn}")

if st.sidebar.button("Reset Game"):
    st.session_state.p1_score = 0
    st.session_state.p2_score = 0
    st.session_state.turn = "Player 1"
    st.rerun()

# 4. Main Game Logic
st.title("𝐇-𝐉-𝐁-𝐑-𝐋 𝐁𝐃")
word_input = st.text_input(f"{st.session_state.turn}, enter your word:", placeholder="যেমন: ক্ষণ")

POINTS = {'ক্ষ': 10, 'জ্ঞ': 10, 'ঞ্চ': 10, 'স্ত': 8, 'খ': 5, 'ঘ': 5}

if word_input:
    if word_input in words_db:
        current_score = sum(POINTS.get(char, 1) for char in word_input)
        st.success(f"✅ Valid! Score: {current_score}")
        
        if st.button(f"Submit for {st.session_state.turn}"):
            if st.session_state.turn == "Player 1":
                st.session_state.p1_score += current_score
                st.session_state.turn = "Player 2"
            else:
                st.session_state.p2_score += current_score
                st.session_state.turn = "Player 1"
            st.rerun()
    else:
        st.error("❌ Not in dictionary.")
