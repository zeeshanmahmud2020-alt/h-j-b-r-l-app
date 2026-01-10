import streamlit as st
import random
import requests

# 1. GRAPHICS: Locked 11x11 Grid
st.set_page_config(page_title="হ য ব র ল PRO", layout="centered")

@st.cache_resource
def load_dict():
    # Using your uploaded/provided dictionary URL
    url = "https://raw.githubusercontent.com/tahmid02016/bangla-wordlist/master/words.txt"
    try:
        r = requests.get(url, timeout=5)
        return set(word.strip() for word in r.text.split()) # Strip whitespace for exact match
    except:
        return {"কাকা", "বাবা", "মামা", "কাকি"}

WORDS_DB = load_dict()

st.markdown("""
    <style>
    .block-container { max-width: 550px !important; padding: 10px !important; }
    div.stButton > button[key^="b_"] {
        background-color: #1e272e !important; color: #ecf0f1 !important;
        width: 44px !important; height: 44px !important;
        border: 1px solid #3d4e5f !important; padding: 0px !important;
        margin: 0px !important; font-size: 16px !important;
    }
    .rack-container {
        display: flex; justify-content: center; gap: 4px;
        background: linear-gradient(#8b5a2b, #5d3a1a);
        padding: 12px; border-bottom: 6px solid #3d2611;
        border-radius: 4px; margin-top: 10px;
    }
    div.stButton > button[key^="h_"] {
        background-color: #f3cf7a !important; color: #3e2723 !important;
        width: 52px !important; height: 60px !important;
        border: 1px solid #b38b4d !important; box-shadow: 0 4px 0 #b38b4d !important;
        font-weight: bold !important; font-size: 18px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. STATE (Fixes AttributeError and Gibberish Score)
SUB = {"1":"₁", "2":"₂", "3":"₃", "4":"₄", "5":"₅"}
POOL = [('কা',1), ('কি',2), ('কু',2), ('পা',1), ('মা',1), ('বা',1), ('রে',2), ('না',1), ('নি',2)]

if 'board' not in st.session_state: st.session_state.board = [["" for _ in range(11)] for _ in range(11)]
if 'hand' not in st.session_state: st.session_state.hand = random.sample(POOL, 7)
if 'scores' not in st.session_state: st.session_state.scores = {"P1": 0, "P2": 0}
if 'turn' not in st.session_state: st.session_state.turn = "P1"
if 'sel_idx' not in st.session_state: st.session_state.sel_idx = None
if 'turn_data' not in st.session_state: st.session_state.turn_data = [] # List of (r, c, char, pts)

# 3. HEADER
st.markdown(f"<h2 style='text-align:center;'>P1: {st.session_state.scores['P1']} | P2: {st.session_state.scores['P2']}</h2>", unsafe_allow_html=True)

# 4. THE BOARD (11x11 Grid)
for r in range(11):
    cols = st.columns(11)
    for c in range(11):
        val = st.session_state.board[r][c]
        if cols[c].button(val if val else " ", key=f"b_{r}_{c}"):
            if st.session_state.sel_idx is not None:
                char, pts = st.session_state.hand[st.session_state.sel_idx]
                st.session_state.board[r][c] = char
                st.session_state.turn_data.append((r, c, char, pts))
                st.session_state.hand[st.session_state.sel_idx] = random.choice(POOL)
                st.session_state.sel_idx = None
                st.rerun()

# 5. THE RACK
st.markdown("<div class='rack-container'>", unsafe_allow_html=True)
h_cols = st.columns(7)
for i, (char, pts) in enumerate(st.session_state.hand):
    if h_cols[i].button(f"{char}{SUB.get(str(pts), '')}", key=f"h_{i}"):
        st.session_state.sel_idx = i
        st.rerun()

# 6. REWIRE & VALIDATE (The Fix)
word_built = "".join([d[2] for d in st.session_state.turn_data])
st.write(f"Drafting: **{word_built}**")

if st.button("🔥 SUBMIT WORD", use_container_width=True, type="primary"):
    # Must be at least 2 letters and in dictionary
    if len(word_built) > 1 and word_built in WORDS_DB:
        total_pts = sum([d[3] for d in st.session_state.turn_data])
        st.session_state.scores[st.session_state.turn] += total_pts
        st.session_state.turn = "P2" if st.session_state.turn == "P1" else "P1"
        st.session_state.turn_data = [] 
        st.success(f"'{word_built}' Accepted! (+{total_pts})")
        st.rerun()
    else:
        # SELF-HEALING: Rejection logic
        for r, c, char, pts in st.session_state.turn_data:
            st.session_state.board[r][c] = ""
        st.session_state.turn_data = []
        st.error(f"'{word_built}' is not in dictionary or too short! Tiles returned.")
        st.rerun()
