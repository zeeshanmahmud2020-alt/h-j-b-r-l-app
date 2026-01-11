import streamlit as st
import requests
import re
import unicodedata

# --- THE ARCHITECTURE: SHARED MEMORY ---
if 'board' not in st.session_state:
    st.session_state.board = [["" for _ in range(9)] for _ in range(9)]
if 'p1_score' not in st.session_state:
    st.session_state.p1_score = 0
if 'p2_score' not in st.session_state:
    st.session_state.p2_score = 0
if 'turn' not in st.session_state:
    st.session_state.turn = "Player 1"

# --- THE ENGINE: LEXICON INGESTION ---
@st.cache_data
def load_lexicon():
    url = "https://raw.githubusercontent.com/MinhasKamal/BengaliDictionary/master/BengaliDictionary_17.txt"
    lexicon = set()
    try:
        r = requests.get(url)
        # Extract Bengali script only
        words = re.findall(r'[\u0980-\u09ff]+', r.text)
        for w in words:
            lexicon.add(unicodedata.normalize('NFC', w))
        return lexicon
    except: return set()

lexicon = load_lexicon()

# --- THE VISUALS: SIDEBAR SCOREBOARD ---
st.sidebar.title("🏆 H.J.B.R.L Arena")
st.sidebar.metric("Player 1", f"{st.session_state.p1_score}")
st.sidebar.metric("Player 2", f"{st.session_state.p2_score}")
st.sidebar.info(f"Current Turn: {st.session_state.turn}")

# --- THE VISUALS: 9x9 GRID ---
st.title("🏛️ Bengali Scrabble")
for r in range(9):
    cols = st.columns(9)
    for c in range(9):
        tile = st.session_state.board[r][c]
        color = "#FFD700" if (r, c) == (4, 4) else "#262730"
        cols[c].markdown(f"<div style='height:40px; border:1px solid #555; background:{color}; text-align:center; line-height:40px;'>{tile}</div>", unsafe_allow_html=True)

# --- THE CONTROLS: PLACEMENT & TURN SWAP ---
word_to_place = st.text_input("Enter Word:")
c1, c2, c3 = st.columns(3)
row_idx = c1.number_input("Row", 0, 8)
col_idx = c2.number_input("Col", 0, 8)
orient = c3.selectbox("Direction", ["Horizontal", "Vertical"])

if st.button("Confirm Move & End Turn"):
    if word_to_place:
        # 1. Clean and Split into Aksharas
        tiles = re.findall(r'[\u0980-\u09ff][\u09be-\u09cc\u09cd\u0981\u0982\u0983]*', word_to_place)
        
        # 2. Place on Board
        for i, t in enumerate(tiles):
            r = row_idx + (i if orient == "Vertical" else 0)
            c = col_idx + (i if orient == "Horizontal" else 0)
            if r < 9 and c < 9: st.session_state.board[r][c] = t
        
        # 3. Simple Score Update (1 pt per tile for now)
        if st.session_state.turn == "Player 1":
            st.session_state.p1_score += len(tiles)
            st.session_state.turn = "Player 2"
        else:
            st.session_state.p2_score += len(tiles)
            st.session_state.turn = "Player 1"
        st.rerun()

if st.button("Reset Game"):
    st.session_state.clear()
    st.rerun()
