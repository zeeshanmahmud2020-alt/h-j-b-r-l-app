import streamlit as st
import random

# 1. Compact Styling (9x9 Grid)
st.set_page_config(page_title="H-J-B-R-L PRO", layout="centered")
st.markdown("""
    <style>
    .grid-container {
        display: grid;
        grid-template-columns: repeat(9, 40px);
        grid-gap: 4px;
        justify-content: center;
        background-color: #2c3e50;
        padding: 10px;
        border-radius: 10px;
    }
    .cell {
        width: 40px; height: 40px;
        background-color: #34495e;
        border: 1px solid #444;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; font-size: 14px; color: white;
        cursor: pointer;
    }
    .bonus-3w { background-color: #d35400 !important; } /* Orange */
    .bonus-2l { background-color: #2980b9 !important; } /* Blue */
    </style>
    """, unsafe_allow_html=True)

# 2. Syllable Data & Game State
CONSONANTS = {'ক': 1, 'ম': 1, 'প': 2, 'ব': 2, 'ঘ': 8, 'হ': 4}
MATRAS = {'': 0, 'া': 1, 'ি': 2, 'ু': 3}

if 'board' not in st.session_state:
    st.session_state.board = [["" for _ in range(9)] for _ in range(9)]
    st.session_state.hand = [f"{random.choice(list(CONSONANTS))}{random.choice(list(MATRAS))}" for _ in range(7)]
    st.session_state.selected_tile = None

# 3. Game UI
st.title("𝐇-𝐉-𝐁-𝐑-𝐋 𝐁𝐃")

# The Board (Compact 9x9)
st.write("### The Board")
# Streamlit buttons in a loop to act as the board
for r in range(9):
    cols = st.columns(9)
    for c in range(9):
        label = st.session_state.board[r][c] if st.session_state.board[r][c] != "" else " "
        if cols[c].button(label, key=f"b_{r}_{c}"):
            if st.session_state.selected_tile:
                st.session_state.board[r][c] = st.session_state.selected_tile
                st.session_state.hand.remove(st.session_state.selected_tile)
                st.session_state.selected_tile = None
                st.rerun()

# 4. The Player's Hand (Compact & Clickable)
st.write("---")
st.write(f"### Your Hand (Selected: **{st.session_state.selected_tile}**)")
h_cols = st.columns(7)
for i, tile in enumerate(st.session_state.hand):
    if h_cols[i].button(tile, key=f"h_{i}"):
        st.session_state.selected_tile = tile
        st.rerun()

st.button("Clear Board", on_click=lambda: st.session_state.clear())
