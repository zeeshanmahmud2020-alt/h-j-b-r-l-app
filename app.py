import streamlit as st
import random

# 1. THE SOUL: Hard-Locked CSS Grid (No Columns)
st.set_page_config(page_title="H-J-B-R-L PRO", layout="centered")

st.markdown("""
    <style>
    /* Stop the barcode stretching */
    .block-container { max-width: 500px !important; padding: 10px !important; }
    
    /* THE BOARD: A single, locked square unit */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(11, 38px);
        grid-gap: 2px;
        justify-content: center;
        margin: 0 auto;
    }

    /* THE RACK: Physical bar at the bottom */
    .rack-container {
        display: flex;
        justify-content: center;
        gap: 4px;
        background: linear-gradient(#8b5a2b, #5d3a1a);
        padding: 12px;
        border-bottom: 6px solid #3d2611;
        margin-top: 30px;
    }

    /* TILES: Wooden look with subscript */
    div.stButton > button {
        border-radius: 2px !important;
        padding: 0px !important;
        font-family: sans-serif !important;
    }
    
    /* Board Tiles */
    div.stButton > button[key^="b_"] {
        background-color: #263238 !important;
        color: #546e7a !important;
        width: 38px !important; height: 38px !important;
        border: 1px solid #1a252f !important;
    }

    /* Rack Tiles */
    div.stButton > button[key^="h_"] {
        background-color: #f3cf7a !important;
        color: #3e2723 !important;
        width: 45px !important; height: 55px !important;
        font-size: 20px !important;
        border: 1px solid #b38b4d !important;
        box-shadow: 0 4px 0 #b38b4d !important;
    }
    
    /* Selection Highlight */
    div.stButton > button:focus { border: 2px solid white !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Logic: Fixed Attribute Errors
SUB = {"1":"₁", "2":"₂", "3":"₃", "4":"₄", "5":"₅", "6":"₆", "7":"₇", "8":"₈", "9":"₉", "0":"₀"}
TILES = [('কা',1), ('কি',2), ('কু',3), ('পা',2), ('মা',1), ('বা',2), ('রে',3), ('লা',2), ('না',1)]

if 'board' not in st.session_state:
    st.session_state.board = [["" for _ in range(11)] for _ in range(11)]
if 'hand' not in st.session_state:
    st.session_state.hand = random.sample(TILES, 7)
if 'sel_idx' not in st.session_state:
    st.session_state.sel_idx = None

st.markdown("<h2 style='text-align:center;'>𝐇-𝐉-𝐁-𝐑-𝐋 𝐏𝐑𝐎</h2>", unsafe_allow_html=True)

# 3. The Board (Fixed Layout)
for r in range(11):
    cols = st.columns(11) # Columns are only used inside this loop to stay centered
    for c in range(11):
        val = st.session_state.board[r][c]
        if cols[c].button(val if val else " ", key=f"b_{r}_{c}"):
            if st.session_state.sel_idx is not None:
                st.session_state.board[r][c] = st.session_state.hand[st.session_state.sel_idx][0]
                st.session_state.hand[st.session_state.sel_idx] = random.choice(TILES)
                st.session_state.sel_idx = None
                st.rerun()

# 4. The Rack (Visual Only)
st.markdown("<div class='rack-container'>", unsafe_allow_html=True)
h_cols = st.columns([1,1,1,1,1,1,1])
for i, (char, pts) in enumerate(st.session_state.hand):
    pt_sub = "".join(SUB.get(d, d) for d in str(pts))
    if h_cols[i].button(f"{char}{pt_sub}", key=f"h_{i}"):
        st.session_state.sel_idx = i
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)
