import streamlit as st
import random
import requests
import unicodedata

# --- 1. SETTINGS & DICTIONARY ---
st.set_page_config(page_title="হ য ব র ল PRO", layout="centered")

# Update this URL to your actual Bangla word list file
DICT_URL = "https://raw.githubusercontent.com/zeeshanmahmud2020-alt/h-j-b-r-l-app/main/requirements.txt"

@st.cache_resource
def load_dictionary():
    try:
        r = requests.get(DICT_URL, timeout=10)
        # Normalizes and creates a set of valid words
        return set(unicodedata.normalize('NFC', w.strip()) for w in r.text.split())
    except:
        # Fallback list if the URL fails
        return {"বলো", "করো", "বড়", "খেলো", "বাড়ি", "মা", "বাবা", "আমি"}

WORDS_DB = load_dictionary()

def get_random_tile():
    consonants = ['ক', 'খ', 'গ', 'চ', 'জ', 'ত', 'দ', 'ন', 'প', 'ব', 'ম', 'র', 'ল', 'স', 'হ']
    vowels = ['', 'া', 'ি', 'ী', 'ু', 'ে', 'ো']
    # Combines them into a single "meme" tile
    return random.choice(consonants) + random.choice(vowels)

# --- 2. GAME STATE ---
if 'board' not in st.session_state:
    st.session_state.update({
        'board': [["" for _ in range(5)] for _ in range(5)],
        's1': 0, 's2': 0, 'turn': 1, 
        'sel_idx': None, 
        'turn_moves': [], 
        'hand': [get_random_tile() for _ in range(7)]
    })

# --- 3. UI HEADER ---
st.markdown("<h1 style='text-align: center;'>হ য ব র ল PRO</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("📊 Scoreboard")
    st.metric("Player 1", st.session_state.s1)
    st.metric("Player 2", st.session_state.s2)
    st.write(f"👉 **Active: Player {st.session_state.turn}**")
    if st.button("🔄 Reset Game"):
        st.session_state.clear()
        st.rerun()

# --- 4. THE 5x5 GRID ---
for r in range(5):
    cols = st.columns(5)
    for c in range(5):
        tile_val = st.session_state.board[r][c]
        if cols[c].button(tile_val if tile_val else " ", key=f"b_{r}_{c}", use_container_width=True):
            if st.session_state.sel_idx is not None:
                char = st.session_state.hand[st.session_state.sel_idx]
                st.session_state.board[r][c] = char
                st.session_state.turn_moves.append({'r': r, 'c': c, 'char': char})
                st.session_state.hand[st.session_state.sel_idx] = " " 
                st.session_state.sel_idx = None
                st.rerun()

# --- 5. TILE RACK ---
st.write("### Your Tiles")
rack = st.columns(7)
for i in range(7):
    tile_label = st.session_state.hand[i]
    if rack[i].button(tile_label, key=f"h_{i}", disabled=(tile_label == " ")):
        st.session_state.sel_idx = i

# --- 6. ACTIONS (SUBMIT & SWAP) ---
st.write("---")
col_a, col_b = st.columns(2) # Defining columns BEFORE buttons

if col_a.button("🔥 SUBMIT WORD", use_container_width=True, type="primary"):
    played_word = "".join([m['char'] for m in st.session_state.turn_moves])
    clean_word = unicodedata.normalize('NFC', played_word)
    
    if clean_word in WORDS_DB:
        points = len(clean_word)
        if st.session_state.turn == 1: st.session_state.s1 += points
        else: st.session_state.s2 += points
        # Success: Refill hand and toggle turn
        st.session_state.hand = [get_random_tile() if h == " " else h for h in st.session_state.hand]
        st.session_state.turn = 2 if st.session_state.turn == 1 else 1
        st.session_state.turn_moves = []
        st.toast(f"Accepted: {clean_word}")
        st.rerun()
    else:
        # FAILED: Self-healing board (removes only recent moves)
        for m in st.session_state.turn_moves:
            st.session_state.board[m['r']][m['c']] = ""
        # Return tiles to hand
        st.session_state.hand = [get_random_tile() if h == " " else h for h in st.session_state.hand]
        st.session_state.turn_moves = []
        st.error(f"Rejected: '{clean_word}' is not a valid word.")

if col_b.button("🔄 SWAP ALL", use_container_width=True):
    st.session_state.hand = [get_random_tile() for _ in range(7)]
    st.rerun()
