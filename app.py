import streamlit as st
import random

st.set_page_config(page_title="H-J-B-R-L PRO", layout="centered")

# 1. THE SOUL: Tight Grid & Physical Rack
st.markdown("""
    <style>
    /* Tight Board - No Gaps */
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    div.stButton > button { border-radius: 0px !important; margin: 0px !important; padding: 0px !important; }

    /* The Board Tiles */
    div.stButton > button[key^="b_"] {
        background-color: #2c3e50 !important; color: #5d6d7e !important;
        height: 35px !important; width: 35px !important; border: 0.5px solid #1a252f !important;
    }

    /* THE RACK (The physical wooden bar) */
    .rack-visual {
        background: linear-gradient(to bottom, #8b5a2b, #5d3a1a);
        padding: 10px; border-radius: 2px; border-bottom: 5px solid #3d2611;
        display: flex; justify-content: center; margin-top: 20px;
    }

    /* The Wooden Tiles in the Rack */
    div.stButton > button[key^="h_"] {
        background-color: #f3cf7a !important; color: #3d2b1f !important;
        height: 50px !important; width: 45px !important;
        font-size: 20px !important; border: 1px solid #b38b4d !important;
        box-shadow: inset 0px -3px 0px #b38b4d !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Logic: Syllables & Subscripts
# Subscript map: 0-9
SUB = {"1":"₁", "2":"₂", "3":"₃", "4":"₄", "5":"₅", "6":"₆", "7":"₇", "8":"₈", "9":"₉", "0":"₀"}
TILES = [('কা',1), ('কি',2), ('কু',3), ('কে',4), ('কো',5), ('পা',2), ('মা',1), ('বা',2), ('রে',3), ('লা',2)]

if 'board' not in st.session_state:
    st.session_state.update({
        'board': [["" for _ in range(11)] for _ in range(11)],
        'hand': random.sample(TILES, 7),
        'selected': None,
        'checkpoint': None
    })

# 3. Board Header & Checkpoint
c1, c2 = st.columns([3, 1])
with c1: st.title("𝐇-𝐉-𝐁-𝐑-𝐋 𝐏𝐑𝐎")
with c2: 
    if st.button("💾 CHECKPOINT"):
        st.session_state.checkpoint = [row[:] for row in st.session_state.board]
        st.toast("Match Saved!")

# 4. The 11x11 Compact Board
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

# 5. THE RACK (Visual Container)
st.markdown("<div class='rack-visual'>", unsafe_allow_html=True)
h_cols = st.columns(7)
for i, (char, pts) in enumerate(st.session_state.hand):
    pt_sub = "".join(SUB.get(d, d) for d in str(pts))
    if h_cols[i].button(f"{char}{pt_sub}", key=f"h_{i}"):
        st.session_state.selected = (char, pts)
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.checkpoint:
    if st.sidebar.button("⏪ Load Checkpoint"):
        st.session_state.board = [row[:] for row in st.session_state.checkpoint]
        st.rerun()
