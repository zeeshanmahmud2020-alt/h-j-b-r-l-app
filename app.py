import streamlit as st
import random
import requests
import unicodedata

# --- 1. SETTINGS & DICTIONARY ---
st.set_page_config(page_title="হ য ব র ল PRO", layout="centered")

@st.cache_resource
def load_dictionary():
    # Placeholder: In a real app, link to a large Bengali word list
    return {"বলো", "করো", "বড়", "খেলো", "বাড়ি", "মা", "বাবা", "আমি"}

WORDS_DB = load_dictionary()

def get_random_tile():
    consonants = ['ক', 'খ', 'গ', 'চ', 'জ', 'ত', 'দ', 'ন', 'প', 'ব', 'ম', 'র', 'ল', 'স', 'হ']
    vowels = ['', 'া', 'ি', 'ী', 'ু', 'ে', 'ো']
    # 70% chance of a pair (e.g., 'মা'), 30% single letter
    if random.random() > 0.3:
        return random.choice(consonants) + random.choice(vowels)
    return random.choice(consonants)

# --- 2. GAME STATE ---
if 'board' not in st.session_state:
    st.session_state.update({
        'board': [["" for _ in range(7)] for _ in range(7)],
        's1': 0, 's2': 0, 'turn': 1, 
        'sel_idx': None, 
        'turn_moves': [], # Stores {'r': r, 'c': c, 'char': char}
        'hand': [get_random_tile() for _ in range(7)]
    })

# --- 3. SCANNING LOGIC ---
def validate_move():
    moves = st.session_state.turn_moves
    if not moves: return False
    
    rows = [m['r'] for m in moves]
    cols = [m['c'] for m in moves]
    
    # Check if play is in a straight line
    is_horiz = len(set(rows)) == 1
    is_vert = len(set(cols)) == 1
    
    if not (is_horiz or is_vert):
        st.error("শব্দ অবশ্যই সোজা লাইনে হতে হবে (Horizontal or Vertical)!")
        return False

    # Find the full word by scanning the board
    r_start, c_start = moves[0]['r'], moves[0]['c']
    
    if is_horiz:
        r = r_start
        # Walk Left
        c_min = min(cols)
        while c_min > 0 and st.session_state.board[r][c_min - 1] != "":
            c_min -= 1
        # Read Right
        word = ""
        while c_min < 7 and st.session_state.board[r][c_min] != "":
            word += st.session_state.board[r][c_min]
            c_min += 1
    else:
        c = c_start
        # Walk Up
        r_min = min(rows)
        while r_min > 0 and st.session_state.board[r_min - 1][c] != "":
            r_min -= 1
        # Read Down
        word = ""
        while r_min < 7 and st.session_state.board[r_min][c] != "":
            word += st.session_state.board[r_min][c]
            r_min += 1

    clean_word = unicodedata.normalize('NFC', word)
    if clean_word in WORDS_DB:
        return clean_word
    return None

# --- 4. UI ---
st.markdown("<h1 style='text-align: center;'>হ য ব র ল PRO</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("📊 Scoreboard")
    st.metric("Player 1", st.session_state.s1)
    st.metric("Player 2", st.session_state.s2)
    st.write(f"👉 **Turn: Player {st.session_state.turn}**")
    if st.button("🔄 Reset Game"):
        st.session_state.clear()
        st.rerun()

# Grid Layout
for r in range(7):
    cols = st.columns(7)
    for c in range(7):
        tile_val = st.session_state.board[r][c]
        if cols[c].button(tile_val if tile_val else " ", key=f"b_{r}_{c}"):
            if st.session_state.sel_idx is not None:
                char = st.session_state.hand[st.session_state.sel_idx]
                st.session_state.board[r][c] = char
                st.session_state.turn_moves.append({'r': r, 'c': c, 'char': char})
                st.session_state.hand[st.session_state.sel_idx] = " " # Mark as used
                st.session_state.sel_idx = None
                st.rerun()

# Hand/Rack
st.write("---")
rack = st.columns(7)
for i in range(7):
    if rack[i].button(st.session_state.hand[i], key=f"h_{i}"):
        st.session_state.sel_idx = i

# Actions
col_sub, col_swp = st.columns(2)
if col_sub.button("🔥 SUBMIT", use_container_width=True, type="primary"):
    result_word = validate_move()
    if result_word:
        points = len(result_word)
        if st.session_state.turn == 1: st.session_state.s1 += points
        else: st.session_state.s2 += points
        # Refill hand and switch turn
        st.session_state.hand = [get_random_tile() if h == " " else h for h in st.session_state.hand]
        st.session_state.turn = 2 if st.session_state.turn == 1 else 1
        st.session_state.turn_moves = []
        st.toast(f"Success! '{result_word}' found.")
        st.rerun()
    else:
        # Self-Healing: Remove only the tiles placed this turn
        for m in st.session_state.turn_moves:
            st.session_state.board[m['r']][m['c']] = ""
        # Return tiles to hand
        st.session_state.hand = [get_random_tile() for _ in range(7)]
        st.session_state.turn_moves = []
        st.error("ভুল শব্দ অথবা লাইন সোজা নয়!")

if col_swp.button("🔄 SWAP TILES", use_container_width=True):
    st.session_state.hand = [get_random_tile() for _ in range(7)]
    st.rerun()
