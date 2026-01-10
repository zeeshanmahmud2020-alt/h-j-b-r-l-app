import streamlit as st
import random
import requests
import unicodedata

# --- 1. CONFIG & MASSIVE 640k DICTIONARY ---
st.set_page_config(page_title="হ য ব র ল PRO", layout="wide")

@st.cache_resource
def load_massive_dictionary():
    url = "https://raw.githubusercontent.com/maheshwariligade/Bengali-Dictionary/master/bengali_words.txt"
    try:
        response = requests.get(url, timeout=10)
        return set(unicodedata.normalize('NFC', w.strip()) for w in response.text.split())
    except:
        return {"জুতা", "কচি", "বলো", "মা", "বাবা"}

WORDS_DB = load_massive_dictionary()

def get_meme_tile():
    consonants = ['ক', 'খ', 'গ', 'চ', 'জ', 'ত', 'দ', 'ন', 'প', 'ব', 'ম', 'র', 'ল', 'স', 'হ']
    vowels = ['', 'া', 'ি', 'ী', 'ু', 'ে', 'ো'] 
    return random.choice(consonants) + random.choice(vowels)

# --- 2. INITIALIZE STATE (The fix for your AttributeError) ---
if 'p1_score' not in st.session_state:
    st.session_state.update({
        'board': [["" for _ in range(5)] for _ in range(5)],
        'p1_score': 0, 'p2_score': 0, 'turn': 1, 
        'hand': [get_meme_tile() for _ in range(7)],
        'turn_moves': [], 'selected_hand_idx': None
    })

# --- 3. UI LAYOUT ---
st.title("হ য ব র ল PRO")
with st.sidebar:
    st.header("🏆 Live Scores")
    st.subheader(f"Player 1: {st.session_state.p1_score}")
    st.subheader(f"Player 2: {st.session_state.p2_score}")
    st.info(f"👉 Turn: Player {st.session_state.turn}")
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
                val = st.session_state.hand[st.session_state.selected_hand_idx]
                st.session_state.board[r][c] = val
                st.session_state.turn_moves.append({'r': r, 'c': c, 'val': val})
                st.session_state.hand[st.session_state.selected_hand_idx] = " "
                st.session_state.selected_hand_idx = None
                st.rerun()

st.write("### Your Tiles")
hand_cols = st.columns(7)
for i in range(7):
    tile = st.session_state.hand[i]
    if hand_cols[i].button(tile if tile != " " else "✔", key=f"hand_{i}", disabled=(tile == " ")):
        st.session_state.selected_hand_idx = i

# --- 4. THE FIX: SCORE & AUTO-HEAL ---
st.divider()
col_a, col_b = st.columns(2)

if col_a.button("🔥 SUBMIT MOVE", use_container_width=True, type="primary"):
    word_attempt = "".join([m['val'] for m in st.session_state.turn_moves]).strip()
    clean_word = unicodedata.normalize('NFC', word_attempt)
    
    if clean_word in WORDS_DB:
        # 1. Increment score BEFORE clearing
        points = len(clean_word) * 10
        if st.session_state.turn == 1: st.session_state.p1_score += points
        else: st.session_state.p2_score += points
        # 2. Refill and toggle
        st.session_state.hand = [get_meme_tile() if t == " " else t for t in st.session_state.hand]
        st.session_state.turn = 2 if st.session_state.turn == 1 else 1
        st.session_state.turn_moves = []
        st.toast(f"✅ Success: {clean_word}")
        st.rerun()
    else:
        # 3. SELF-HEAL: Remove bad letters from board
        for move in st.session_state.turn_moves:
            st.session_state.board[move['r']][move['c']] = ""
        st.session_state.hand = [get_meme_tile() if t == " " else t for t in st.session_state.hand]
        st.session_state.turn_moves = []
        st.error(f"❌ '{clean_word}' dictionary-তে নেই।")

if col_b.button("🔄 SWAP TILES", use_container_width=True):
    st.session_state.hand = [get_meme_tile() for _ in range(7)]
    st.rerun()
