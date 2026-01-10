import streamlit as st
import random

st.set_page_config(page_title="H-J-B-R-L PRO", layout="centered")

# 1. THE SOUL: Authentic Game CSS
st.markdown("""
    <style>
    /* 11x11 Compact Board */
    .board-grid {
        display: grid;
        grid-template-columns: repeat(9, 38px);
        grid-gap: 2px;
        justify-content: center;
        background-color: #1a252f;
        padding: 10px;
        border-radius: 5px;
    }
    /* The Rack (Connected Wooden Holder) */
    .rack-box {
        background: #5d3a1a;
        padding: 10px 20px;
        border-radius: 5px;
        border-bottom: 8px solid #3d2611;
        display: flex;
        justify-content: center;
        gap: 0px; /* Connected tiles */
        margin-top: 30px;
    }
    /* Super-Script Logic via Button Styling */
    div.stButton > button {
        border-radius: 2px !important;
        font-family: 'Courier New', Courier, monospace;
    }
    /* Wood Tile Style */
    div.stButton > button[key^="h_"] {
        background-color: #f3cf7a !important;
        color: #3d2b1f !important;
        width: 45px !important; height: 50px !important;
        border: 1px solid #b38b4d !important;
        font-size: 18px !important;
        line-height: 1 !important;
    }
    /* Board Cell Style */
    div.stButton > button[key^="b_"] {
        background-color: #2c3e50 !important;
        color: #ecf0f1 !important;
        width: 38px !important; height: 38px !important;
        font-size: 14px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Logic: Syllable Matrix with Points
# Format: (Syllable, Pts)
TILES = [('কা',1), ('কি',2), ('কু',3), ('কে',4), ('কো',5), ('পা',2), ('পি',3), ('মা',1), ('মি',2), ('বা',2)]

if 'board' not in st.session_state:
    st.session_state.board = [["" for _ in range(9)] for _ in range(9)]
    st.session_state.hand = random.sample(TILES, 7)
    st.session_state.selected = None

# 3. Game Interface
st.markdown("<h2 style='text-align: center;'>𝐇-𝐉-𝐁-𝐑-𝐋 𝐏𝐑𝐎</h2>", unsafe_allow_html=True)

# 4. The 9x9 Board (Tight Grid)
for r in range(9):
    cols = st.columns(9)
    for c in range(9):
        val = st.session_state.board[r][c]
        if cols[c].button(val if val else "·", key=f"b_{r}_{c}"):
            if st.session_state.selected:
                st.session_state.board[r][c] = st.session_state.selected[0]
                st.session_state.hand.remove(st.session_state.selected)
                st.session_state.hand.append(random.choice(TILES))
                st.session_state.selected = None
                st.rerun()

# 5. THE RACK (The Holder)
st.write("---")
st.markdown("<div style='text-align:center; font-weight:bold;'>THE HOLDER</div>", unsafe_allow_html=True)
h_cols = st.columns([1,1,1,1,1,1,1])
for i, (char, pts) in enumerate(st.session_state.hand):
    # Using Unicode superscript for the points
    superscripts = {"1":"¹", "2":"²", "3":"³", "4":"⁴", "5":"⁵", "6":"⁶", "7":"⁷", "8":"⁸", "9":"⁹", "0":"⁰"}
    pt_str = "".join(superscripts.get(d, d) for d in str(pts))
    
    if h_cols[i].button(f"{char}{pt_str}", key=f"h_{i}"):
        st.session_state.selected = (char, pts)
        st.rerun()

if st.session_state.selected:
    st.info(f"Picked: {st.session_state.selected[0]}. Now click a spot on the board.")
