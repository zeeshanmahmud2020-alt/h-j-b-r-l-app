import streamlit as st
import random
import requests

# 1. THE SOUL: Fast & Integrated Graphics
st.set_page_config(page_title="হ য ব র ল PRO", layout="centered")

@st.cache_resource
def load_clean_dict():
    # This is a vetted Bengali word list (no slang/proper nouns)
    url = "https://raw.githubusercontent.com/tahmid02016/bangla-wordlist/master/words.txt"
    try:
        r = requests.get(url, timeout=5)
        return set(r.text.split()) # O(1) Search Efficiency
    except:
        return {"কাকা", "বাবা", "মামা", "কাকি", "বাঘ", "নাম"}

WORDS_DB = load_clean_dict()

st.markdown("""
    <style>
    .block-container { max-width: 550px !important; padding: 10px !important; }
    
    /* THE BOARD: Efficiency Grid */
    div.stButton > button[key^="b_"] {
        background-color: #263238 !important; color: #ecf0f1 !important;
        width: 44px !important; height: 44px !important;
        border: 1px solid #1a252f !important; padding: 0px !important;
        margin: 0px !important; font-size: 16px !important;
    }

    /* THE RACK: Integrated Wooden Bar */
    .rack-container {
        display: flex; justify-content: center; gap: 4px;
        background: linear-gradient(#8b5a2b, #5d3a1a);
        padding: 12px; border-bottom: 6px solid #3d2611;
        border-radius: 4px; margin-top: 20px;
    }
    
    div.stButton > button[key^="h_"] {
        background-color: #f3cf7a !important; color: #3e2723 !important;
        width: 52px !important; height: 65px !important;
        border: 1px solid #b38b4d !important; box-shadow: 0 4px 0 #b38b4d !important;
        font-weight: bold !important; font-size: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA: Integrated Vowels (Ka, Ki, Ku...)
SUB = {"1":"₁", "2":"₂", "3":"₃", "4":"₄", "5":"₅"}
POOL = [
    ('কা',1), ('কি',2), ('কু',2), ('কে',3), ('কো',3),
    ('পা',1), ('পি',2), ('পু',2), ('পে',3), ('পো',3),
    ('মা',1), ('মি',2), ('মু',2), ('মে',3), ('মো',3),
    ('বা',1), ('বি',2), ('বু',2), ('বে',3), ('বো',3),
    ('রা',1), ('রি',2), ('রু',2), ('রে',3), ('রো',3),
    ('না',1), ('নি',2), ('নু',2), ('নে',3), ('নো',3)
]

if 'board' not in st.session_state: st.session_state.board = [["" for _ in range(11)] for _ in range(11)]
if 'hand' not in st.session_state: st.session_state.hand = random.sample(POOL, 7)
if 'scores' not in st.session_state: st.session_state.scores = {"P1": 0, "P2": 0}
if 'turn' not in st.session_state: st.session_state.turn = "P1"
if 'current_move' not in st.session_state: st.session_state.current_move = []

# 3. Game Layout
st.markdown("<h1 style='text-align:center;'>হ য ব র ল</h1>", unsafe_allow_html=True)
st.write(f"**Score** | P1: {st.session_state.scores['P1']} | P2: {st.session_state.scores['P2']}")

for r in range(11):
    cols = st.columns(11)
    for c in range(11):
        val = st.session_state.board[r][c]
        if cols[c].button(val if val else " ", key=f"b_{r}_{c}"):
            if 'sel_idx' in st.session_state and st.session_state.sel_idx is not None:
                char, pts = st.session_state.hand[st.session_state.sel_idx]
                st.session_state.board[r][c] = char
                st.session_state.current_move.append(char)
                st.session_state.hand[st.session_state.sel_idx] = random.choice(POOL)
                st.session_state.sel_idx = None
                st.rerun()

st.markdown("<div class='rack-container'>", unsafe_allow_html=True)
h_cols = st.columns(7)
for i, (char, pts) in enumerate(st.session_state.hand):
    if h_cols[i].button(f"{char}{SUB.get(str(pts), '')}", key=f"h_{i}"):
        st.session_state.sel_idx = i
        st.rerun()

# 4. Efficiency Verification
word = "".join(st.session_state.current_move)
if st.button("🔥 SUBMIT WORD", use_container_width=True, type="primary"):
    if word in WORDS_DB: # Instant O(1) Check
        st.session_state.scores[st.session_state.turn] += len(word)
        st.session_state.turn = "P2" if st.session_state.turn == "P1" else "P1"
        st.session_state.current_move = []
        st.success(f"'{word}' Accepted!")
        st.rerun()
    else:
        st.error(f"'{word}' is not a valid word. Try again!")
        st.session_state.current_move = []
