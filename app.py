import streamlit as st
import random
import requests

# 1. THE SOUL: Tight CSS to kill the "Puke" stretching
st.set_page_config(page_title="হ য ব র ল PRO", layout="centered")

@st.cache_resource
def load_dict():
    url = "https://raw.githubusercontent.com/tahmid02016/bangla-wordlist/master/words.txt"
    try: return set(requests.get(url, timeout=5).text.split())
    except: return {"কাকা", "বাবা", "মামা", "কাকি", "বাঘ"}

WORDS_DB = load_dict()

st.markdown("""
    <style>
    .block-container { max-width: 550px !important; padding: 10px !important; }
    
    /* THE BOARD: Forced Squares */
    div.stButton > button[key^="b_"] {
        background-color: #1e272e !important; color: #ecf0f1 !important;
        width: 44px !important; height: 44px !important;
        border: 1px solid #3d4e5f !important; padding: 0px !important;
        margin: 0px !important; font-size: 16px !important;
    }

    /* THE RACK: Integrated Wooden Tray */
    .rack-container {
        display: flex; justify-content: center; gap: 4px;
        background: linear-gradient(#8b5a2b, #5d3a1a);
        padding: 12px; border-bottom: 6px solid #3d2611;
        border-radius: 4px; margin-top: 10px;
    }
    
    div.stButton > button[key^="h_"] {
        background-color: #f3cf7a !important; color: #3e2723 !important;
        width: 52px !important; height: 60px !important;
        border: 1px solid #b38b4d !important; box-shadow: 0 4px 0 #b38b4d !important;
        font-weight: bold !important; font-size: 18px !important;
    }

    /* Active Turn indicator */
    .active-p { color: #00d2ff; font-weight: bold; border-bottom: 2px solid #00d2ff; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA & STATE (Robust init to stop Crashes)
SUB = {"1":"₁", "2":"₂", "3":"₃", "4":"₄", "5":"₅"}
POOL = [('কা',1), ('কি',2), ('কু',2), ('পা',1), ('মা',1), ('বা',1), ('রে',2), ('না',1), ('নি',2)]

if 'board' not in st.session_state: st.session_state.board = [["" for _ in range(11)] for _ in range(11)]
if 'hand' not in st.session_state: st.session_state.hand = random.sample(POOL, 7)
if 'scores' not in st.session_state: st.session_state.scores = {"P1": 0, "P2": 0}
if 'turn' not in st.session_state: st.session_state.turn = "P1"
if 'sel_idx' not in st.session_state: st.session_state.sel_idx = None
if 'turn_data' not in st.session_state: st.session_state.turn_data = [] # List of (r, c, char)

# 3. SCOREBOARD
st.markdown("<h1 style='text-align:center;'>হ য ব র ল</h1>", unsafe_allow_html=True)
s1, s2 = st.columns(2)
s1.markdown(f"<div class='{'active-p' if st.session_state.turn=='P1' else ''}' style='text-align:center;'>PLAYER 1: {st.session_state.scores['P1']}</div>", unsafe_allow_html=True)
s2.markdown(f"<div class='{'active-p' if st.session_state.turn=='P2' else ''}' style='text-align:center;'>PLAYER 2: {st.session_state.scores['P2']}</div>", unsafe_allow_html=True)

# 4. THE BOARD (11x11 Grid)
for r in range(11):
    cols = st.columns(11)
    for c in range(11):
        val = st.session_state.board[r][c]
        if cols[c].button(val if val else " ", key=f"b_{r}_{c}"):
            if st.session_state.sel_idx is not None:
                char, pts = st.session_state.hand[st.session_state.sel_idx]
                st.session_state.board[r][c] = char
                st.session_state.turn_data.append((r, c, char)) # Memory for healing
                st.session_state.hand[st.session_state.sel_idx] = random.choice(POOL)
                st.session_state.sel_idx = None
                st.rerun()

# 5. THE RACK (No HTML tags, uses Unicode subscripts)
st.markdown("<div class='rack-container'>", unsafe_allow_html=True)
h_cols = st.columns(7)
for i, (char, pts) in enumerate(st.session_state.hand):
    label = f"{char}{SUB.get(str(pts), '')}"
    if h_cols[i].button(label, key=f"h_{i}"):
        st.session_state.sel_idx = i
        st.rerun()

# 6. LEGIT SUBMIT & SELF-HEALING
word = "".join([d[2] for d in st.session_state.turn_data])
st.write(f"Drafting: **{word}**")

if st.button("🔥 SUBMIT WORD", use_container_width=True, type="primary"):
    if word in WORDS_DB:
        st.session_state.scores[st.session_state
