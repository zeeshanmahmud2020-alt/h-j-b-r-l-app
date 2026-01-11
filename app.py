import streamlit as st
import requests
import re
import unicodedata

# 1. PERMANENT MEMORY SETUP
if 'board' not in st.session_state:
    st.session_state.board = [["" for _ in range(9)] for _ in range(9)]
if 'p1_score' not in st.session_state:
    st.session_state.p1_score = 0
if 'p2_score' not in st.session_state:
    st.session_state.p2_score = 0
if 'turn' not in st.session_state:
    st.session_state.turn = "Player 1"

# 2. DICTIONARY LOADING
@st.cache_data
def load_lexicon():
    url = "https://raw.githubusercontent.com/MinhasKamal/BengaliDictionary/master/BengaliDictionary_17.txt"
    try:
        r = requests.get(url)
        words = re.findall(r'[\u0980-\u09ff]+', r.text)
        return {unicodedata.normalize('NFC', w) for w in words}
    except: return set()

lexicon = load_lexicon()

# 3. SIDEBAR SCOREBOARD
st.sidebar.title("🏆 H.J.B.R.L Arena")
st.sidebar.metric("Player 1", f"{st.session_state.p1_score}")
st.sidebar.metric("Player 2", f"{st.session_state.p2_score}")
st.sidebar.info(f"Current Turn: {st.session_state.turn}")

# 4. MAIN BOARD DISPLAY (9x9)
st.title("🏛️ Bengali Scrabble Arena")
for r in range(9):
    cols = st.columns(9)
    for c in range(9):
        tile = st.session_state.board[r][c]
        color = "#FFD700" if (r, c) == (4, 4) else "#262730"
        cols[c].markdown(f"<div style='height:45px; border:1px solid #555; background:{color}; text-align:center; line-height:45px; font-size:20px; font-weight:bold; color:white;'>{tile}</div>", unsafe_allow_html=True)

# 5. INPUT & LOGIC
st.divider()

# Function to clear the input after a successful move
def handle_submission():
    word = st.session_state.word_box_input
    if not word:
        return
    
    target = unicodedata.normalize('NFC', word.strip())
    
    if target in lexicon:
        tiles = re.findall(r'[\u0980-\u09ff][\u09be-\u09cc\u09cd\u0981\u0982\u0983]*', target)
        
        # Check for Overlap and Board Edges
        can_place = True
        for i, t in enumerate(tiles):
            curr_r = st.session_state.row_val + (i if st.session_state.dir_val == "Vertical" else 0)
            curr_c = st.session_state.col_val + (i if st.session_state.dir_val == "Horizontal" else 0)
            
            if curr_r >= 9 or curr_c >= 9:
                st.error("❌ Word goes off the board!")
                return
            
            existing = st.session_state.board[curr_r][curr_c]
            if existing != "" and existing != t:
                st.error(f"❌ Collision! Cannot overwrite '{existing}' with '{t}'.")
                return

        # Commit to Board
        for i, t in enumerate(tiles):
            curr_r = st.session_state.row_val + (i if st.session_state.dir_val == "Vertical" else 0)
            curr_c = st.session_state.col_val + (i if st.session_state.dir_val == "Horizontal" else 0)
            st.session_state.board[curr_r][curr_c] = t
        
        # Update Score
        points = len(tiles)
        if st.session_state.turn == "Player 1":
            st.session_state.p1_score += points
            st.session_state.turn = "Player 2"
        else:
            st.session_state.p2_score += points
            st.session_state.turn = "Player 1"
        
        # CLEAR THE TEXT BOX
        st.session_state.word_box_input = ""
    else:
        st.error("❌ Word not in dictionary!")

# UI Components linked to state
user_input = st.text_input("Type your Bengali word:", key="word_box_input")
c1, c2, c3 = st.columns(3)
r_start = c1.number_input("Start Row", 0, 8, key="row_val")
c_start = c2.number_input("Start Col", 0, 8, key="col_val")
orient = c3.selectbox("Direction", ["Horizontal", "Vertical"], key="dir_val")

if st.button("Confirm Move & End Turn", on_click=handle_submission):
    pass # The logic is now handled by the 'on_click' callback

if st.button("Reset Arena"):
    st.session_state.clear()
    st.rerun()
