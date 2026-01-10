import streamlit as st
import random
import requests

st.set_page_config(page_title="হ য ব র ল PRO", layout="centered")

@st.cache_resource
def load_dict():
    url = "https://raw.githubusercontent.com/tahmid02016/bangla-wordlist/master/words.txt"
    try:
        r = requests.get(url, timeout=5)
        # STRICTOR CLEANING: removes every possible hidden space/newline
        return set(w.strip() for w in r.text.split() if len(w.strip()) > 1)
    except:
        return {"কাকা", "বাবা", "মামা"}

WORDS_DB = load_dict()

# 1. INITIALIZATION & UI
POOL = [('না',1), ('বা',1), ('কা',1), ('কি',2), ('মা',1), ('রা',2), ('নি',2)]
if 's1' not in st.session_state: st.session_state.update({'s1':0, 's2':0, 'turn':1, 'sel_idx':None, 'turn_moves':[]})
if 'board' not in st.session_state: st.session_state.board = [["" for _ in range(11)] for _ in range(11)]
if 'hand' not in st.session_state: st.session_state.hand = random.sample(POOL, 7)

st.markdown("<h1 style='text-align:center; color:#f1c40f;'>হ য ব র ল</h1>", unsafe_allow_html=True)

# 2. BOARD GRID
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

# 3. SUBMIT WITH HARD DICTIONARY AUDIT
word_attempt = "".join([m['char'] for m in st.session_state.turn_moves]).strip()
st.write(f"Audit Target: **{word_attempt}**")

if st.button("🔥 SUBMIT WORD", use_container_width=True, type="primary"):
    # THE ONLY CHECK THAT MATTERS: Is the word EXACTLY in the dictionary?
    if word_attempt in WORDS_DB:
        pts = sum([m['pts'] for m in st.session_state.turn_moves])
        if st.session_state.turn == 1: st.session_state.s1 += pts
        else: st.session_state.s2 += pts
        st.session_state.turn = 2 if st.session_state.turn == 1 else 1
        st.session_state.turn_moves = []
        st.success(f"Legal Word Approved: {word_attempt}")
        st.rerun()
    else:
        # REJECTED: Any illegal word results in tile deletion and 0 points
        for m in st.session_state.turn_moves:
            st.session_state.board[m['r']][m['c']] = ""
        st.session_state.turn_moves = []
        st.error(f"ILLEGAL WORD: '{word_attempt}' not found in dictionary. Tiles wiped.")
        st.rerun()
