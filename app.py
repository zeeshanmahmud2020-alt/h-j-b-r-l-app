import streamlit as st
import random
import requests
import unicodedata

# --- 1. CONFIG & DICTIONARY ---
st.set_page_config(page_title="হ য ব র ল PRO", layout="wide")

# Custom CSS to make the labels inside buttons look right if needed
st.markdown("""<style> div.stButton > button > div > p { font-size: 1.2rem; } </style>""", unsafe_allow_html=True)

@st.cache_resource
def load_massive_dictionary():
    url = "https://raw.githubusercontent.com/maheshwariligade/Bengali-Dictionary/master/bengali_words.txt"
    safety = {"লাখ", "জুতা", "কচি", "বলো", "মা", "বাবা", "বাড়ি", "খেলো", "গে"}
    try:
        r = requests.get(url, timeout=5)
        return safety.union(set(unicodedata.normalize('NFC', w.strip()) for w in r.text.split()))
    except:
        return safety

WORDS_DB = load_massive_dictionary()

def get_clean_tile():
    consonants = ['ক', 'খ', 'গ', 'চ', 'জ', 'ত', 'দ', 'ন', 'প', 'ব', 'ম', 'র', 'ল', 'স', 'হ']
    letter = random.choice(consonants)
    num = random.randint(1, 9)
    # Using specific subscript unicode characters so they render on buttons
    subscripts = ["₀", "₁", "₂", "₃", "₄", "₅", "₆", "₇", "₈", "₉"]
    return f"{letter}{subscripts[num]}"

# --- 2. SESSION STATE ---
if 'p1_score' not in st.session_state:
    st.session_state.update({
        'board': [["" for _ in range(5)] for _ in range(5)],
        'p1_score': 0, 'p2_score': 0, 'turn': 1, 
        'hand': [get_clean_tile() for _ in range(7)],
        'turn_moves': [], 'selected_hand_idx': None
    })

# --- 3. UI ---
st.title("হ য ব র ল PRO")
with st.sidebar:
    st.header("🏆 Scores")
    st.metric("P1", st.session_state.p1_score)
    st.metric("P2", st.session_state.p2_score)
    st.write(f"👉 **Turn: Player {st.session_state.turn}**")
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
                st.session_state.turn_moves.append({'r': r, 'c': c, 'val': val, 'h_idx': st.session_state.selected_hand_idx})
                st.session_state.hand[st.session_state.selected_hand_idx] = " " 
                st.session_state.selected_hand_idx = None
                st.rerun()

st.write("### Your Hand")
hand_cols = st.columns(7)
for i in range(7):
    tile = st.session_state.hand[i]
    if hand_cols[i].button(tile if tile != " " else "---", key=f"hand_{i}", disabled=(tile == " ")):
        st.session_state.selected_hand_idx = i

# --- 4. THE LOGIC ---
st.divider()
col_a, col_b, col_c = st.columns(3)

# SUBMIT: Only ends turn if word is VALID
if col_a.button("🔥 SUBMIT WORD", use_container_width=True, type="primary"):
    # Strip the unicode subscripts for the dictionary check
    raw_word = "".join([m['val'] for m in st.session_state.turn_moves])
    clean_word = "".join([c for c in raw_word if '\u0980' <= c <= '\u09FF']).strip()
    
    if clean_word in WORDS_DB:
        points = len(clean_word) * 10
        if st.session_state.turn == 1: st.session_state.p1_score += points
        else: st.session_state.p2_score += points
        st.session_state.hand = [get_clean_tile() if t == " " else t for t in st.session_state.hand]
        st.session_state.turn_moves = []
        st.session_state.turn = 2 if st.session_state.turn == 1 else 1
        st.rerun()
    else:
        st.error(f"❌ '{clean_word}' dictionary-তে নেই! Try again or Recall.")

# RECALL: Scrabble-style recovery
if col_b.button("↩️ TRY AGAIN (Recall)", use_container_width=True):
    for m in st.session_state.turn_moves:
        st.session_state.board[m['r']][m['c']] = ""
        st.session_state.hand[m['h_idx']] = m['val']
    st.session_state.turn_moves = []
    st.rerun()

# SKIP & SWAP: Clears board moves and gives new hand
if col_c.button("🔄 SKIP & SWAP", use_container_width=True):
    # Wipe any tiles currently on the board from this failed turn
    for m in st.session_state.turn_moves:
        st.session_state.board[m['r']][m['c']] = ""
    st.session_state.hand = [get_clean_tile() for _ in range(7)]
    st.session_state.turn_moves = []
    st.session_state.turn = 2 if st.session_state.turn == 1 else 1
    st.rerun()
