import streamlit as st
import random
import requests
import unicodedata

st.set_page_config(page_title="হ য ব র ল PRO", layout="centered")

@st.cache_resource
def load_dict():
    url = "https://raw.githubusercontent.com/tahmid02016/bangla-wordlist/master/words.txt"
    try:
        r = requests.get(url, timeout=5)
        # NORMALIZE: Ensures dictionary characters match user input exactly
        return set(unicodedata.normalize('NFC', w.strip()) for w in r.text.split())
    except:
        return {"কাকা", "বাবা", "মামা"}

WORDS_DB = load_dict()

# CSS for a locked, professional grid
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

# ROBUST INITIALIZATION
if 's1' not in st.session_state: 
    st.session_state.update({'s1':0, 's2':0, 'turn':1, 'sel_idx':None, 'turn_moves':[]})
if 'board' not in st.session_state: 
    st.session_state.board = [["" for _ in range(11)] for _ in range(11)]
if 'hand' not in st.session_state:
    POOL = [('না',1), ('বা',1), ('কা',1), ('কি',2), ('মা',1), ('রা',2), ('নি',2), ('পু',3)]
    st.session_state.hand = random.sample(POOL, 7)

# SIDEBAR SCOREBOARD
with st.sidebar:
    st.header("📊 Executive Audit")
    st.metric("Player 1", st.session_state.s1)
    st.metric("Player 2", st.session_state.s2)
    st.write(f"👉 **Player {st.session_state.turn}'s Turn**")
    if st.button("🔄 System Reset"):
        st.session_state.clear()
        st.rerun()

st.markdown("<h1 style='text-align:center; color:#f1c40f;'>হ য ব র ল</h1>", unsafe_allow_html=True)

# BOARD RENDER
for r in range(11):
    cols = st.columns(11)
    for c in range(11):
        val = st.session_state.board[r][c]
        if cols[c].button(val if val else " ", key=f"b_{r}_{c}"):
            if st.session_state.sel_idx is not None:
                char, pts = st.session_state.hand[st.session_state.sel_idx]
                st.session_state.board[r][c] = char
                st.session_state.turn_moves.append({'r':r, 'c':c, 'char':char, 'pts':pts})
                st.session_state.hand[st.session_state.sel_idx] = random.choice(POOL)
                st.session_state.sel_idx = None
                st.rerun()

# RACK RENDER
st.markdown("<div class='rack-container'>", unsafe_allow_html=True)
h_cols = st.columns(7)
SUBS = {"1":"₁", "2":"₂", "3":"₃"}
for i, (char, pts) in enumerate(st.session_state.hand):
    if h_cols[i].button(f"{char}{SUBS.get(str(pts),'')}", key=f"h_{i}"):
        st.session_state.sel_idx = i
        st.rerun()

# THE AUDIT (The Fix)
word_to_audit = "".join([m['char'] for m in st.session_state.turn_moves])
# Force normalize the user input to match the dictionary
normalized_word = unicodedata.normalize('NFC', word_to_audit)
st.write(f"Audit Target: **{normalized_word if normalized_word else '...'}**")

if st.button("🔥 SUBMIT WORD", use_container_width=True, type="primary"):
    # STRICT DICTIONARY GATE
    if normalized_word in WORDS_DB:
        pts = sum([m['pts'] for m in st.session_state.turn_moves])
        if st.session_state.turn == 1: st.session_state.s1 += pts
        else: st.session_state.s2 += pts
        st.session_state.turn = 2 if st.session_state.turn == 1 else 1
        st.session_state.turn_moves = []
        st.success(f"Legal Move! +{pts}")
        st.rerun()
    else:
        # AUTOMATIC WIPE: Rejects "naba" or any other illegal string
        for m in st.session_state.turn_moves:
            st.session_state.board[m['r']][m['c']] = ""
        st.session_state.turn_moves = []
        st.error(f"Illegal Word: '{normalized_word}' rejected.")
        st.rerun()
