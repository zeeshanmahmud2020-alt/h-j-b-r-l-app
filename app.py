import streamlit as st
import random

st.set_page_config(page_title="H-J-B-R-L PRO", layout="centered")

# 1. THE SOUL: High-End UI Styling
st.markdown("""
    <style>
    /* The Board Grid */
    .stButton > button { border-radius: 4px; border: none; font-weight: bold; }
    
    /* Board Cells */
    div.stButton > button[key^="b_"] {
        background-color: #2e3d49 !important; color: #5d6d7e !important;
        height: 42px !important; width: 42px !important; margin: 1px !important;
    }
    
    /* The Rack (The Holder) */
    .rack-container {
        background: linear-gradient(to bottom, #8b5a2b, #5d3a1a);
        padding: 15px; border-radius: 10px; border-bottom: 6px solid #3d2611;
        display: flex; justify-content: center; gap: 8px; margin-top: 20px;
    }
    
    /* The Wooden Tiles */
    div.stButton > button[key^="h_"] {
        background-color: #f3cf7a !important; color: #3d2b1f !important;
        height: 55px !important; width: 50px !important;
        font-size: 20px !important; border-bottom: 4px solid #b38b4d !important;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.4) !important;
    }
    
    /* Selected Tile Highlight */
    div.stButton > button[key^="h_"]:focus { border: 3px solid #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Syllabic Matrix Logic
CONS = ['ক', 'খ', 'গ', 'চ', 'জ', 'ত', 'দ', 'ন', 'প', 'ব', 'ম', 'র', 'ল', 'স', 'হ']
MATRAS = ['', 'া', 'ি', 'ু', 'ে', 'ো']

if 'board' not in st.session_state:
    st.session_state.board = [["" for _ in range(11)] for _ in range(11)]
    st.session_state.hand = [random.choice(CONS) + random.choice(MATRAS) for _ in range(7)]
    st.session_state.selected = None

# 3. Game Header
st.markdown("<h1 style='text-align: center; color: #f3cf7a;'>𝐇-𝐉-𝐁-𝐑-𝐋 𝐏𝐑𝐎</h1>", unsafe_allow_html=True)
st.write(f"**Selected:** {st.session_state.selected if st.session_state.selected else 'Click a tile from the rack'}")

# 4. The 11x11 Board
for r in range(11):
    cols = st.columns(11)
    for c in range(11):
        val = st.session_state.board[r][c]
        if cols[c].button(val if val else "·", key=f"b_{r}_{c}"):
            if st.session_state.selected:
                st.session_state.board[r][c] = st.session_state.selected
                st.session_state.hand.remove(st.session_state.selected)
                st.session_state.hand.append(random.choice(CONS) + random.choice(MATRAS))
                st.session_state.selected = None
                st.rerun()

# 5. THE HOLDER (Wooden Rack)
st.markdown("<div class='rack-container'>", unsafe_allow_html=True)
st.write("### 🪵 Your Letter Rack")
h_cols = st.columns(7)
for i, tile in enumerate(st.session_state.hand):
    if h_cols[i].button(tile, key=f"h_{i}"):
        st.session_state.selected = tile
        st.rerun()

if st.sidebar.button("Reset Game"):
    st.session_state.clear()
    st.rerun()
