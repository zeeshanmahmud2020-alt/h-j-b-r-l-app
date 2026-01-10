import streamlit as st
import random
import requests

# 1. THE SOUL: High-End Game Styling
st.set_page_config(page_title="হ য ব র ল PRO", layout="centered")

@st.cache_resource
def load_dict():
    url = "https://raw.githubusercontent.com/tahmid02016/bangla-wordlist/master/words.txt"
    try: return set(requests.get(url).text.split())
    except: return {"কাকা", "বাবা", "মা"}

WORDS_DB = load_dict()

st.markdown("""
    <style>
    .block-container { max-width: 550px !important; padding: 10px !important; }
    
    /* THE BOARD: Hard-Locked Grid */
    div.stButton > button[key^="b_"] {
        background-color: #263238 !important; color: #ecf0f1 !important;
        width: 44px !important; height: 44px !important;
        border: 1px solid #1a252f !important; padding: 0px !important;
        margin: 0px !important; font-size: 14px !important;
    }

    /* THE RACK: Physical Wooden Bar */
    .rack-container {
        display: flex; justify-content: center; gap: 4px;
        background: linear-gradient(#8b5a2b, #5d3a1a);
        padding: 12px; border-bottom: 6px solid #3d2611;
        border-radius: 4px; margin-top: 20px;
    }
    
    div.stButton > button[key^="h_"] {
        background-color: #f3cf7a !important; color: #3e2723 !important;
        width: 50px !important; height: 60px !important;
        border: 1px solid #b38b4d !important; box-shadow: 0 4px 0 #b38b4d !important;
        font-weight: bold !important; font-size: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA & STATE
SUB = {"1":"₁", "2":"₂", "3":"₃", "4":"₄", "5":"₅", "6":"₆", "7":"₇", "8":"₈", "9":"₉", "0":"₀"}
POOL = [('ক',1), ('খ',2), ('গ',2), ('প',1), ('ম',1), ('ব',2), ('র',1), ('ল',1), ('স',2), ('হ',3), ('া',1), ('ি',2), ('ু',2)]

if 'board' not in st.session_state: st.session_state.board = [["" for _ in range(11)] for _ in range(11)]
if 'hand' not in st.session_state: st.session_state.hand = random.sample(POOL, 7)
if 'scores' not in st.session_state: st.session_state.scores = {"P1": 0, "P2": 0}
if 'turn' not in st.session_state: st.session_state.turn = "P1"
if 'sel_idx' not in st.session_state: st.session_state.sel_idx = None
if 'current_word' not in st.session_state: st.session_state.current_word = ""

# 3. SCOREBOARD
st.markdown("<h1 style='text-align:center;'>হ য ব র ল</h1>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
c1.metric("Player 1", st.session_state.scores["P1"])
c2.metric("Player 2", st.session_state.scores["P2"])

# 4. THE BOARD (11x11 Grid)
for r in range(11):
    cols = st.columns(11)
    for c in range(11):
        val = st.session_state.board[r][c]
        if cols[c].button(val if val else " ", key=f"b_{r}_{c}"):
            if st.session_state.sel_idx is not None:
                char, pts = st.session_state.hand[st.session_state.sel_idx]
                st.session_state.board[r][c] = char
                st.session_state.current_word += char # Track for dictionary
                st.session_state.hand[st.session_state.sel_idx] = random.choice(POOL)
                st.session_state.sel_idx = None
                st.rerun()

# 5. THE RACK (The Holder)
st.markdown("<div class='rack-container'>", unsafe_allow_html=True)
h_cols = st.columns(7)
for i, (char, pts) in enumerate(st.session_state.hand):
    pt_sub = "".join(SUB.get(d, d) for d in str(pts))
    if h_cols[i].button(f"{char}{pt_sub}", key=f"h_{i}"):
        st.session_state.sel_idx = i
        st.rerun()

# 6. SUBMIT & DICTIONARY CHECK
st.write(f"**Current Turn:** {st.session_state.turn} | **Word Built:** {st.session_state.current_word}")
if st.button("🔥 SUBMIT TURN", use_container_width=True, type="primary"):
    if st.session_state.current_word in WORDS_DB:
        st.session_state.scores[st.session_state.turn] += len(st.session_state.current_word)
        st.session_state.turn = "P2" if st.session_state.turn == "P1" else "P1"
        st.session_state.current_word = ""
        st.toast("Valid Word!")
        st.rerun()
    else:
        st.error(f"'{st.session_state.current_word}' not found. Word reset.")
        st.session_state.current_word = ""
        st.rerun()
