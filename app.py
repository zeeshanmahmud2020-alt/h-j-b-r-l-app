import streamlit as st
import requests
import re
import unicodedata
import random

# --- 1. THE ECONOMY (Points and Tile Bag) ---
# Points assigned to each part of a Bengali "Tile"
GRAPHEME_VALUES = {
    'ক': 1, 'ত': 1, 'ন': 1, 'প': 1, 'র': 1, 'ল': 1, 'স': 1, 'া': 1, 'ি': 1,
    'গ': 2, 'চ': 2, 'জ': 2, 'দ': 2, 'ব': 2, 'ম': 2, 'ু': 2,
    'খ': 3, 'ছ': 3, 'ট': 3, 'থ': 3, 'ফ': 3, 'ঙ': 8, 'ঞ': 10
}

# Setup the 100-tile bag and player hands
if 'bag' not in st.session_state:
    raw_bag = (['ক', 'ন', 'প', 'র', 'ল', 'স', 'ত'] * 6 + 
               ['া', 'ি'] * 10 + 
               ['গ', 'চ', 'জ', 'দ', 'ব', 'ম'] * 4 + 
               ['ঙ', 'ঞ'] * 2)
    random.shuffle(raw_bag)
    st.session_state.bag = raw_bag
    st.session_state.p1_rack = [st.session_state.bag.pop() for _ in range(7)]
    st.session_state.p2_rack = [st.session_state.bag.pop() for _ in range(7)]

# Initialize board and scores
if 'board' not in st.session_state:
    st.session_state.board = [["" for _ in range(9)] for _ in range(9)]
if 'p1_score' not in st.session_state:
    st.session_state.p1_score = 0
if 'p2_score' not in st.session_state:
    st.session_state.p2_score = 0
if 'turn' not in st.session_state:
    st.session_state.turn = "Player 1"

# --- 2. THE DICTIONARY ---
@st.cache_data
def load_lexicon():
    url = "https://raw.githubusercontent.com/MinhasKamal/BengaliDictionary/master/BengaliDictionary_17.txt"
    try:
        r = requests.get(url)
        words = re.findall(r'[\u0980-\u09ff]+', r.text)
        return {unicodedata.normalize('NFC', w) for w in words}
    except: return set()

lexicon = load_lexicon()

# --- 3. THE BRAIN (Logic and Collision Rules) ---
def handle_submission():
    word = st.session_state.word_box_input
    if not word: return
    
    target = unicodedata.normalize('NFC', word.strip())
    
    if target in lexicon:
        # Break word into Grapheme clusters (Tiles)
        tiles_to_place = re.findall(r'[\u0980-\u09ff][\u09be-\u09cc\u09cd\u0981\u0982\u0983]*', target)
        
        # 1. COLLISION CHECK: Is the spot already taken?
        for i, t in enumerate(tiles_to_place):
            curr_r = st.session_state.row_val + (i if st.session_state.dir_val == "Vertical" else 0)
            curr_c = st.session_state.col_val + (i if st.session_state.dir_val == "Horizontal" else 0)
            
            if curr_r >= 9 or curr_c >= 9:
                st.error("❌ Word goes off the board!")
                return
            
            existing_tile = st.session_state.board[curr_r][curr_c]
            if existing_tile != "" and existing_tile != t:
                st.error(f"❌ Collision! Spot ({curr_r}, {curr_c}) has '{existing_tile}'")
                return

        # 2. SCORE CALCULATION
        word_score = sum(sum(GRAPHEME_VALUES.get(char, 0) for char in g) for g in tiles_to_place)

        # 3. PLACE TILES
        for i, t in enumerate(tiles_to_place):
            curr_r = st.session_state.row_val + (i if st.session_state.dir_val == "Vertical" else 0)
            curr_c = st.session_state.col_val + (i if st.session_state.dir_val == "Horizontal" else 0)
            st.session_state.board[curr_r][curr_c] = t

        # 4. TILE MANAGEMENT (Remove from hand, refill from bag)
        rack = st.session_state.p1_rack if st.session_state.turn == "Player 1" else st.session_state.p2_rack
        for t in tiles_to_place:
            if t in rack: rack.remove(t)
        while len(rack) < 7 and st.session_state.bag:
            rack.append(st.session_state.bag.pop())

        # 5. UPDATE SCORE AND TURN
        if st.session_state.turn == "Player 1":
            st.session_state.p1_score += word_score
            st.session_state.turn = "Player 2"
        else:
            st.session_state.p2_score += word_score
            st.session_state.turn = "Player 1"
        
        st.session_state.word_box_input = ""
    else:
        st.error("❌ Word not in dictionary!")

# --- 4. THE INTERFACE ---
st.sidebar.title("🏆 H.J.B.R.L Arena")
st.sidebar.metric("Player 1", f"{st.session_state.p1_score}")
st.sidebar.metric("Player 2", f"{st.session_state.p2_score}")
st.sidebar.info(f"Current Turn: {st.session_state.turn}")

st.sidebar.markdown("---")
st.sidebar.subheader("Your Tiles:")
current_rack = st.session_state.p1_rack if st.session_state.turn == "Player 1" else st.session_state.p2_rack
st.sidebar.warning("  ".join(current_rack))

st.title("🏛️ Bengali Scrabble Arena")
# Draw the 9x9 grid
for r in range(9):
    cols = st.columns(9)
    for c in range(9):
        tile = st.session_state.board[r][c]
        color = "#FFD700" if (r, c) == (4, 4) else "#262730"
        cols[c].markdown(f"<div style='height:45px; border:1px solid #555; background:{color}; text-align:center; line-height:45px; font-size:20px; font-weight:bold; color:white;'>{tile}</div>", unsafe_allow_html=True)

st.divider()
user_input = st.text_input("Type your Bengali word:", key="word_box_input")
c1, c2, c3 = st.columns(3)
r_start = c1.number_input("Start Row", 0, 8, key="row_val")
c_start = c2.number_input("Start Col", 0, 8, key="col_val")
orient = c3.selectbox("Direction", ["Horizontal", "Vertical"], key="dir_val")

if st.button("Confirm Move & End Turn", on_click=handle_submission):
    pass

if st.button("Reset Arena"):
    st.session_state.clear()
    st.rerun()
