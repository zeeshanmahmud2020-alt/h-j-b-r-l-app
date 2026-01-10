import streamlit as st
import random
import requests
import unicodedata

# --- 1. SETTINGS & DICTIONARY ---
st.set_page_config(page_title="হ য ব র ল PRO", layout="centered")
RAW_DICT_URL = "https://raw.githubusercontent.com/zeeshanmahmud2020-alt/h-j-b-r-l-app/main/requirements.txt"

@st.cache_resource
def load_dictionary():
    try:
        r = requests.get(RAW_DICT_URL, timeout=10)
        return set(unicodedata.normalize('NFC', w.strip()) for w in r.text.split())
    except:
        return set()

WORDS_DB = load_dictionary()

# --- 2. GAME STATE INITIALIZATION ---
if 'board' not in st.session_state:
    st.session_state.update({
        'board': [["" for _ in range(11)] for _ in range(11)],
        's1': 0, 's2': 0, 'turn': 1, 'sel_idx': None, 'turn_moves': []
    })
    # Basic pool for testing
    pool = ['অ', 'আ', 'ই', 'উ', 'ক', 'খ', 'গ', 'ঘ', 'চ', 'ছ', 'জ', 'ট', 'ত', 'দ', 'ন', 'প', 'ব', 'ম', 'য', 'র', 'ল', 'শ', 'স', 'হ']
    st.session_state.hand = [random.choice(pool) for _ in range(7)]

# --- 3. SIDEBAR (The Executive Audit) ---
with st.sidebar:
    st.header("📊 Executive Audit")
    st.metric("Player 1", st.session_state.s1)
    st.metric("Player 2", st.session_state.s2)
    st.write(f"👉 **Active: Player {st.session_state.turn}**")
    if st.button("🔄 System Reset"):
        st.session_state.clear()
        st.rerun()

# --- 4. THE GAME GRID ---
for r in range(11):
    cols = st.columns(11)
    for c in range(11):
        tile_val = st.session_state.board[r][c]
        if cols[c].button(tile_val if tile_val else " ", key=f"b_{r}_{c}"):
            if st.session_state.sel_idx is not None:
                char = st.session_state.hand[st.session_state.sel_idx]
                st.session_state.board[r][c] = char
                st.session_state.turn_moves.append({'r': r, 'c': c, 'char': char})
                # Refill hand and reset selection
                st.session_state.hand[st.session_state.sel_idx] = random.choice(['ক','ন','ব','র','ল'])
                st.session_state.sel_idx = None
                st.rerun()

# --- 5. TILE RACK ---
st.write("---")
rack_cols = st.columns(7)
for i in range(7):
    if rack_cols[i].button(st.session_state.hand[i], key=f"hand_{i}"):
        st.session_state.sel_idx = i

# --- 6. THE SUBMIT GATE ---
if st.button("🔥 SUBMIT WORD", use_container_width=True, type="primary"):
    played_word = "".join([m['char'] for m in st.session_state.turn_moves])
    clean_word = unicodedata.normalize('NFC', played_word.strip())
    
    if clean_word in WORDS_DB:
        points = len(clean_word)
        if st.session_state.turn == 1: st.session_state.s1 += points
        else: st.session_state.s2 += points
        st.session_state.turn = 2 if st.session_state.turn == 1 else 1
        st.session_state.turn_moves = []
        st.success(f"PASSED! '{clean_word}' found.")
        st.rerun()
    else:
        # FAILED: Remove invalid tiles from board
        for move in st.session_state.turn_moves:
            st.session_state.board[move['r']][move['c']] = ""
        st.session_state.turn_moves = []
        st.error(f"REJECTED! '{clean_word}' is not in your list.")
