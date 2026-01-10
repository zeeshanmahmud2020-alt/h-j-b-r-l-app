import streamlit as st
import random

# 1. CSS for a compact, professional board
st.set_page_config(page_title="H-J-B-R-L PRO", layout="centered")
st.markdown("""
    <style>
    div.stButton > button { 
        width: 100% !important; height: 45px !important; 
        font-size: 16px !important; padding: 0px !important;
    }
    .tile-hand button { 
        background-color: #f3cf7a !important; color: #3d2b1f !important;
        font-weight: bold !important; border-bottom: 3px solid #b38b4d !important;
    }
    .board-cell button { background-color: #34495e !important; color: white !important; }
    .selected { border: 2px solid #f1c40f !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Syllabic Matrix (Meme-style pre-combined letters)
CONS = ['ক', 'খ', 'গ', 'চ', 'জ', 'ত', 'দ', 'ন', 'প', 'ব', 'ম', 'র', 'ল', 'স', 'হ']
MATRAS = ['', 'া', 'ি', 'ু', 'ে', 'ো']

if 'board' not in st.session_state:
    st.session_state.board = [["" for _ in range(9)] for _ in range(9)]
    st.session_state.hand = [random.choice(CONS) + random.choice(MATRAS) for _ in range(7)]
    st.session_state.selected = None
    st.session_state.score = 0

# 3. Game UI
st.title("𝐇-𝐉-𝐁-𝐑-𝐋 𝐏𝐑𝐎")
st.write(f"### Score: {st.session_state.score} | Selected: {st.session_state.selected if st.session_state.selected else 'None'}")

# The 9x9 Board
for r in range(9):
    cols = st.columns(9)
    for c in range(9):
        val = st.session_state.board[r][c]
        if cols[c].button(val if val else " ", key=f"b_{r}_{c}"):
            if st.session_state.selected:
                st.session_state.board[r][c] = st.session_state.selected
                st.session_state.hand.remove(st.session_state.selected)
                # Refill hand automatically
                st.session_state.hand.append(random.choice(CONS) + random.choice(MATRAS))
                st.session_state.selected = None
                st.rerun()

# 4. The Player's Hand
st.write("---")
st.write("### Your Tiles (Click to select)")
h_cols = st.columns(7)
for i, tile in enumerate(st.session_state.hand):
    if h_cols[i].button(tile, key=f"h_{i}"):
        st.session_state.selected = tile
        st.rerun()

if st.sidebar.button("Reset Game"):
    st.session_state.clear()
    st.rerun()
