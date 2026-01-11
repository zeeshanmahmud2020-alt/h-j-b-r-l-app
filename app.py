import streamlit as st
import requests
import re
import unicodedata

# 1. INITIALIZE ARCHITECTURAL STATE (Memory)
if 'board' not in st.session_state:
    st.session_state.board = [["" for _ in range(9)] for _ in range(9)]
if 'p1_score' not in st.session_state:
    st.session_state.p1_score = 0
if 'p2_score' not in st.session_state:
    st.session_state.p2_score = 0
if 'turn' not in st.session_state:
    st.session_state.turn = "Player 1"

# 2. THE ENGINE: LOAD DICTIONARY FROM GITHUB
@st.cache_data
def load_lexicon():
    url = "https://raw.githubusercontent.com/MinhasKamal/BengaliDictionary/master/BengaliDictionary_17.txt"
    lexicon = set()
    try:
        r = requests.get(url)
        # Extract Bengali script only
        words = re.findall(r'[\u0980-\u09ff]+', r.text)
        for w in words:
            lexicon.add(unicodedata.normalize('NFC', w))
        return lexicon
    except:
        return set()

lexicon = load_lexicon()

# 3. SIDEBAR SCOREBOARD
st.sidebar.title("🏆 H.J.B.R.L Arena")
st.sidebar.metric("Player 1", f"{st.session_state.p1_score} pts")
st.sidebar.metric("Player 2", f"{st.session_state.p2_score} pts")
st.sidebar.info(f"Current Turn: {st.session_state.turn}")

# 4. MAIN BOARD DISPLAY (9x9)
st.title("🏛️ Bengali Scrabble Arena")
for r in range(9):
    cols = st.columns(9)
    for c in range(9):
        tile = st.session_state.board[r][c]
        # Yellow center for the first move
        color = "#FFD700" if (r, c) == (4, 4) else "#262730"
        cols[c].markdown(
            f"<div style='height:45px; border:1px solid #555; background:{color}; "
            f"text-align:center; line-height:45px; font-size:20px; font-weight:bold; color:white;'>"
            f"{tile}</div>", unsafe_allow_html=True
        )

# 5. THE GEARBOX: PLACEMENT & VALIDATION
st.divider()
word_to_place = st.text_input("Type your word here:")
c1, c2, c3 = st.columns(3)
row_idx = c1.number_input("Start Row", 0, 8)
col_idx = c2.number_input("Start Col", 0, 8)
orient = c3.selectbox("Direction", ["Horizontal", "Vertical"])

if st.button("Confirm Move & End Turn"):
    if word_to_place:
        # Step A: Normalize (Official Spelling)
        target = unicodedata.normalize('NFC', word_to_place.strip())
        
        # Step B: Check Lexicon
        if target in lexicon:
            # Step C: Split into Aksharas (Shondhi-aware)
            # This regex captures consonants + their vowel signs/hasanta clusters
            tiles = re.findall(r'[\u0980-\u09ff][\u09be-\u09cc\u09cd\u0981\u0982\u0983]*', target)
            
            # Step D: Write to Board
            for i, t in enumerate(tiles):
                r_pos = row_idx + (i if orient == "Vertical" else 0)
                c_pos = col_idx + (i if orient == "Horizontal" else 0)
                if r_pos < 9 and c_pos < 9:
                    st.session_state.board[r_pos][c_pos] = t
            
            # Step E: Update Scores & Swap Turn
            points = len(tiles)
            if st.session_state.turn == "Player 1":
                st.session_state.p1_score += points
                st.session_state.turn = "Player 2"
            else:
                st.session_state.p2_score += points
                st.session_state.turn = "Player 1"
            
            st.success(f"Verified! '{target}' is valid. {points} points awarded.")
            st.rerun()
        else:
            st.error("❌ Word not found in Bengali dictionary. Try again!")

# 6. RESET BUTTON
if st.button("Reset Arena"):
    st.session_state.clear()
    st.rerun()
