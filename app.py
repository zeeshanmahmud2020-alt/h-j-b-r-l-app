import streamlit as st
import requests
import re
import unicodedata

# 1. PERMANENT MEMORY SETUP
if 'board' not in st.session_state:
    st.session_state.board = [["" for _ in range(9)] for _ in range(9)]
if 'p1_score' not in st.session_state:
    st.session_state.p1_score = 0
if 'p2_score' not in st.session_state:
    st.session_state.p2_score = 0
if 'turn' not in st.session_state:
    st.session_state.turn = "Player 1"

# 2. DICTIONARY LOADING (Kamal Lexicon)
@st.cache_data
def load_lexicon():
    url = "https://raw.githubusercontent.com/MinhasKamal/BengaliDictionary/master/BengaliDictionary_17.txt"
    try:
        r = requests.get(url)
        words = re.findall(r'[\u0980-\u09ff]+', r.text)
        return {unicodedata.normalize('NFC', w) for w in words}
    except: return set()

lexicon = load_lexicon()

# 3. SIDEBAR SCOREBOARD
st.sidebar.title("🏆 H.J.B.R.L Arena")
st.sidebar.metric("Player 1", f"{st.session_state.p1_score}")
st.sidebar.metric("Player 2", f"{st.session_state.p2_score}")
st.sidebar.info(f"It is {st.session_state.turn}'s turn")

# 4. MAIN BOARD DISPLAY (9x9)
st.title("🏛️ Bengali Scrabble Arena")
for r in range(9):
    cols = st.columns(9)
    for c in range(9):
        tile = st.session_state.board[r][c]
        color = "#FFD700" if (r, c) == (4, 4) else "#262730"
        cols[c].markdown(f"<div style='height:45px; border:1px solid #555; background:{color}; text-align:center; line-height:45px; font-size:20px; font-weight:bold; color:white;'>{tile}</div>", unsafe_allow_html=True)

# 5. INPUT & VALIDATION
st.divider()
# Added 'key' to allow the machine to wipe the box after submission
user_input = st.text_input("Type your Bengali word:", key="word_box")
c1, c2, c3 = st.columns(3)
r_start = c1.number_input("Start Row", 0, 8)
c_start = c2.number_input("Start Col", 0, 8)
orient = c3.selectbox("Direction", ["Horizontal", "Vertical"])

if st.button("Confirm Move & End Turn"):
    if user_input:
        target = unicodedata.normalize('NFC', user_input.strip())
        
        if target in lexicon:
            # SHONDHI FIX: Grouping consonant + vowel signs
            tiles = re.findall(r'[\u0980-\u09ff][\u09be-\u09cc\u09cd\u0981\u0982\u0983]*', target)
            
            # --- THE SAFETY CHECKER ---
            can_place = True
            for i, t in enumerate(tiles):
                curr_r = r_start + (i if orient == "Vertical" else 0)
                curr_c = c_start + (i if orient == "Horizontal" else 0)
                
                # 1. Off-Board Check
                if curr_r >= 9 or curr_c >= 9:
                    can_place = False
                    st.error("❌ Word goes off the board!")
                    break
                
                # 2. Collision Check (Overlap Guard)
                existing = st.session_state.board[curr_r][curr_c]
                if existing != "" and existing != t:
                    can_place = False
                    st.error(f"❌ Collision at {curr_r},{curr_c}! Cannot overwrite '{existing}' with '{t}'.")
                    break

            # --- THE FINAL COMMIT ---
            if can_place:
                for i, t in enumerate(tiles):
                    curr_r = r_start + (i if orient == "Vertical" else 0)
