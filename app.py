import streamlit as st
import random

# 1. THE SOUL: Hard-Locked CSS (Prevents the "Barcode" stretching)
st.set_page_config(page_title="হ য ব র ল PRO", layout="centered")

st.markdown("""
    <style>
    .block-container { max-width: 500px !important; padding: 10px !important; }
    
    /* THE RACK: Physical bar */
    .rack-container {
        display: flex; justify-content: center; gap: 4px;
        background: linear-gradient(#8b5a2b, #5d3a1a);
        padding: 12px; border-bottom: 6px solid #3d2611;
        margin-top: 20px; border-radius: 4px;
    }

    /* TILES: Wooden look */
    div.stButton > button { border-radius: 2px !important; font-family: sans-serif !important; }
    
    /* Board Tiles (Forced Squares) */
    div.stButton > button[key^="b_"] {
        background-color: #263238 !important; color: #546e7a !important;
        width: 38px !important; height: 38px !important; border: 1px solid #1a252f !important;
    }

    /* Rack Tiles */
    div.stButton > button[key^="h_"] {
        background-color: #f3cf7a !important; color: #3e2723 !important;
        width: 45px !important; height: 55px !important; font-size: 20px !important;
        border: 1px solid #b38b4d !important; box-shadow: 0 4px 0 #b38b4d !important;
    }

    /* SUBMIT BUTTON: Green Professional Look */
    div.stButton > button[key="submit_btn"] {
        background-color: #27ae60 !important; color: white !important;
        width: 100% !important; height: 50px !important; font-size: 20px !important;
        margin-top: 20px !important; border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Logic: Fixed Attribute Errors & Scoring
SUB = {"1":"₁", "2":"₂", "3":"₃", "4":"₄", "5":"₅", "6":"₆", "7":"₇", "8":"₈", "9":"₉", "0":"₀"}
TILES = [('কা',1), ('কি',2), ('কু',3), ('পা',2), ('মা',1), ('বা',2), ('রে',3), ('লা',2), ('না',1)]

# Initialize session states to prevent crashes
if 'board' not in st.session_state: st.session_state.board = [["" for _ in range(11)] for _ in range(11)]
if 'hand' not in st.session_state: st.session_state.hand = random.sample(TILES, 7)
if 'sel_idx' not in st.session_state: st.session_state.sel_idx = None
if 'score' not in st.session_state: st.session_state.score = 0
if 'placed_tiles' not in st.session_state: st.session_state.placed_tiles = []

st.markdown(f"<h2 style='text-align:center;'>Score: {st.session_state.score}</h2>", unsafe_allow_html=True)

# 3. The Board
for r in range(11):
    cols = st.columns(11)
    for c in range(11):
        val = st.session_state.board[r][c]
        if cols[c].button(val if val else " ", key=f"b_{r}_{c}"):
            if st.session_state.sel_idx is not None:
                tile_data = st.session_state.hand[st.session_state.sel_idx]
                st.session_state.board[r][c] = tile_data[0]
                st.session_state.placed_tiles.append(tile_data[1]) # Track points
                st.session_state.hand[st.session_state.sel_idx] = random.choice(TILES)
                st.session_state.sel_idx = None
                st.rerun()

# 4. The Rack
st.markdown("<div class='rack-container'>", unsafe_allow_html=True)
h_cols = st.columns(7)
for i, (char, pts) in enumerate(st.session_state.hand):
    pt_sub = "".join(SUB.get(d, d) for d in str(pts))
    if h_cols[i].button(f"{char}{pt_sub}", key=f"h_{i}"):
        st.session_state.sel_idx = i
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# 5. THE SUBMIT BUTTON
if st.button("🔥 SUBMIT WORD", key="submit_btn"):
    if st.session_state.placed_tiles:
        st.session_state.score += sum(st.session_state.placed_tiles)
        # Clear the board or keep the word? Keeping for now to feel like a real game.
        st.session_state.placed_tiles = [] 
        st.toast("Word Submitted!")
        st.rerun()
    else:
        st.error("Place some tiles first!")
