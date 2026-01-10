import streamlit as st
import random

st.set_page_config(page_title="H-J-B-R-L PRO", layout="centered")

# 1. THE SOUL: Fixed-Pixel CSS (No more stretching)
st.markdown("""
    <style>
    /* Force the main container to be narrow */
    .block-container { max-width: 500px !important; padding-top: 2rem !important; }
    
    /* THE BOARD: 11x11 Square Grid */
    .board-container {
        display: grid;
        grid-template-columns: repeat(11, 40px);
        grid-template-rows: repeat(11, 40px);
        gap: 2px;
        justify-content: center;
        background-color: #1a1a1a;
        padding: 5px;
        border: 4px solid #333;
    }

    /* THE RACK: Solid Wooden Bar */
    .rack-visual {
        background: linear-gradient(to bottom, #8b5a2b, #5d3a1a);
        width: 440px; /* 11 tiles * 40px */
        height: 70px;
        margin: 20px auto;
        display: flex;
        justify-content: center;
        align-items: center;
        border-bottom: 6px solid #3d2611;
        border-radius: 4px;
        gap: 2px;
    }

    /* TILE STYLING */
    div.stButton > button {
        padding: 0px !important;
        border-radius: 2px !important;
        font-family: 'Arial', sans-serif !important;
    }
    
    /* Board Buttons */
    div.stButton > button[key^="b_"] {
        background-color: #2c3e50 !important;
        color: #5d6d7e !important;
        width: 40px !important; height: 40px !important;
        border: 0.5px solid #1a252f !important;
    }

    /* Rack Buttons (The Wood Tiles) */
    div.stButton > button[key^="h_"] {
        background-color: #f3cf7a !important;
        color: #3d2b1f !important;
        width: 45px !important; height: 55px !important;
        font-size: 22px !important;
        font-weight: bold !important;
        border: 1px solid #b38b4d !important;
        box-shadow: 0px 4px 0px #b38b4d !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Logic: Syllables & Subscripts
SUB = {"1":"₁", "2":"₂", "3":"₃", "4":"₄", "5":"₅", "6":"₆", "7":"₇", "8":"₈", "9":"₉", "0":"₀"}
TILES = [('কা',1), ('কি',2), ('কু',3), ('পা',2), ('মা',1), ('বা',2), ('রে',3), ('লা',2), ('না',1)]

if 'board' not in st.session_state:
    st.session_state.update({
        'board': [["" for _ in range(11)] for _ in range(11)],
        'hand': random.sample(TILES, 7),
        'selected': None
    })

# 3. Game UI
st.markdown("<h2 style='text-align: center; color: white;'>𝐇-𝐉-𝐁-𝐑-𝐋 𝐏𝐑𝐎</h2>", unsafe_allow_html=True)

# The Square Board
for r in range(11):
    cols = st.columns(11)
    for c in range(11):
        val = st.session_state.board[r][c]
        if cols[c].button(val if val else " ", key=f"b_{r}_{c}"):
            if st.session_state.selected:
                st.session_state.board[r][c] = st.session_state.selected[0]
                st.session_state.hand.remove(st.session_state.selected)
                st.session_state.hand.append(random.choice(TILES))
                st.session_state.selected = None
                st.rerun()

# 4. THE RACK (The Holder)
st.write("---")
h_cols = st.columns([1,1,1,1,1,1,1,1,1,1,1]) # Use 11 slots to center the 7 tiles
for i, (char, pts) in enumerate(st.session_state.hand):
    pt_sub = "".join(SUB.get(d, d) for d in str(pts))
    # We place the 7 tiles starting from the 3rd column to center them
    if h_cols[i+2].button(f"{char}{pt_sub}", key=f"h_{i}"):
        st.session_state.selected = (char, pts)
        st.rerun()

st.markdown("<div style='text-align:center; color:#8b5a2b; font-weight:bold;'>═══ RACK ═══</div>", unsafe_allow_html=True)
