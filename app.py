import streamlit as st
import random
import unicodedata

# --- 1. SETTINGS & LOCAL DICTIONARY ---
st.set_page_config(page_title="হ য ব র ল PRO", layout="centered")

@st.cache_resource
def load_dictionary():
    # ADD YOUR WORDS HERE - This is your built-in Dictionary
    return {
        "জুতা", "কচি", "বলো", "করো", "বড়", "মা", "বাবা", 
        "বাড়ি", "গান", "খাওয়া", "খেলো", "আমি", "তুমি", "গাখি"
    }

WORDS_DB = load_dictionary()

def get_random_tile():
    consonants = ['ক', 'খ', 'গ', 'চ', 'জ', 'ত', 'দ', 'ন', 'প', 'ব', 'ম', 'র', 'ল', 'স', 'হ']
    vowels = ['', 'া', 'ি', 'ী', 'ু', 'ে', 'ো']
    # Creates one "meme" tile unit
    return random.choice(consonants) + random.choice(vowels)

# --- 2. SESSION STATE ---
if 'board' not in st.session_state:
    st.session_state.update({
        'board': [["" for _ in range(5)] for _ in range(5)], # 5x5 Grid
        's1': 0, 's2': 0, 'turn': 1, 
        'sel_idx': None, 'turn_moves': [], 
        'hand': [get_random_tile() for _ in range(7)] # 7 Tiles
    })

# --- 3. UI ---
st.markdown("<h1 style='text-align: center;'>হ য ব র ল PRO</h1>", unsafe_allow_html=True)

# 5x5 Grid Logic
for r in range(5):
    cols = st.columns(5)
    for c in range(5):
        val = st.session_state.board[r][c]
        if cols[c].button(val if val else " ", key=f"b_{r}_{c}", use_container_width=True):
            if st.session_state.sel_idx is not None:
                char = st.session_state.hand[st.session_state.sel_idx]
                st.session_state.board[r][c] = char
                st.session_state.turn_moves.append({'r': r, 'c': c, 'char': char})
                st.session_state.hand[st.session_state.sel_idx] = " "
                st.session_state.sel_idx = None
                st.rerun()

# Rack Logic
st.write("### Your Tiles")
rack = st.columns(7)
for i in range(7):
    label = st.session_state.hand[i]
    if rack[i].button(label, key=f"h_{i}", disabled=(label == " ")):
        st.session_state.sel_idx = i

# --- 4. SUBMIT & SELF-HEALING ---
st.write("---")
col_a, col_b = st.columns(2)

if col_a.button("🔥 SUBMIT WORD", use_container_width=True, type="primary"):
    # Joins tiles and cleans Unicode
    played_word = "".join([m['char'] for m in st.session_state.turn_moves]).strip()
    clean_word = unicodedata.normalize('NFC', played_word)
    
    if clean_word in WORDS_DB:
        points = len(clean_word)
        if st.session_state.turn == 1: st.session_state.s1 += points
        else: st.session_state.s2 += points
        st.session_state.hand = [get_random_tile() if h == " " else h for h in st.session_state.hand]
        st.session_state.turn = 2 if st.session_state.turn == 1 else 1
        st.session_state.turn_moves = []
        st.toast(f"Accepted: {clean_word}")
        st.rerun()
    else:
        # SELF-HEALING: Clears board on failure
        for m in st.session_state.turn_moves:
            st.session_state.board[m['r']][m['c']] = ""
        st.session_state.hand = [get_random_tile() if h == " " else h for h in st.session_state.hand]
        st.session_state.turn_moves = []
        st.error(f"Rejected: '{clean_word}' dictionary-তে নেই।")

if col_b.button("🔄 SWAP ALL", use_container_width=True):
    st.session_state.hand = [get_random_tile() for _ in range(7)]
    st.rerun()
