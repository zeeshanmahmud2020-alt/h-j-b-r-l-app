import streamlit as st
import random
import requests

# 1. THE SOUL: Graphics & Layout
st.set_page_config(page_title="হ য ব র ল PRO", layout="centered")

@st.cache_resource
def load_dict():
    url = "https://raw.githubusercontent.com/tahmid02016/bangla-wordlist/master/words.txt"
    try:
        return set(requests.get(url, timeout=5).text.split())
    except:
        return {"কাকা", "বাবা", "মামা", "কাকি"}

WORDS_DB = load_dict()

st.markdown("""
    <style>
    .block-container { max-width: 550px !important; padding: 10px !important; }
    div.stButton > button[key^="b_"] {
        background-color: #263238 !important; color: #ecf0f1 !important;
        width: 44px !important; height: 44px !important;
        border: 1px solid #1a252f !important; padding: 0px !important;
        margin: 0px !important; font-size: 16px !important;
    }
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
        font-weight: bold !important; font-size: 18px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. ROBUST INITIALIZATION (Fixes the AttributeError)
if 'board' not in st.session_state:
    st.session_state.board = [["" for _ in range(11)] for _ in range(11)]
if 'hand' not in st.session_state:
    POOL = [('কা',1), ('কি',2), ('কু',2), ('কে',3), ('কো',3), ('পা',1), ('মা',1), ('বা',1), ('রা',2), ('না',1)]
    st.session_state.hand = random.sample(POOL, 7)
if 'scores' not in st.session_state: st.session_state.scores = {"P1": 0, "P2": 0}
if 'turn' not in st.session_state: st.session_state.turn = "P1"
if 'sel_idx' not in st.session_state: st.session_state.sel_idx = None
if 'turn_data' not in st.session_state: st.session_state.turn_data = [] # Stores (r, c, char)

# 3. SCOREBOARD
st.markdown("<h1 style='text-align:center;'>হ য ব র ল</h1>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
c1.metric("Player 1", st.session_state.scores["P1"])
c2.metric("Player 2", st.session_state.scores["P2"])

# 4. THE BOARD (11x11)
for r in range(11):
    cols = st.columns(11)
    for c in range(11):
        val = st.session_state.board[r][c]
        if cols[c].button(val if val else " ", key=f"b_{r}_{c}"):
            if st.session_state.sel_idx is not None:
                char, pts = st.session_state.hand[st.session_state.sel_idx]
                st.session_state.board[r][c] = char
                st.session_state.turn_data.append((r, c, char)) # Remember for self-healing
                
                # Replace tile in hand
                new_tile = random.choice([('কা',1), ('কি',2), ('কু',2), ('কে',3), ('পা',1), ('বা',1)])
                st.session_state.hand[st.session_state.sel_idx] = new_tile
                st.session_state.sel_idx = None
                st.rerun()

# 5. THE RACK
st.markdown("<div class='rack-container'>", unsafe_allow_html=True)
h_cols = st.columns(7)
for i, (char, pts) in enumerate(st.session_state.hand):
    if h_cols[i].button(f"{char}<sub>{pts}</sub>", key=f"h_{i}"):
        st.session_state.sel_idx = i
        st.rerun()

# 6. DICTIONARY CHECK & REWIRE
word = "".join([d[2] for d in st.session_state.turn_data])
st.write(f"Drafting: **{word}**")

if st.button("🔥 SUBMIT WORD", use_container_width=True, type="primary"):
    if word in WORDS_DB:
        st.session_state.scores[st.session_state.turn] += len(word)
        st.session_state.turn = "P2" if st.session_state.turn == "P1" else "P1"
        st.session_state.turn_data = [] # Word is legit, keep on board
        st.success("Accepted!")
        st.rerun()
    else:
        # SELF-HEALING: Rewire the board by deleting invalid letters
        for r, c, char in st.session_state.turn_data:
            st.session_state.board[r][c] = ""
        st.session_state.turn_data = []
        st.error("Invalid word. Letters removed.")
        st.rerun()
