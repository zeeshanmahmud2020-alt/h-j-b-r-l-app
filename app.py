import streamlit as st
import random
import requests

st.set_page_config(page_title="হ য ব র ল PRO", layout="centered")

@st.cache_resource
def load_dict():
    url = "https://raw.githubusercontent.com/tahmid02016/bangla-wordlist/master/words.txt"
    try:
        r = requests.get(url, timeout=5)
        # Using a set for O(1) efficiency in searching
        return set(word.strip() for word in r.text.split())
    except:
        return {"কাকা", "বাবা", "মামা", "বাঘ", "নাম"}

WORDS_DB = load_dict()

# CSS to lock the board and clean the puke layout
st.markdown("""
    <style>
    div.stButton > button[key^="b_"] {
        background-color: #1e272e !important; color: #ecf0f1 !important;
        width: 44px !important; height: 44px !important;
        border: 1px solid #3d4e5f !important; font-size: 16px !important;
    }
    .rack-container {
        display: flex; justify-content: center; gap: 4px;
        background: linear-gradient(#8b5a2b, #5d3a1a); padding: 12px;
        border-radius: 4px; margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. INITIALIZATION (Fixing the population error)
# Ensure POOL is large enough to sample 7 tiles
POOL = [('কা',1), ('কি',2), ('কু',2), ('কে',3), ('পা',1), ('মা',1), ('বা',1), ('রা',2), ('না',1), ('নি',2), ('মা',1), ('বি',2)]

if 'board' not in st.session_state: st.session_state.board = [["" for _ in range(11)] for _ in range(11)]
if 's1' not in st.session_state: st.session_state.s1 = 0
if 's2' not in st.session_state: st.session_state.s2 = 0
if 'turn' not in st.session_state: st.session_state.turn = 1
if 'hand' not in st.session_state: st.session_state.hand = random.sample(POOL, 7)
if 'sel_idx' not in st.session_state: st.session_state.sel_idx = None
if 'turn_moves' not in st.session_state: st.session_state.turn_moves = []

# 2. SIDEBAR FOR EXECUTIVE OVERSIGHT
with st.sidebar:
    st.header("📊 Scoreboard")
    st.metric("Player 1", st.session_state.s1)
    st.metric("Player 2", st.session_state.s2)
    st.write(f"👉 **Player {st.session_state.turn}'s Turn**")
    if st.button("🔄 System Reset"):
        st.session_state.clear()
        st.rerun()

st.markdown("<h1 style='text-align:center; color:#f1c40f;'>হ য ব র ল</h1>", unsafe_allow_html=True)

# 3. THE BOARD (11x11 Grid)
for r in range(11):
    cols = st.columns(11)
    for c in range(11):
        val = st.session_state.board[r][c]
        if cols[c].button(val if val else " ", key=f"b_{r}_{c}"):
            if st.session_state.sel_idx is not None:
                char, pts = st.session_state.hand[st.session_state.sel_idx]
                st.session_state.board[r][c] = char
                # ADD TO BUFFER ONLY - NO SCORING HERE
                st.session_state.turn_moves.append({'pos':(r,c), 'char':char, 'pts':pts})
                st.session_state.hand[st.session_state.sel_idx] = random.choice(POOL)
                st.session_state.sel_idx = None
                st.rerun()

# 4. THE RACK (Integrated Subscripts)
st.markdown("<div class='rack-container'>", unsafe_allow_html=True)
h_cols = st.columns(7)
SUBS = {"1":"₁", "2":"₂", "3":"₃"}
for i, (char, pts) in enumerate(st.session_state.hand):
    if h_cols[i].button(f"{char}{SUBS.get(str(pts),'')}", key=f"h_{i}"):
        st.session_state.sel_idx = i
        st.rerun()

# 5. THE SCAN & COMPARE DICTIONARY TEST
# This reads the letters exactly in the order they were placed
current_word = "".join([m['char'] for m in st.session_state.turn_moves])
st.write(f"Drafting: **{current_word if current_word else '...'}**")

if st.button("🔥 SUBMIT WORD", use_container_width=True, type="primary"):
    # The dictionary comparison happens HERE and only HERE
    if current_word in WORDS_DB and len(current_word) > 1:
        points = sum([m['pts'] for m in st.session_state.turn_moves])
        if st.session_state.turn == 1: st.session_state.s1 += points
        else: st.session_state.s2 += points
        
        # Turn Management
        st.session_state.turn = 2 if st.session_state.turn == 1 else 1
        st.session_state.turn_moves = []
        st.success(f"Accepted: {current_word}! +{points}")
        st.rerun()
    else:
        # REJECTED: Rewire the board by deleting the bad move
        for m in st.session_state.turn_moves:
            r, c = m['pos']
            st.session_state.board[r][c] = ""
        st.session_state.turn_moves = []
        st.error(f"'{current_word}' failed audit. Move reverted.")
        st.rerun()
