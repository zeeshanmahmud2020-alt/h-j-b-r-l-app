import streamlit as st
import requests
import random

# 1. Professional Page Setup
st.set_page_config(page_title="H-J-B-R-L", layout="centered")

# 2. Custom CSS for Horizontal Clickable Tiles
st.markdown("""
    <style>
    .tile-row { display: flex; justify-content: center; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
    div.stButton > button { 
        background-color: #f3cf7a !important; color: #3d2b1f !important; 
        font-weight: bold !important; font-size: 22px !important;
        border-radius: 8px !important; border-bottom: 4px solid #b38b4d !important;
        width: 60px !important; height: 60px !important; padding: 0px !important;
    }
    .main-word { font-size: 50px; text-align: center; color: white; margin-bottom: 10px; min-height: 60px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Game State
POOL = ['ক', 'খ', 'গ', 'ঘ', 'চ', 'ছ', 'জ', 'ত', 'দ', 'ন', 'প', 'ব', 'ম', 'র', 'ল', 'স', 'হ', 'া', 'ি', 'ু', 'ে', 'ো']
if 's1' not in st.session_state:
    st.session_state.update({'s1':0, 's2':0, 'turn':1, 'word':"", 'letters':random.sample(POOL, 7)})

# 4. Score & Turn
st.markdown(f"### P1: {st.session_state.s1} | P2: {st.session_state.s2}")
st.write(f"👉 **Player {st.session_state.turn}'s Turn**")

# 5. The Active Word
st.markdown(f"<div class='main-word'>{st.session_state.word}</div>", unsafe_allow_html=True)

# 6. Horizontal Tile Hand
st.write("---")
cols = st.columns(7)
for i, l in enumerate(st.session_state.letters):
    if cols[i].button(l, key=f"t_{i}"):
        st.session_state.word += l
        st.rerun()

# 7. Action Controls
st.write("---")
c1, c2 = st.columns([3, 1])

if c1.button("🔥 SUBMIT MOVE", type="primary"):
    r = requests.get("https://raw.githubusercontent.com/tahmid02016/bangla-wordlist/master/words.txt")
    if st.session_state.word in set(r.text.split()):
        pts = len(st.session_state.word)
        if st.session_state.turn == 1: st.session_state.s1 += pts
        else: st.session_state.s2 += pts
        st.session_state.turn = 2 if st.session_state.turn == 1 else 1
        st.session_state.letters = random.sample(POOL, 7)
        st.session_state.word = ""
        st.rerun()
    else:
        st.error("Invalid Bengali word!")

if c2.button("🔙 Del"):
    st.session_state.word = st.session_state.word[:-1]
    st.rerun()
