import streamlit as st
import random
import unicodedata

# --- 1. SETTINGS & FULL DICTIONARY ---
st.set_page_config(page_title="হ য ব র ল PRO", layout="wide")

@st.cache_resource
def load_full_dictionary():
    # To avoid the 'requirements.txt' issue, we define a robust set here.
    # You can paste thousands of words into this set.
    return {"জুতা", "কচি", "বলো", "করো", "বড়", "মা", "বাবা", "বাড়ি", "গান", "গাখি", "খেলো", "তুমি", "আমি"}

WORDS_DB = load_full_dictionary()

def get_meme_tile():
    consonants = ['ক', 'খ', 'গ', 'চ', 'জ', 'ত', 'দ', 'ন', 'প', 'ব', 'ম', 'র', 'ল', 'স', 'হ']
    # These are the subscripts/vowel marks you requested
    vowels = ['', 'া', 'ি', 'ী', 'ু', 'ে', 'ো'] 
    return random.choice(consonants) + random.choice(vowels)

# --- 2. SESSION STATE (Score & Board) ---
if 'board' not in st.session_state:
    st.session_state.update({
        'board': [["" for _ in range(5)] for _ in range(5)],
        'p1_score': 0, 
        'p2_score': 0, 
        'turn': 1, 
        'hand': [get_meme_tile() for _ in range(7)],
        'turn_moves': [],
        'selected_hand_idx': None
    })

# --- 3. UI LAYOUT ---
st.title("হ য ব র ল PRO")

# Sidebar Score Tracking
with st.sidebar:
    st.header("🏆 Live Scores")
    st.subheader(f"Player 1: {st.session_state.p1_score}")
    st.subheader(f"Player 2: {st.session_state.p2_score}")
    st.divider()
    st.info(f"Current Turn: Player {st.session_state.turn}")
    if st.button("Reset Game"):
        st.session_state.clear()
        st.rerun()

# 5x5 Board
for r in range(5):
    cols = st.columns(5)
    for c in range(5):
        tile_text = st.session_state.board[r][c]
        if cols[c].button(tile_text if tile_text else " ", key=f"cell_{r}_{c}", use_container_width=True):
            if st.session_state.selected_hand_idx is not None:
                # Place tile on board
                val = st.session_state.hand[st.session_state.selected_hand_idx]
                st.session_state.board[r][c] = val
                st.session_state.turn_moves.append({'r': r, 'c': c, 'val': val})
                st.session_state.hand[st.session_state.selected_hand_idx] = " " # Mark used
                st.session_state.selected_hand_idx = None
                st.rerun()

# Player Hand (The Rack)
st.write("### Your Tiles (Consonant + Subscript)")
hand_cols = st.columns(7)
for i in range(7):
    tile = st.session_state.hand[i]
    if hand_cols[i].button(tile, key=f"hand_{i}", disabled=(tile == " ")):
        st.session_state.selected_hand_idx = i

# --- 4. LOGIC: SCORE INCREMENT & SELF-HEAL ---
st.divider()
btn_col1, btn_col2 = st.columns(2)

if btn_col1.button("🔥 SUBMIT MOVE", use_container_width=True, type="primary"):
    # Build the word from the turn's moves
    word_attempt = "".join([m['val'] for m in st.session_state.turn_moves]).strip()
    clean_word = unicodedata.normalize('NFC', word_attempt)
    
    if clean_word in WORDS_DB:
        # 1. CALCULATE SCORE (Points = letters * 10)
        points = len(clean_word) * 10
        if st.session_state.turn == 1:
            st.session_state.p1_score += points
        else:
            st.session_state.p2_score += points
            
        # 2. SUCCESS: Refill hand and switch player
        st.session_state.hand = [get_meme_tile() if t == " " else t for t in st.session_state.hand]
        st.session_state.turn = 2 if st.session_state.turn == 1 else 1
        st.session_state.turn_moves = []
        st.success(f"Correct! +{points} Points for Player {1 if st.session_state.turn==2 else 2}")
        st.rerun()
    else:
        # 3. SELF-HEALING: Auto-revert the board if word is fake
        for move in st.session_state.turn_moves:
            st.session_state.board[move['r']][move['c']] = ""
        # Return random tiles to hand for the failed attempt
        st.session_state.hand = [get_meme_tile() if t == " " else t for t in st.session_state.hand]
        st.session_state.turn_moves = []
        st.error(f"'{clean_word}' is not valid! Board healed and turn passed.")
        st.session_state.turn = 2 if st.session_state.turn == 1 else 1
        st.rerun()

if btn_col2.button("🔄 SWAP TILES", use_container_width=True):
    st.session_state.hand = [get_meme_tile() for _ in range(7)]
    st.rerun()
