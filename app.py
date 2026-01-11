import streamlit as st
import requests
import re
import unicodedata
import random

# --- 1. DATA HELPERS ---
BENGALI_NUMS = {'0':'০', '1':'১', '2':'২', '3':'৩', '4':'৪', '5':'৫', '6':'৬', '7':'৭', '8':'৮', '9':'৯'}

def to_bn(num):
    return "".join(BENGALI_NUMS.get(d, d) for d in str(num))

# Point values for Grapheme Tiles
GRAPHEME_VALUES = {
    'ক': 1, 'কা': 1, 'ি': 1, 'ত': 1, 'ন': 1, 'র': 1, 'ল': 1, 'স': 1,
    'গ': 2, 'চ': 2, 'জ': 2, 'দ': 2, 'ব': 2, 'ম': 2, 'ু': 2,
    'খ': 3, 'ট': 3, 'থ': 3, 'ফ': 3, 'ন্দ': 5, 'ক্ট': 5, 'ষ্ট': 5,
    'ঙ': 8, 'ঞ': 10, 'ৎ': 10
}

# --- 2. INITIALIZE GAME ---
if 'bag' not in st.session_state:
    # A fixed pool of 100 Grapheme tiles
    pool = (['ক', 'কা', 'ত', 'তা', 'ন', 'না', 'র', 'রা', 'ল', 'লা', 'স', 'সা'] * 5 +
            ['গ', 'গা', 'চ', 'জ', 'দ', 'দা', 'ব', 'বা', 'ম', 'মা', 'ি', 'ু'] * 3 +
            ['ন্দ', 'ক্ট', 'ষ্ট', 'ঙ', 'ঞ', 'ৎ'] * 2)
    st.session_state.bag = pool[:100]
    random.shuffle(st.session_state.bag)
    st.session_state.p1_rack = [st.session_state.bag.pop() for _ in range(7)]
    st.session_state.p2_rack = [st.session_state.bag.pop() for _ in range(7)]

ROW_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

if 'board' not in st.session_state:
    st.session_state.board = [["" for _ in range(9)] for _ in range(9)]
if 'p1_score' not in st.session_state: st.session_state.p1_score = 0
if 'p2_score' not in st.session_state: st.session_state.p2_score = 0
if 'turn' not in st.session_state: st.session_state.turn = "Player 1"

# --- 3. DICTIONARY ---
@st.cache_data
def load_lexicon():
    url = "https://raw.githubusercontent.com/MinhasKamal/BengaliDictionary/master/BengaliDictionary_17.txt"
    try:
        r = requests.get(url)
        words = re.findall(r'[\u0980-\u09ff]+', r.text)
        return {unicodedata.normalize('NFC', w) for w in words}
    except: return set()
lexicon = load_lexicon()

# --- 4. THE BRAIN ---
def handle_submission():
    word = st.session_state.word_box_input
    if not word: return
    target = unicodedata.normalize('NFC', word.strip())
    
    if target in lexicon:
        tiles_needed = re.findall(r'[\u0980-\u09ff][\u09be-\u09cc\u09cd\u0981\u0982\u0983]*', target)
        rack = st.session_state.p1_rack if st.session_state.turn == "Player 1" else st.session_state.p2_rack
        
        # Inventory Check
        temp_rack = rack.copy()
        for t in tiles_needed:
            if t in temp_rack: temp_rack.remove(t)
            else: st.error(f"❌ Missing tile: {t}"); return

        # Coordinate Calculation
        r_idx = ROW_LABELS.index(st.session_state.row_sel)
        c_idx = int(st.session_state.col_sel) - 1
        
        # Collision/Off-board Check
        for i, t in enumerate(tiles_needed):
            curr_r = r_idx + (i if st.session_state.dir_val == "Vertical" else 0)
            curr_c = c_idx + (i if st.session_state.dir_val == "Horizontal" else 0)
            if curr_r >= 9 or curr_c >= 9: st.error("❌ Off board!"); return
            if st.session_state.board[curr_r][curr_c] not in ["", t]: st.error("❌ Collision!"); return

        # Apply Score and Move
        move_score = sum(GRAPHEME_VALUES.get(t, 1) for t in tiles_needed)
        for i, t in enumerate(tiles_needed):
            curr_r = r_idx + (i if st.session_state.dir_val == "Vertical" else 0)
            curr_c = c_idx + (i if st.session_state.dir_val == "Horizontal" else 0)
            st.session_state.board[curr_r][curr_c] = t

        # Update Rack
        for t in tiles_needed: rack.remove(t)
        while len(rack) < 7 and st.session_state.bag: rack.append(st.session_state.bag.pop())
        
        if st.session_state.turn == "Player 1": st.session_state.p1_score += move_score
        else: st.session_state.p2_score += move_score
        st.session_state.turn = "Player 2" if st.session_state.turn == "Player 1" else "Player 1"
        st.session_state.word_box_input = ""
    else:
        st.error("❌ Invalid word!")

# --- 5. CLEAN UI ---
st.sidebar.title("🏆 H.J.B.R.L Arena")
st.sidebar.metric("Player 1", st.session_state.p1_score)
st.sidebar.metric("Player 2", st.session_state.p2_score)
st.sidebar.info(f"Turn: {st.session_state.turn}")

# Current Rack Display
current_rack = st.session_state.p1_rack if st.session_state.turn == "Player 1" else st.session_state.p2_rack
st.sidebar.markdown(f"### Hand: `{' | '.join(current_rack)}`")

# Shuffle & Swap Controls
c1, c2 = st.sidebar.columns(2)
if c1.button("🔀 Shuffle"):
    random.shuffle(current_rack)
    st.rerun()

if c2.button("🔄 Swap"):
    st.session_state.bag.extend(current_rack)
    random.shuffle(st.session_state.bag)
    new_rack = [st.session_state.bag.pop() for _ in range(7)]
    if st.session_state.turn == "Player 1": st.session_state.p1_rack = new_rack
    else: st.session_state.p2_rack = new_rack
    st.session_state.turn = "Player 2" if st.session_state.turn == "Player 1" else "Player 1"
    st.rerun()

st.title("🏛️ Bengali Scrabble")

# Header Numbers
cols = st.columns([0.5] + [1]*9)
for i in range(1, 10): cols[i].write(f"**{i}**")

# Grid Layout
for r_idx, label in enumerate(ROW_LABELS):
    cols = st.columns([0.5] + [1]*9)
    cols[0].write(f"**{label}**")
    for c_idx in range(9):
        tile_text = st.session_state.board[r_idx][c_idx]
        pts = to_bn(GRAPHEME_VALUES.get(tile_text, "")) if tile_text else ""
        bg = "#FFD700" if (r_idx, c_idx) == (4, 4) else "#262730"
        cols[c_idx+1].markdown(f"<div style='height:45px; border:1px solid #444; background:{bg}; color:white; text-align:center; position:relative; font-size:20px; line-height:45px;'>{tile_text}<sub style='font-size:10px; position:absolute; bottom:2px; right:2px; color:#aaa;'>{pts}</sub></div>", unsafe_allow_html=True)

st.divider()
st.text_input("Type Bengali word:", key="word_box_input")
u1, u2, u3 = st.columns(3)
u1.selectbox("Row", ROW_LABELS, key="row_sel")
u2.selectbox("Column", [str(i) for i in range(1, 10)], key="col_sel")
u3.selectbox("Direction", ["Horizontal", "Vertical"], key="dir_val")
st.button("Submit Move", on_click=handle_submission)
if st.button("Reset Game"): st.session_state.clear(); st.rerun()
