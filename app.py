import streamlit as st
import requests
import re
import unicodedata
import random

# --- 1. THE SETUP (The "Rules" of the Game) ---
# This is where we give letters their "Price"
GRAPHEME_VALUES = {
    'ক': 1, 'ত': 1, 'ন': 1, 'প': 1, 'র': 1, 'ল': 1, 'স': 1, 'া': 1, 'ি': 1,
    'গ': 2, 'চ': 2, 'জ': 2, 'দ': 2, 'ব': 2, 'ম': 2, 'ু': 2,
    'খ': 3, 'ছ': 3, 'ট': 3, 'থ': 3, 'ফ': 3, 'ঙ': 8, 'ঞ': 10
}

# This is our "Cloth Bag" with 100 tiles
if 'bag' not in st.session_state:
    # We mix 100 letters together
    raw_bag = (['ক', 'ন', 'প', 'র', 'ল', 'স', 'ত'] * 6 + 
               ['া', 'ি'] * 10 + 
               ['গ', 'চ', 'জ', 'দ', 'ব', 'ম'] * 4 + 
               ['ঙ', 'ঞ'] * 2)
    random.shuffle(raw_bag)
    st.session_state.bag = raw_bag
    # Give each player their starting 7 tiles
    st.session_state.p1_rack = [st.session_state.bag.pop() for _ in range(7)]
    st.session_state.p2_rack = [st.session_state.bag.pop() for _ in range(7)]

if 'board' not in st.session_state:
    st.session_state.board = [["" for _ in range(9)] for _ in range(9)]
if 'p1_score' not in st.session_state:
    st.session_state.p1_score = 0
if 'p2_score' not in st.session_state:
    st.session_state.p2_score = 0
if 'turn' not in st.session_state:
    st.session_state.turn = "Player 1"

# --- 2. DICTIONARY LOADING ---
@st.cache_data
def load_lexicon():
    url = "https://raw.githubusercontent.com/MinhasKamal/BengaliDictionary/master/BengaliDictionary_17.txt"
    try:
        r = requests.get(url)
        words = re.findall(r'[\u0980-\u09ff]+', r.text)
        return {unicodedata.normalize('NFC', w) for w in words}
    except: return set()

lexicon = load_lexicon()

# --- 3. SIDEBAR (The Scores and Your Hand) ---
st.sidebar.title("🏆 H.J.B.R.L Arena")
st.sidebar.metric("Player 1 Score", f"{st.session_state.p1_score}")
st.sidebar.metric("Player 2 Score", f"{st.session_state.p2_score}")
st.sidebar.info(f"Current Turn: {st.session_state.turn}")

st.sidebar.markdown("---")
st.sidebar.subheader("Your 7 Tiles:")
# Show the current player what letters they have
current_rack = st.session_state.p1_rack if st.session_state.turn == "Player 1" else st.session_state.p2_rack
st.sidebar.warning(" | ".join(current_rack))

# --- 4. THE BOARD DISPLAY ---
st.title("🏛️ Bengali Scrabble Arena")
for r in range(9):
    cols = st.columns(9)
    for c in range(9):
        tile = st.session_state.board[r][c]
        color = "#FFD700" if (r, c) == (4, 4) else "#262730"
        cols[c].markdown(f"<div style='height
