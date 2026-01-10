import streamlit as st
import random
import unicodedata

# --- 1. SETTINGS & DICTIONARY ---
st.set_page_config(page_title="হ য ব র ল PRO")
st.markdown("<h1 style='text-align: center;'>হ য ব র ল</h1>", unsafe_allow_html=True)

# Logic to create "Memes" (Consonant + Vowel) as one tile
def get_random_tile():
    consonants = ['ক', 'খ', 'গ', 'চ', 'জ', 'ত', 'দ', 'ন', 'প', 'ব', 'ম', 'র', 'ল', 'স', 'হ']
    vowels = ['', 'া', 'ি', 'ী', 'ু', 'ে', 'ো'] # Empty string for just the consonant
    # Combines one from each to make a single tile like 'কা' or 'লি'
    return random.choice(consonants) + random.choice(vowels)

if 'board' not in st.session_state:
    st.session_state.update({
        'board': [["" for _ in range(5)] for _ in range(5)], # 5x5 Board
        's1': 0, 's2': 0, 'turn': 1,
        'hand': [get_random_tile() for _ in range(7)], # 7 Tiles
        'sel_idx': None, 'turn_moves': []
    })

# --- 2. BOARD & RACK UI ---
# Display Scores
c1, c2 = st.columns(2)
c1.metric("Player 1", st.session_state.s1)
c2.metric("Player 2", st.session_state.s2)

# 5x5 Grid
for r in range(5):
    cols = st.columns(5)
    for c in range(5):
        tile = st.session_state.board[r][c]
        if cols[c].button(tile if tile else " ", key=f"{r}_{c}", use_container_width=True):
            if st.session_state.sel_idx is not None:
                char = st.session_state.hand[st.session_state.sel_idx]
                st.session_state.board[r][c] = char
                st.session_state.turn_moves.append({'r': r, 'c': c, 'char': char})
                st.session_state.hand[st.session_state.sel_idx] = "Used"
                st.session_state.sel_idx = None
                st.rerun()

# 7-Tile Rack
st.write("### Your Tiles")
rack_cols = st.columns(7)
for i in range(7):
    label = st.session_state.hand[i]
    if rack_cols[i].button(label, key=f"h_{i}", disabled=(label=="Used")):
        st.session_state.sel_idx = i

# --- 3. SUBMIT & SWAP ---
col_a, col_b = st.columns(2)

if col_a.button("🔥 SUBMIT WORD", use_container_width=True, type="primary"):
    # Simple check: extract current turn tiles
    played_word = "".join([m['char'] for m in st.session_state.turn_moves])
    
    # Validation (Placeholder: Add your word list here)
    if len(played_word) > 1:
        points = len(played_word)
        if st.session_state.turn == 1: st.session_state.s1 += points
        else: st.session_state.s2 += points
        # Reset for next turn
        st.session_state.hand = [get_random_tile() if t=="Used" else t for t in st.session_state.hand]
        st.session_state.turn = 2 if st.session_state.turn == 1 else 1
        st.session_state.turn_moves = []
        st.success(f"Accepted: {played_word}")
        st.rerun()
    else:
        # Self-Healing: Remove only the invalid tiles from this turn
        for m in st.session_state.turn_moves:
            st.session_state.board[m['r']][m['c']] = ""
        st.session_state.hand = [get_random_tile() if t=="Used" else t for t in st.session_state.hand]
        st.session_state.turn_moves = []
        st.error("Invalid! Tiles cleared.")

if col_b.button("🔄 SWAP ALL", use_container_width=True):
    st.session_state.hand = [get_random_tile() for _ in range(7)]
    st.rerun()
