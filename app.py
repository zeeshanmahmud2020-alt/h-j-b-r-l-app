import streamlit as st
import random

# 1. THE SOUL: Custom HTML/CSS Engine
st.set_page_config(page_title="H-J-B-R-L PRO", layout="centered")

st.markdown("""
    <style>
    /* Force the entire app to stay compact */
    .main { background-color: #121212; }
    .block-container { max-width: 500px !important; padding: 1rem !important; }

    /* THE BOARD: Forced Square Grid */
    .stButton > button[key^="b_"] {
        background-color: #263238 !important;
        border: 1px solid #37474f !important;
        color: #546e7a !important;
        width: 40px !important;
        height: 40px !important;
        min-width: 40px !important;
        border-radius: 2px !important;
        padding: 0px !important;
        margin: 0px !important;
    }

    /* THE RACK: Physical Wood Style */
    .rack-bar {
        background: linear-gradient(to bottom, #8d6e63, #4e342e);
        padding: 10px;
        border-bottom: 6px solid #2d1b15;
        display: flex;
        justify-content: center;
        gap: 4px;
        margin-top: 20px;
    }

    /* THE TILES: Wooden blocks with Subscripts */
    div.stButton > button[key^="h_"] {
        background-color: #ffe082 !important;
        color: #3e2723 !important;
        width: 48px !important;
        height: 55px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        border: 1px solid #d4a017 !important;
        box-shadow: 0 4px 0 #b38b4d !important;
    }
    
    /* Highlight the selected tile */
    div.stButton > button:active, div.stButton > button:focus {
        border: 2px solid #ffffff !important;
        background-color: #ffd54f !important;
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
        'selected_idx': None
    })

# 3. Game Header
st.markdown("<h2 style='text-align:center; color:#ffe082;'>𝐇-𝐉-𝐁-𝐑-𝐋 𝐏𝐑𝐎</h2>", unsafe_allow_html=True)

# 4. The 11x11 Board
# Using fixed container to stop the "Barcode" stretching
with st.container():
    for r in range(11):
        cols = st.columns(11)
        for c in range(11):
            val = st.session_state.board[r][c]
            if cols[c].button(val if val else " ", key=f"b_{r}_{c}"):
                if st.session_state.selected_idx is not None:
                    # Place tile
                    tile_data = st.session_state.hand[st.session_state.selected_idx]
                    st.session_state.board[r][c] = tile_data[0]
                    # Refill hand
                    st.session_state.hand[st.session_state.selected_idx] = random.choice(TILES)
                    st.session_state.selected_idx = None
                    st.rerun()

# 5. THE RACK (The Holder)
st.write("---")
h_cols = st.columns(7)
for i, (char, pts) in enumerate(st.session_state.hand):
    pt_sub = "".join(SUB.get(d, d) for d in str(pts))
    if h_cols[i].button(f"{char}{pt_sub}", key=f"h_{i}"):
        st.session_state.selected_idx = i
        st.rerun()

st.markdown("<div style='text-align:center; color:#8d6e63;'>═══ WOODEN RACK ═══</div>", unsafe_allow_html=True)
