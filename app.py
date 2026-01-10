import streamlit as st
import random
import requests

# 1. THE SOUL: Graphics & Layout
st.set_page_config(page_title="হ য ব র ল PRO", layout="centered")

@st.cache_resource
def load_dict():
    url = "https://raw.githubusercontent.com/tahmid02016/bangla-wordlist/master/words.txt"
    try:
        r = requests.get(url, timeout=5)
        return set(word.strip() for word in r.text.split())
    except:
        return {"কাকা", "বাবা", "মামা", "কাকি", "বাঘ"}

WORDS_DB = load_dict()

st.markdown("""
    <style>
    .block-container { max-width: 550px !important; padding: 10px !important; }
    
    /* THE TITLE: Centered and Bold */
    .game-title { text-align: center; font-size: 50px; font-weight: bold; color: #f1c40f; margin-bottom: 10px; }

    /* THE BOARD: Physical square buttons */
    div.stButton > button[key^="b_"] {
        background-color: #1e272e !important; color: #ecf0f1 !important;
        width: 44px !important; height: 44px !important;
        border: 1px solid #3d4e5f !important; padding: 0px !important;
        margin: 0px !important; font-size: 16px !important;
    }

    /* THE RACK: Integrated wooden holder */
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
    </style>
    """, unsafe_allow_html=True)

# 2. ROBUST INITIALIZATION
SUB = {"1":"₁", "2":"₂", "3":"₃", "4":"₄", "5":"₅"}
POOL = [('কা',1), ('কি',2), ('কু',2), ('কে',3), ('কো',3), ('পা',1), ('পি',2), ('পু',2), ('মা',1), ('মি',2), ('বা',1), ('বি',2), ('রা',2), ('রে',2), ('না',1), ('নি',2)]

if 'board' not in st.session_state: st.session_state.board = [["" for _ in range(11)] for _ in range(11)]
if 'hand' not in st.session_state: st.session_state.hand = random.sample(POOL, 7)
if 'scores' not in st.session_state: st.session_state.scores = {"P1": 0, "P2": 0}
if 'turn' not in st.session_state: st.session_state.turn = "P1"
if 'sel_idx' not in st.session_state: st.session_state.sel_idx = None
if 'turn_data' not in st.session_state: st.session_state.turn_data = []

# 3. HEADER: Restored Title & Score
st.markdown("<div class='game-title'>হ য ব র ল</div>", unsafe_allow_html=True)
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
                st.session_state.turn_data.append((r, c, char, pts))
                st.session_state.hand[st.session_state.sel_idx] = random.choice(POOL)
                st.session_state.sel_idx = None
                st.rerun()

# 5. THE RACK
st.markdown("<div class='rack-container'>", unsafe_allow_html=True)
h_cols = st.columns(7)
for i, (char, pts) in enumerate(st.session_state.hand):
    if h_cols[i].button(f"{char}{SUB.get(str(pts), '')}", key=f"h_{i}"):
        st.session_state.sel_idx = i
        st.rerun()

# 6. DICTIONARY CHECK & REWIRE (Self-Healing)
word = "".join([d[2] for d in st.session_state.turn_data])
st.write(f"**Turn:** {st.session_state.turn} | **Drafting:** {word}")

if st.button("🔥 SUBMIT WORD", use_container_width=True, type="primary"):
    if len(word) > 1 and word in WORDS_DB:
        turn_pts = sum([d[3] for d in st.session_state.turn_data])
        st.session_state.scores[st.session_state.turn] += turn_pts
        st.session_state.turn = "P2" if st.session_state.turn == "P1" else "P1"
        st.session_state.turn_data = [] 
        st.success(f"'{word}' Accepted! (+{turn_pts})")
        st.rerun()
    else:
        # GIBBERISH REJECTION: Clean the board
        for r, c, char, pts in st.session_state.turn_data:
            st.session_state.board[r][c] = ""
        st.session_state.turn_data = []
        st.error(f"'{word}' is invalid. Move wiped from board.")
        st.rerun()
