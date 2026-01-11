import streamlit as st
import requests
import re
import unicodedata
import random

# --- 1. GAME DATA ---
GRAPHEME_VALUES = {
    'ক': 1, 'ত': 1, 'ন': 1, 'প': 1, 'র': 1, 'ল': 1, 'স': 1, 'া': 1, 'ি': 1,
    'গ': 2, 'চ': 2, 'জ': 2, 'দ': 2, 'ব': 2, 'ম': 2, 'ু': 2,
    'খ': 3, 'ছ': 3, 'ট': 3, 'থ': 3, 'ফ': 3, 'ঙ': 8, 'ঞ': 10
}

# Row labels for the board
ROW_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

if 'bag' not in st.session_state:
    raw_bag = (['ক', 'ন', 'প', 'র', 'ল', 'স', 'ত'] * 6 + ['া', 'ি'] * 10 + 
               ['গ', 'চ', 'জ', 'দ', 'ব', 'ম'] * 4 + ['ঙ', 'ঞ'] * 2)
    random.shuffle(raw_bag)
    st.session_state.bag = raw_bag
    st.session_state.p1_rack = [st.session_state.bag.pop() for _ in range(7)]
    st.session_state.p2_rack = [st.session_state.bag.pop() for _ in range(7)]

if 'board' not in st.session_state:
    st.session_state.board = [["" for _ in range(9)] for _ in range(9)]
if 'p1_score' not in st.session_state: st.session_state.p1_score = 0
if 'p2_score' not in st.session_state: st.session_state.p2_score = 0
if 'turn' not in st.session_state: st.session_state.turn = "Player 1"

# --- 2. DICTIONARY ---
@st.cache_data
def load_lexicon():
    url = "https://raw.githubusercontent.com/MinhasKamal/BengaliDictionary/master/BengaliDictionary_17.txt"
    try:
        r = requests.get(url)
        words = re.findall(r'[\u0980-\u09ff]+', r.text)
        return {unicodedata.normalize('NFC', w) for w in words}
    except: return set()
lexicon = load_lexicon()

# --- 3. BRAIN ---
def handle_submission():
    word = st.session_state.word_box_input
    if not word:
        st.warning("⚠️ Please type a word first!")
        return
    
    target = unicodedata.normalize('NFC', word.strip())
    
    # 1. DICTIONARY CHECK
    if target not in lexicon:
        st.error(f"❌ '{target}' is not a valid Bengali word!")
        return

    # 2. BREAK INTO TILES
    tiles_to_place = re.findall(r'[\u0980-\u09ff][\u09be-\u09cc\u09cd\u0981\u0982\u0983]*', target)
    
    # 3. INVENTORY CHECK (Do you have the tiles?)
    rack = st.session_state.p1_rack.copy() if st.session_state.turn == "Player 1" else st.session_state.p2_rack.copy()
    for t in tiles_to_place:
        if t in rack:
            rack.remove(t)
        else:
            st.error(f"❌ You don't have the tile '{t}' in your hand!")
            return

    # 4. PLACEMENT & COLLISION CHECK
    r_idx = ROW_LABELS.index(st.session_state.row_sel)
    c_idx = int(st.session_state.col_sel) - 1
    
    for i, t in enumerate(tiles_to_place):
        curr_r = r_idx + (i if st.session_state.dir_val == "Vertical" else 0)
        curr_c = c_idx + (i if st.session_state.dir_val == "Horizontal" else 0)
        
        if curr_r >= 9 or curr_c >= 9:
            st.error("❌ Word goes off the board edges!")
            return
        
        existing = st.session_state.board[curr_r][curr_c]
        if existing != "" and existing != t:
            st.error(f"❌ Collision at {ROW_LABELS[curr_r]}{curr_c+1}!")
            return

    # 5. SUCCESS: COMMIT MOVE
    score = sum(sum(GRAPHEME_VALUES.get(char, 0) for char in g) for g in tiles_to_place)
    for i, t in enumerate(tiles_to_place):
        curr_r = r_idx + (i if st.session_state.dir_val == "Vertical" else 0)
        curr_c = c_idx + (i if st.session_state.dir_val == "Horizontal" else 0)
        st.session_state.board[curr_r][curr_c] = t

    # Refill Hand
    real_rack = st.session_state.p1_rack if st.session_state.turn == "Player 1" else st.session_state.p2_rack
    for t in tiles_to_place: real_rack.remove(t)
    while len(real_rack) < 7 and st.session_state.bag:
        real_rack.append(st.session_state.bag.pop())

    # Update Score/Turn
    if st.session_state.turn == "Player 1": st.session_state.p1_score += score
    else: st.session_state.p2_score += score
    
    st.session_state.turn = "Player 2" if st.session_state.turn == "Player 1" else "Player 1"
    st.session_state.word_box_input = ""
    st.success(f"✅ Points Added: {score}")

# --- 4. DISPLAY ---
st.sidebar.title("🏆 H.J.B.R.L Arena")
st.sidebar.metric("Player 1", st.session_state.p1_score)
st.sidebar.metric("Player 2", st.session_state.p2_score)
st.sidebar.info(f"Turn: {st.session_state.turn}")
st.sidebar.warning("Hand: " + " | ".join(st.session_state.p1_rack if st.session_state.turn == "Player 1" else st.session_state.p2_rack))
# Shuffle Button Logic
if st.sidebar.button("🔀 Shuffle Hand"):
    if st.session_state.turn == "Player 1":
        random.shuffle(st.session_state.p1_rack)
    else:
        random.shuffle(st.session_state.p2_rack)
    st.rerun()

st.title("🏛️ Bengali Scrabble")
# Grid with Labels
cols = st.columns([0.5] + [1]*9)
cols[0].write("") # Empty corner
for i in range(1, 10): cols[i].write(f"**{i}**") # Column headers

for r_idx, label in enumerate(ROW_LABELS):
    cols = st.columns([0.5] + [1]*9)
    cols[0].write(f"**{label}**") # Row header
    for c_idx in range(9):
        t = st.session_state.board[r_idx][c_idx]
        bg = "#FFD700" if (r_idx, c_idx) == (4, 4) else "#262730"
        cols[c_idx+1].markdown(f"<div style='height:40px; border:1px solid #444; background:{bg}; color:white; text-align:center; line-height:40px;'>{t}</div>", unsafe_allow_html=True)

st.divider()
st.text_input("Type Bengali word:", key="word_box_input")
c1, c2, c3 = st.columns(3)
c1.selectbox("Row", ROW_LABELS, key="row_sel")
c2.selectbox("Column", [str(i) for i in range(1, 10)], key="col_sel")
c3.selectbox("Direction", ["Horizontal", "Vertical"], key="dir_val")

if st.button("Submit Move", on_click=handle_submission): pass
if st.button("Reset"): st.session_state.clear(); st.rerun()
