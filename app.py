import streamlit as st
import random

# 1. THE SOUL: CSS Hard-Lock (Kills the "Barcode" look)
st.set_page_config(page_title="হ য ব র ল PRO", layout="centered")

st.markdown("""
    <style>
    .block-container { max-width: 550px !important; padding: 10px !important; }
    
    /* THE BOARD: Forced 1:1 Squares */
    div.stButton > button[key^="b_"] {
        background-color: #1e272e !important;
        color: #ecf0f1 !important;
        border: 1px solid #3d4e5f !important;
        width: 42px !important; 
        height: 42px !important; 
        padding: 0px !important;
        margin: 0px !important;
        font-size: 16px !important;
    }

    /* THE RACK: Zero-Gap wooden holder */
    .rack-container {
        display: flex; justify-content: center; gap: 2px;
        background: linear-gradient(#8b5a2b, #5d3a1a);
        padding: 10px; border-bottom: 5px solid #3d2611;
        border-radius: 4px; margin-top: 20px;
    }
    
    div.stButton > button[key^="h_"] {
        background-color: #f3cf7a !important;
        color: #3e2723 !important;
        width: 52px !important; height: 62px !important;
        border: 1px solid #b38b4d !important;
        box-shadow: 0 4px 0 #b38b4d !important;
        font-weight: bold !important;
    }

    /* Active Player indicator */
    .active { border-bottom: 3px solid #00d2ff; color: #00d2ff; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA & STATE
TILES = [('কা',1), ('কি',2), ('কু',3), ('পা',2), ('মা',1), ('বা',2), ('রে',3), ('লা',2), ('না',1)]
SUB = {"1":"₁", "2":"₂", "3":"₃", "4":"₄", "5":"₅", "6":"₆", "7":"₇", "8":"₈", "9":"₉", "0":"₀"}

if 'board' not in st.session_state: st.session_state.board = [["" for _ in range(11)] for _ in range(11)]
if 'hand' not in st.session_state: st.session_state.hand = random.sample(TILES, 7)
if 'scores' not in st.session_state: st.session_state.scores = {"Player 1": 0, "Player 2": 0}
if 'turn' not in st.session_state: st.session_state.turn = "Player 1"
if 'sel_idx' not in st.session_state: st.session_state.sel_idx = None

# 3. HEADER & SCOREBOARD
st.markdown("<h1 style='text-align: center;'>হ য ব র ল</h1>", unsafe_allow_html=True)
s1, s2 = st.columns(2)
s1.markdown(f"<div class='{'active' if st.session_state.turn == 'Player 1' else ''}' style='text-align:center;'>PLAYER 1: {st.session_state.scores['Player 1']}</div>", unsafe_allow_html=True)
s2.markdown(f"<div class='{'active' if st.session_state.turn == 'Player 2' else ''}' style='text-align:center;'>PLAYER 2: {st.session_state.scores['Player 2']}</div>", unsafe_allow_html=True)

# 4. THE BOARD (Perfect Grid)
for r in range(11):
    cols = st.columns(11)
    for c in range(11):
        val = st.session_state.board[r][c]
        if cols[c].button(val if val else " ", key=f"b_{r}_{c}"):
            if st.session_state.sel_idx is not None:
                char, pts = st.session_state.hand[st.session_state.sel_idx]
                st.session_state.board[r][c] = char
                st.session_state.scores[st.session_state.turn] += pts
                st.session_state.hand[st.session_state.sel_idx] = random.choice(TILES)
                st.session_state.sel_idx = None
                st.rerun()

# 5. THE RACK (The Holder)
st.markdown("<div class='rack-container'>", unsafe_allow_html=True)
h_cols = st.columns(7)
for i, (char, pts) in enumerate(st.session_state.hand):
    pt_sub = "".join(SUB.get(d, d) for d in str(pts))
    if h_cols[i].button(f"{char}{pt_sub}", key=f"h_{i}"):
        st.session_state.sel_idx = i
        st.rerun()

if st.button(f"DONE / SWITCH TO {'PLAYER 2' if st.session_state.turn == 'Player 1' else 'PLAYER 1'}", use_container_width=True):
    st.session_state.turn = "Player 2" if st.session_state.turn == "Player 1" else "Player 1"
    st.rerun()
