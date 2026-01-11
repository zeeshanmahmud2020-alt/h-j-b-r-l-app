import streamlit as st
import unicodedata
import requests
import re

# --- ARCHITECTURAL STATE (Memory) ---
if 'board' not in st.session_state:
    st.session_state.board = [["" for _ in range(9)] for _ in range(9)]
if 'total_score' not in st.session_state:
    st.session_state.total_score = 0

# --- THE UNIFIED SYSTEM ---
def get_akshara_tiles(word):
    # The atomic unit of Bengali Scrabble
    cluster_pattern = r'[\u0985-\u09b9\u09ce\u09dc-\u09df][\u09be-\u09cc\u09cd\u0981\u0982\u0983]*|[\u0985-\u0994]'
    return re.findall(cluster_pattern, word)

# --- THE BOARD UI ---
st.title("🏛️ Bengali Scrabble Arena (9x9)")

# Render Grid
for r in range(9):
    cols = st.columns(9)
    for c in range(9):
        tile_val = st.session_state.board[r][c]
        # Multiplier Colors: (4,4) is Center Star
        color = "#FFD700" if (r, c) == (4, 4) else "#f0f2f6"
        cols[c].markdown(
            f"<div style='height:40px; border:1px solid #333; background:{color}; "
            f"text-align:center; line-height:40px; color:black; font-weight:bold;'>"
            f"{tile_val}</div>", unsafe_allow_html=True
        )

# --- THE CONTROLLER ---
st.divider()
word_input = st.text_input("Enter Validated Word:")
if word_input:
    # (Assuming validation logic from Phase 1 is above this)
    tiles = get_akshara_tiles(word_input)
    st.write(f"Tiles to place: {tiles}")
    
    col_row, col_col, col_dir = st.columns(3)
    start_r = col_row.number_input("Start Row", 0, 8, key="row")
    start_c = col_col.number_input("Start Col", 0, 8, key="col")
    direction = col_dir.selectbox("Direction", ["Horizontal", "Vertical"])

    if st.button("Confirm Placement"):
        # The Machine projects tiles onto the 2D Array
        for i, tile in enumerate(tiles):
            r = start_r + (i if direction == "Vertical" else 0)
            c = start_c + (i if direction == "Horizontal" else 0)
            
            if r < 9 and c < 9:
                st.session_state.board[r][c] = tile
        
        st.success("Placement Successful.")
        st.rerun()
