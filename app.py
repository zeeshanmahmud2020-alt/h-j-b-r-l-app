import streamlit as st
import random
import requests

st.set_page_config(page_title="হ য ব র ল PRO", layout="centered")

@st.cache_resource
def load_dict():
    # Fetching the official vetted Bengali word list
    url = "https://raw.githubusercontent.com/tahmid02016/bangla-wordlist/master/words.txt"
    try:
        r = requests.get(url, timeout=5)
        # We strip every word to ensure no white-space bypasses the check
        return set(w.strip() for w in r.text.split())
    except:
        return {"কাকা", "বাবা", "মামা", "বাঘ", "নাম"}

WORDS_DB = load_dict()

# 1. LOCK THE GRID: No more puke layout
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

# 2. STATE INITIALIZATION (Score starts and stays at 0 until audit)
POOL = [('কা',1), ('কি',2), ('কু',2), ('পা',1), ('মা',1), ('বা',1), ('রা',2), ('না',1), ('নি',2)]

if 'board' not in st.session_state: st.session_state.board = [["" for _ in range(11)] for _ in range(11)]
if 's1' not in st.session_state: st.session_state.s1 = 0
if 's2' not in st.session_state: st.session_state.s2 = 0
if 'turn' not in st.session_state: st.session_state.turn = 1
if 'hand' not in st.session_state: st.session_state.hand = random.sample(POOL, 7)
if 'sel_idx' not in st.session_state: st.session_state.sel_idx = None
if 'turn_moves' not in st.session_state: st.session_state.turn_moves = []

# 3. SIDEBAR AUDIT
with st.sidebar:
    st.header("📊 Executive Audit")
    st.metric("Player 1 Score", st.session_state.s1)
    st.metric("Player 2 Score", st.session_state.s2)
    st.write(f"👉 Current: **Player {st.session_state.turn}**")
    if st.button("🔄 Full System Reset"):
        st.session_state.clear()
        st.rerun()

st.markdown("<h1 style='text-align:center; color:#f1c40f;'>হ য ব র ল</h1>", unsafe_allow_html=True)

# 4. THE GRID
for r in range(11):
    cols = st.columns(11)
    for c in range(11):
        val = st.session_state.board[r][c]
        if cols[c].button(val if val else " ", key=f"b_{r}_{c}"):
            if st.session_state.sel_idx is not None:
                char, pts = st.session_state.hand[st.session_state.sel_idx]
                st.session_state.board[r][c] = char
                # Moves go to a temporary buffer (NO SCORE ADDED)
                st.session_state.turn_moves.append({'pos':(r,c), 'char':char, 'pts':pts})
                st.session_state.hand[st.session_state.sel_idx] = random.choice(POOL)
                st.session_state.sel_idx = None
                st.rerun()

# THE RACK (Clean Unicode Subscripts)
st.markdown("<div class='rack-container'>", unsafe_allow_html=True)
h_cols = st.columns(7)
SUBS = {"1":"₁", "2":"₂", "3":"₃"}
for i, (char, pts) in enumerate(st.session_state.hand):
    if h_cols[i].button(f"{char}{SUBS.get(str(pts),'')}", key=f"h_{i}"):
        st.session_state.sel_idx = i
        st.rerun()

# 5. THE SCANNER: Reads what you actually placed
word_to_check = "".join([m['char'] for m in st.session_state.turn_moves])
st.write(f"Board Draft: **{word_to_check if word_to_check else '...'}**")

if st.button("🔥 SUBMIT WORD", use_container_width=True, type="primary"):
    # THE GATEKEEPER: Check against dictionary set
    if word_to_check in WORDS_DB and len(word_to_check) > 1:
        # SUCCESS: Only now do we touch the score variables
        points = sum([m['pts'] for m in st.session_state.turn_moves])
        if st.session_state.turn == 1: st.session_state.s1 += points
        else: st.session_state.s2 += points
        
        st.session_state.turn = 2 if st.session_state.turn == 1 else 1
        st.session_state.turn_moves = []
        st.success(f"Transaction Verified: +{points}")
        st.rerun()
    else:
        # FAILURE: Rejection logic wipes the board
        for m in st.session_state.turn_moves:
            r, c = m['pos']
            st.session_state.board[r][c] = ""
        st.session_state.turn_moves = []
        st.error(f"'{word_to_check}' failed validation. Score withheld.")
        st.rerun()
