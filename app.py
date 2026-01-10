import streamlit as st
import random
import requests
import unicodedata

# 1. SETTINGS & DICTIONARY (Executive Grade)
st.set_page_config(page_title="হ য ব র ল PRO", layout="centered")

@st.cache_resource
def load_dict():
    url = "https://raw.githubusercontent.com/tahmid02016/bangla-wordlist/master/words.txt"
    try:
        r = requests.get(url, timeout=5)
        # Normalize to NFC to ensure "ন" + "া" matches the dictionary entry "না"
        return set(unicodedata.normalize('NFC', w.strip()) for w in r.text.split())
    except:
        return {"কাকা", "বাবা", "মামা", "বাঘ"}

WORDS_DB = load_dict()

# GLOBAL POOL - Defined at top-level to prevent NameError
GLOBAL_POOL = [
    ('না',1), ('বা',1), ('কা',1), ('কি',2), ('মা',1), ('রা',2), 
    ('নি',2), ('পা',1), ('কু',2), ('মি',2), ('গা',2), ('রে',2)
]

# 2. STYLED INTERFACE
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

# 3. INITIALIZATION
if 's1' not in st.session_state: 
    st.session_state.update({'s1':0, 's2':0, 'turn':1, 'sel_idx':None, 'turn_moves':[]})
if 'board' not in st.session_state: 
    st.session_state.board = [["" for _ in range(11)] for _ in range(11)]
if 'hand' not in st.session_state:
    st.session_state.hand = random.sample(GLOBAL_POOL, 7)

# 4. SIDEBAR (The Auditor)
with st.sidebar:
    st.header("📊 Executive Audit")
    st.metric("Player 1", st.session_state.s1)
    st.metric("Player 2", st.session_state.s2)
    st.write(f"👉 Active: **Player {st.session_state.turn}**")
    if st.button("🔄 System Reset"):
        st.session_state.clear()
        st.rerun()

st.markdown("<h1 style='text-align:center; color:#f1c40f;'>হ য ব র ল</h1>", unsafe_allow_html=True)

# 5. THE BOARD
for r in range(11):
    cols = st.columns(11)
    for c in range(11):
        val = st.session_state.board[r][c]
        if cols[c].button(val if val else " ", key=f"b_{r}_{c}"):
            if st.session_state.sel_idx is not None:
                char, pts = st.session_state.hand[st.session_state.sel_idx]
                st.session_state.board[r][c] = char
                # Memory of coordinates for the current turn
                st.session_state.turn_moves.append({'r':r, 'c':c, 'char':char, 'pts':pts})
                st.session_state.hand[st.session_state.sel_idx] = random.choice(GLOBAL_POOL)
                st.session_state.sel_idx = None
                st.rerun()

# 6. THE RACK
st.markdown("<div class='rack-container'>", unsafe_allow_html=True)
h_cols = st.columns(7)
SUBS = {"1":"₁", "2":"₂", "3":"₃"}
for i, (char, pts) in enumerate(st.session_state.hand):
    if h_cols[i].button(f"{char}{SUBS.get(str(pts),'')}", key=f"h_{i}"):
        st.session_state.sel_idx = i
        st.rerun()

# 7. THE FINAL AUDIT (Validation Logic)
if st.button("🔥 SUBMIT WORD", use_container_width=True, type="primary"):
    moves = st.session_state.turn_moves
    if not moves:
        st.warning("Place tiles first.")
    else:
        # Sort and extract the word attempted
        moves.sort(key=lambda x: (x['r'], x['c']))
        word_attempt = "".join([m['char'] for m in moves])
        normalized_word = unicodedata.normalize('NFC', word_attempt)

        # CHECK 1: Connectivity (Must be in a straight line)
        rows = [m['r'] for m in moves]
        cols = [m['c'] for m in moves]
        is_linear = (len(set(rows)) == 1) or (len(set(cols)) == 1)
        
        # CHECK 2: Dictionary Match
        if is_linear and normalized_word in WORDS_DB:
            pts_sum = sum([m['pts'] for m in moves])
            if st.session_state.turn == 1: st.session_state.s1 += pts_sum
            else: st.session_state.s2 += pts_sum
            
            st.session_state.turn = 2 if st.session_state.turn == 1 else 1
            st.session_state.turn_moves = []
            st.success(f"Verified: {normalized_word} (+{pts_sum})")
            st.rerun()
        else:
            # REJECTION: Clear the bad tiles from the board
            for m in moves:
                st.session_state.board[m['r']][m['c']] = ""
            st.session_state.turn_moves = []
            st.error(f"Illegal move: '{normalized_word}' failed validation.")
            st.rerun()
