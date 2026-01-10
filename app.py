import streamlit as st
import random

# 1. THE ENGINE: CSS Grid for a real board look
st.set_page_config(page_title="হ য ব র ল PRO", layout="centered")

st.markdown("""
    <style>
    .block-container { max-width: 550px !important; padding: 10px !important; }
    
    /* THE BOARD: No more 'button gaps' */
    .board-grid {
        display: grid;
        grid-template-columns: repeat(11, 1fr);
        gap: 2px;
        background-color: #1a1a1a;
        padding: 5px;
        border: 4px solid #3d2b1f;
        border-radius: 4px;
    }

    /* TILES: Real wooden board look */
    div.stButton > button {
        border-radius: 2px !important;
        margin: 0 !important;
        width: 100% !important;
        aspect-ratio: 1/1 !important;
    }

    /* Board Tile Colors */
    div.stButton > button[key^="b_"] {
        background-color: #2c3e50 !important;
        color: #ecf0f1 !important;
        font-size: 16px !important;
        border: 1px solid #34495e !important;
    }

    /* Rack Tile Colors */
    div.stButton > button[key^="h_"] {
        background-color: #f3cf7a !important;
        color: #3e2723 !important;
        font-weight: bold !important;
        box-shadow: 0 4px 0 #b38b4d !important;
    }
    
    .active-p { color: #00d2ff; font-weight: bold; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA & STATE
TILES = [('কা',1), ('কি',2), ('কু',3), ('পা',2), ('মা',1), ('বা',2), ('রে',3), ('লা',2), ('না',1)]

for key in ['board', 'p1_score', 'p2_score', 'turn', 'sel_idx', 'hand']:
    if 'board' not in st.session_state: st.session_state.board = [["" for _ in range(11)] for _ in range(11)]
    if 'hand' not in st.session_state: st.session_state.hand = random.sample(TILES, 7)
    if 'p1_score' not in st.session_state: st.session_state.p1_score, st.session_state.p2_score = 0, 0
    if 'turn' not in st.session_state: st.session_state.turn = 1
    if 'sel_idx' not in st.session_state: st.session_state.sel_idx = None

# 3. SCOREBOARD
st.markdown("<h1 style='text-align: center;'>হ য ব র ল</h1>", unsafe_allow_html=True)
s1, s2 = st.columns(2)
s1.markdown(f"<div class='{'active-p' if st.session_state.turn==1 else ''}'>PLAYER 1: {st.session_state.p1_score}</div>", unsafe_allow_html=True)
s2.markdown(f"<div class='{'active-p' if st.session_state.turn==2 else ''}'>PLAYER 2: {st.session_state.p2_score}</div>", unsafe_allow_html=True)

# 4. THE LEGIT BOARD
# Using a container and manual columns to simulate the grid accurately
board_container = st.container()
with board_container:
    for r in range(11):
        cols = st.columns(11)
        for c in range(11):
            val = st.session_state.board[r][c]
            if cols[c].button(val if val else " ", key=f"b_{r}_{c}"):
                if st.session_state.sel_idx is not None:
                    char, pts = st.session_state.hand[st.session_state.sel_idx]
                    st.session_state.board[r][c] = char
                    if st.session_state.turn == 1: st.session_state.p1_score += pts
                    else: st.session_state.p2_score += pts
                    st.session_state.hand[st.session_state.sel_idx] = random.choice(TILES)
                    st.session_state.sel_idx = None
                    st.rerun()

# 5. THE RACK
st.write("### Your Tiles")
h_cols = st.columns(7)
for i, (char, pts) in enumerate(st.session_state.hand):
    if h_cols[i].button(f"{char}", key=f"h_{i}"):
        st.session_state.sel_idx = i
        st.rerun()

if st.button("DONE / SWITCH TURN", use_container_width=True):
    st.session_state.turn = 2 if st.session_state.turn == 1 else 1
    st.rerun()
