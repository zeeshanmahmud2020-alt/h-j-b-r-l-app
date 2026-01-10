import streamlit as st
import random

# 1. SETUP & STYLE
st.set_page_config(page_title="Bengali Scrabble", layout="centered")

st.markdown("""
    <style>
    .block-container { max-width: 550px !important; padding: 10px !important; }
    
    /* The Board Grid */
    div[data-testid="stHorizontalBlock"] { gap: 2px !important; }
    
    /* Board Buttons */
    button[key^="b_"] {
        background-color: #2c3e50 !important;
        border: 1px solid #34495e !important;
        color: #ecf0f1 !important;
        height: 40px !important;
        width: 40px !important;
        padding: 0px !important;
    }

    /* Hand/Rack Buttons */
    button[key^="h_"] {
        background-color: #f1c40f !important;
        color: #2c3e50 !important;
        font-weight: bold !important;
        height: 50px !important;
        border-radius: 5px !important;
    }
    
    /* Highlight Selected Tile */
    .selected { border: 3px solid #e74c3c !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA & SESSION STATE
TILES = [('কা',1), ('কি',2), ('কু',3), ('পা',2), ('মা',1), ('বা',2), ('রে',3), ('লা',2), ('না',1)]

if 'board' not in st.session_state: 
    st.session_state.board = [["" for _ in range(11)] for _ in range(11)]
if 'hand' not in st.session_state: 
    st.session_state.hand = random.sample(TILES, 7)
if 'sel_idx' not in st.session_state: 
    st.session_state.sel_idx = None
if 'score' not in st.session_state: 
    st.session_state.score = 0
if 'turn_points' not in st.session_state: 
    st.session_state.turn_points = 0

# 3. GAME UI
st.title(f"Score: {st.session_state.score}")

# Render Board
for r in range(11):
    cols = st.columns(11)
    for c in range(11):
        tile_val = st.session_state.board[r][c
