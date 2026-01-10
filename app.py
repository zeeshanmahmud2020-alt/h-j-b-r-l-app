import streamlit as st
import random

# 1. PAGE CONFIG & STYLES
st.set_page_config(page_title="Bengali Scrabble PRO", layout="centered")

st.markdown("""
    <style>
    /* Prevent the 'barcode' stretching */
    .block-container { max-width: 550px !important; padding: 10px !important; }
    
    /* Board Button Styling */
    div.stButton > button[key^="b_"] {
        background-color: #2c3e50 !important;
        color: #ecf0f1 !important;
        border: 1px solid #34495e !important;
        height: 42px !important;
        width: 100% !important;
        padding: 0px !important;
        font-weight: bold !important;
    }

    /* Rack/Hand Button Styling */
    div.stButton > button[key^="h_"] {
        background-color: #f1c40f !important;
        color: #2c3e50 !important;
        height: 55px !important;
        width: 100% !important;
        font-size: 18px !important;
        border-radius: 8px !important;
        border: 2px solid #d4ac0d !important;
    }

    /* Selected Tile Highlight */
    div.stButton > button.selected-tile {
        border: 3px solid #e74c3c !important;
        background-color: #ffeb3b !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. GAME DATA
TILES = [('কা',1), ('কি',2), ('কু',3), ('পা',2), ('মা',1), ('বা',2), ('রে',3), ('লা',2), ('না',1)]

# Initialize session states
if 'board' not in st.session_state:
    st.session_state.board = [["" for _ in range(11)] for _ in range(11)]
if 'hand' not in st.session_state:
    st.session_state.hand = random.sample(TILES, 7)
if 'sel_idx' not in st.session_state:
    st.session_state.sel_idx = None
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'turn_pts' not in st.session_state:
    st.session_state.turn_pts = 0

# 3. UI HEADER
st.title("Bengali Scrabble")
col_score1, col_score2 = st.columns(2)
col_score1.metric("Total Score", st.session_state.score)
col_score2.metric("Turn Points", st.session_state.turn_pts)

# 4. THE BOARD (11x11 Grid)
for r in range(11):
    cols = st.columns(11)
    for c in range(11):
        tile_label = st.session_state.board[r][c]
        if cols[c].button(tile_label if tile_label else " ", key=f"b_{r}_{c}"):
            if st.session_state.sel_idx is not None:
                char, pts = st.session_state.hand[st.session_state.sel_idx]
                st.session_state.board[r][c] = char
                st.session_state.turn_pts += pts
                # Replace tile in hand and reset selection
                st.session_state.hand[st.session_state.sel_idx] = random.choice(TILES)
                st.session_state.sel_idx = None
                st.rerun()

st.write("### Your Hand (Select a tile to place)")

# 5. THE RACK (7 Tiles)
h_cols = st.columns(7)
for i, (char, pts) in enumerate(st.session_state.hand):
    # Apply a special class if this tile is selected
    is_selected = "selected-tile" if st.session_state.sel_idx == i else ""
    
    if h_cols[i].button(f"{char}\n{pts}", key=f"h_{i}"):
        st.session_state.sel_idx = i
        st.rerun()

st.divider()

# 6. ACTION BUTTONS
if st.button("🔥 SUBMIT WORD", use_container_width=True):
    if st.session_state.turn_pts > 0:
        st.session_state.score += st.session_state.turn_pts
        st.session_state.turn_pts = 0
        st.success("Word Submitted!")
        st.rerun()
    else:
        st.warning("Place tiles on the board first!")

if st.button("🔄 Reset Board", type="secondary"):
    st.session_state.board = [["" for _ in range(11)] for _ in range(11)]
    st.session_state.turn_pts = 0
    st.rerun()
