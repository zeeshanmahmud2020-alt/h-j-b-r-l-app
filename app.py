import streamlit as st
import random

st.set_page_config(page_title="H-J-B-R-L PRO", layout="centered")

# 1. THE SOUL: Hard-Locked Square Grid CSS
st.markdown("""
    <style>
    /* Force a narrow, centered game container */
    .block-container { max-width: 550px !important; background-color: #121212; }

    /* THE BOARD: Forced Squares, No Stretches */
    .board-wrapper {
        display: grid;
        grid-template-columns: repeat(11, 45px);
        grid-auto-rows: 45px;
        gap: 2px;
        justify-content: center;
        background-color: #1a1a1a;
        padding: 10px;
        border: 4px solid #333;
    }

    /* THE RACK: Actual Wooden Texture & Connected Tiles */
    .wooden-rack {
        background: linear-gradient(to bottom, #8b5a2b, #5d3a1a);
        padding: 15px 10px 5px 10px;
        border-radius: 4px;
        border-bottom: 8px solid #3d2611;
        display: flex;
        justify-content: center;
        gap: 2px;
        margin-top: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }

    /* Styled Buttons to look like Real Tiles */
    div.stButton > button {
        border-radius: 2px !important;
        font-family: sans-serif !important;
        transition: transform 0.1s;
    }
    
    /* Board Button Style */
    div.stButton > button[key^="b_"] {
        background-color: #2c3e50 !important;
        color: #5d6d7e !important;
        width: 45px !important; height: 45px !important;
        border: 1px solid #141e26 !important;
    }

    /* Rack Button Style (The "Wood" Blocks) */
    div.stButton > button[key^="h_"] {
        background-color: #f3cf7a !important;
        color: #3d2b1f !important;
        width: 50px !important; height: 60px !important;
        font-size: 22px !important;
        font-weight: bold !important;
        border: 1px solid #b38b4d !important;
        box-shadow: inset 0 -4px 0 #b38b4d, 0 4px 6px rgba(0,0,0,0.3) !important;
    }
    div.stButton > button[key^="h_"]:active { transform: translateY(4px); box-shadow: none !important; }
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
st.markdown("<h1 style='text-align: center; color: #f3cf7a;'>𝐇-𝐉-𝐁-𝐑-𝐋 𝐏𝐑𝐎</h1>", unsafe_allow_html=True)

# The Square Board (Click a tile first, then click a spot)
st.write(f"**Action:** {'Select a tile from your rack' if not st.session_state.selected else f'Place {st.session_state.selected[0]} on the board'}")

with st.container():
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

# 4. THE RACK (The Physical Holder)
st.markdown("<div class='wooden-rack'>", unsafe_allow_html=True)
h_cols = st.columns([1,1,1,1,1,1,1])
for i, (char, pts) in enumerate(st.session_state.hand):
    pt_sub = "".join(SUB.get(d, d) for d in str(pts))
    if h_cols[i].button(f"{char}{pt_sub}", key=f"h_{i}"):
        st.session_state.selected = (char, pts)
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)
