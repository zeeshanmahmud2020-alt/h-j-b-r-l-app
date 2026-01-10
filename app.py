import streamlit as st
import requests
import random

st.set_page_config(page_title="H-J-B-R-L", layout="centered")

# CSS for the Authentic Look
st.markdown("""
    <style>
    .tile-row { display: flex; justify-content: center; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
    div.stButton > button { 
        background-color: #f3cf7a !important; color: #3d2b1f !important; 
        font-weight: bold !important; font-size: 22px !important;
        border-radius: 8px !important; border-bottom: 4px solid #b38b4d !important;
        width: 60px !important; height: 60px !important; padding: 0px !important;
    }
    .main-word { font-size: 50px; text-align: center; color: white; min-height: 70px; border: 1px dashed #444; border-radius: 10px; margin-bottom: 20px;}
    </style>
    """, unsafe_allow_html=True)

# 1. Memory Setup
POOL = ['ক', 'খ', 'গ', 'ঘ', 'চ', 'ছ', 'জ', 'ত', 'দ', 'ন', 'প', 'ব', 'ম', 'র', 'ল', 'স', 'হ', 'া', 'ি', 'ু', 'ে', 'ো', 'ং', '্']
if 's1' not in st.session_state:
    st.session_state.update({'s1':0, 's2':0, 'turn':1, 'word':"", 'letters':random.sample(POOL, 7), 'history': []})

# 2. Score & Word Display
st.markdown(f"### P1: {st.session_state.s1} | P2: {st.session_state.s2}")
st.write(f"👉 **Player {st.session_state.turn}'s Turn**")
st.markdown(f"<div class='main-word'>{st.session_state.word}</div>", unsafe_allow_html=True)

# 3. Tiles (Click to Build)
cols = st.columns(7)
for i, l in enumerate(st.session_state.letters):
    if cols[i].button(l, key=f"t_{i}"):
        st.session_state.word += l
        st.rerun()

# 4. Strict Validation Logic
st.write("---")
c1, c2, c3 = st.columns([2, 1, 1])

if c1.button("🔥 SUBMIT MOVE", type="primary"):
    # Load Dictionary
    dict_url = "https://raw.githubusercontent.com/tahmid02016/bangla-wordlist/master/words.txt"
    words_db = set(requests.get(dict_url).text.split())
    
    if st.session_state.word in words_db:
        pts = len(st.session_state.word)
        # Update Scores
        if st.session_state.turn == 1: st.session_state.s1 += pts
        else: st.session_state.s2 += pts
        
        # Log History
        st.session_state.history.append(f"P{st.session_state.turn}: {st.session_state.word} (+{pts})")
        
        # Reset for Next Turn
        st.session_state.turn = 2 if st.session_state.turn == 1 else 1
        st.session_state.letters = random.sample(POOL, 7)
        st.session_state.word = ""
        st.rerun()
    else:
        # This keeps the turn from ending and the score from changing
        st.error(f"❌ '{st.session_state.word}' is not a valid word. Try again!")
        st.session_state.word = "" # Optional: Clears the bad word so they start over

if c2.button("🔙 Del"):
    st.session_state.word = st.session_state.word[:-1]
    st.rerun()

if c3.button("🔄 Swap"):
    st.session_state.letters = random.sample(POOL, 7)
    st.session_state.word = ""
    st.session_state.turn = 2 if st.session_state.turn == 1 else 1 # Penalize by skipping turn
    st.rerun()

# 5. History
with st.expander("📜 Match History"):
    for move in reversed(st.session_state.history):
        st.write(move)
