import streamlit as st
import requests
import re
import unicodedata
import random

# --- 1. THE 100 GRAPHEME BAG (The Tiles) ---
# We define specific combined sounds as the actual tiles
if 'bag' not in st.session_state:
    # Common Grapheme Clusters as single tiles
    grapheme_tiles = (
        ['ক', 'কা', 'কি', 'ত', 'তা', 'তি', 'ন', 'না', 'নি', 'প', 'পা', 'র', 'রা', 'রি', 'ল', 'লা', 'লি', 'স', 'সা'] * 4 +
        ['গ', 'গা', 'গী', 'চ', 'চা', 'জ', 'জা', 'দ', 'দা', 'ব', 'বা', 'ম', 'মা'] * 2 +
        ['খ', 'থি', 'ফে', 'ঙ', 'ঞ', 'ষ'] * 2
    )
    # Trim or pad to exactly 100 tiles
    bag = grapheme_tiles[:100]
    random.shuffle(bag)
    st.session_state.bag = bag
    st.session_state.p1_rack = [st.session_state.bag.pop() for _ in range(7)]
    st.session_state.p2_rack = [st.session_state.bag.pop() for _ in range(7)]

# --- 2. GAME STATE ---
ROW_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
GRAPHEME_VALUES = {'ক': 1, 'ত': 1, 'ন': 1, 'প': 1, 'র': 1, 'স': 1, 'গ': 2, 'ঙ': 8, 'ঞ': 10} # Simplified points

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
        # Break input into Graphemes
        tiles_needed = re.findall(r'[\u0980-\u09ff][\u09be-\u09cc\u09cd\u0981\u0982\u0983]*', target)
        
        # Check Hand (Does the player have these specific Grapheme tiles?)
        rack = st.session_state.p1_rack.copy() if st.session_state.turn == "Player 1" else st.session_state.p2_rack.copy()
        for t in tiles_needed:
            if t in rack: rack.remove(t)
            else:
                st.error(f"❌ Missing tile: {t}"); return

        # Coordinate Logic
        r_idx = ROW_LABELS.index(st.session_state.row_sel)
        c_idx = int(st.session_state.col_sel) - 1
        
        # Placement Check
        for i, t in enumerate(tiles_needed):
            curr_r = r_idx + (i if st.session_state.dir_val == "Vertical" else 0)
            curr_c = c_idx + (i if st.session_state.dir_val == "Horizontal" else 0)
            if curr_r >= 9 or curr_c >= 9 or st.session_state.board[curr_r][curr_c] not in ["", t]:
                st.error("❌ Invalid Position"); return

        # Success: Update Board, Rack, and Score
        score = len(tiles_needed) # Simplified for this example
        for i, t in enumerate(tiles_needed):
            curr_r = r_idx + (i if st.session_state.dir_val == "Vertical" else 0)
            curr_c = c_idx + (i if st.session_state.dir_val == "Horizontal" else 0)
            st.session_state.board[curr_r][curr_c] = t

        real_rack = st.session_state.p1_rack if st.session_state.turn == "Player 1" else st.session_state.p2_rack
        for t in tiles_needed: real_rack.remove(t)
        while len(real_rack) < 7 and st.session_state.bag: real_rack.append(st.session_state.bag.pop())

        if st.session_state.turn == "Player 1": st.session_state.p1_score += score
        else: st.session_state.p2_score += score
        st.session_state.turn = "Player 2" if st.session_state.turn == "Player 1" else "Player 1"
        st.session_state.word_box_input = ""
    else: st.error("❌ Invalid word!")

# --- 5. CLEAN UI LAYOUT ---
st.sidebar.title("🏆 H.J.B.R.L Arena")
st.sidebar.metric("Player 1", st.session_state.p1_score)
st.sidebar.metric("Player 2", st.session_state.p2_score)
st.sidebar.info(f"Turn: {st.session_state.turn}")
current_rack = st.session_state.p1_rack if st.session_state.turn == "Player 1" else st.session_state.p2_rack
st.sidebar.warning("Hand: " + " | ".join(current_rack))

if st.sidebar.button("🔀 Shuffle"):
    random.shuffle(current_rack); st.rerun()

st.title("🏛️ Bengali Scrabble")
cols = st.columns([0.5] + [1]*9)
for i in range(1, 10): cols[i].write(f"**{i}**")

for r_idx, label in enumerate(ROW_LABELS):
    cols = st.columns([0.5] + [1]*9)
    cols[0].write(f"**{label}**")
    for c_idx in range(9):
        t = st.session_state.board[r_idx][c_idx]
        bg = "#FFD700" if (r_idx, c_idx) == (4, 4) else "#262730"
        cols[c_idx+1].markdown(f"<div style='height:40px; border:1px solid #444; background:{bg}; color:white; text-align:center; line-height:40px;'>{t}</div>", unsafe_allow_html=True)

st.divider()
st.text_input("Type word:", key="word_box_input")
c1, c2, c3 = st.columns(3)
c1.selectbox("Row", ROW_LABELS, key="row_sel")
c2.selectbox("Column", [str(i) for i in range(1, 10)], key="col_sel")
c3.selectbox("Direction", ["Horizontal", "Vertical"], key="dir_val")
st.button("Submit Move", on_click=handle_submission)
if st.button("Reset"): st.session_state.clear(); st.rerun()
