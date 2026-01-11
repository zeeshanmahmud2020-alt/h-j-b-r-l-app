import streamlit as st
import numpy as np

# 1. INITIALIZE THE BOARD MEMORY
if 'board' not in st.session_state:
    st.session_state.board = [["" for _ in range(9)] for _ in range(9)]

# 2. DEFINE THE MULTIPLIER MAP (9x9)
# 1: Normal, 2: Double Letter, 3: Double Word
MULTIPLIERS = [
    [3, 1, 1, 2, 1, 2, 1, 1, 3],
    [1, 2, 1, 1, 1, 1, 1, 2, 1],
    [1, 1, 2, 1, 1, 1, 2, 1, 1],
    [2, 1, 1, 2, 1, 2, 1, 1, 2],
    [1, 1, 1, 1, 3, 1, 1, 1, 1], # 3 is the Center Star
    [2, 1, 1, 2, 1, 2, 1, 1, 2],
    [1, 1, 2, 1, 1, 1, 2, 1, 1],
    [1, 2, 1, 1, 1, 1, 1, 2, 1],
    [3, 1, 1, 2, 1, 2, 1, 1, 3]
]

# 3. RENDER THE VISUAL BOARD
st.subheader("🧱 9x9 Scrabble Arena")
cols = st.columns(9)
for r in range(9):
    for c in range(9):
        val = st.session_state.board[r][c]
        # Color coding for multipliers
        m = MULTIPLIERS[r][c]
        bg = "#ff4b4b" if m == 3 else ("#1c83e1" if m == 2 else "#f0f2f6")
        cols[c].markdown(
            f"<div style='height:40px; width:40px; background:{bg}; color:black; "
            f"display:flex; align-items:center; justify-content:center; border:1px solid #ccc; "
            f"font-weight:bold;'>{val}</div>", unsafe_allow_html=True
        )

# 4. PLACEMENT CONTROLS
st.divider()
with st.expander("🛠️ Place Word on Board"):
    row = st.number_input("Row (0-8)", 0, 8)
    col = st.number_input("Column (0-8)", 0, 8)
    direction = st.radio("Direction", ["Horizontal", "Vertical"])
    
    if st.button("Apply Move"):
        if 'tiles' in locals() or 'tiles' in globals():
            for i, tile in enumerate(tiles):
                r_idx = row + (i if direction == "Vertical" else 0)
                c_idx = col + (i if direction == "Horizontal" else 0)
                if r_idx < 9 and c_idx < 9:
                    st.session_state.board[r_idx][c_idx] = tile
            st.rerun()
