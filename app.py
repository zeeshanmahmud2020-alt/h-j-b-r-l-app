import streamlit as st
import requests
import random

# 1. Clean UI Setup
st.set_page_config(page_title="H-J-B-R-L", layout="centered")

# Custom CSS for the "Screenshot Look"
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 60px; font-size: 24px; border-radius: 10px; margin-bottom: 10px; }
    .score-text { font-size: 30px; font-weight: bold; text-align: center; color: #f3cf7a; }
    </style>
    """, unsafe_allow_html=True)

# 2. Memory
POOL = ['ক', 'খ', 'গ', 'ঘ', 'চ', 'ছ', 'জ', 'ত', 'দ', 'ন', 'প', 'ব', 'ম', 'র', 'ল', 'স', 'হ', 'া', 'ি', 'ু', 'ে']
if 's1' not in st.session_state:
    st.session_state.update({'s1':0, 's2':0, 'turn':1, 'word':"", 'letters':random.sample(POOL, 7)})

# 3. Header & Score (Symmetric)
st.markdown(f"<div class='score-text'>P1: {st.session_state.s1} | P2: {st.session_state.s2}</div>", unsafe_allow_html=True)
st.write(f"### Player {st.session_state.turn}'s Turn")

# 4. The Word Display (Big and Clear)
st.title(f"👉 {st.session_state.word}")

# 5. The Letter Buttons (One per row for mobile stability)
st.write("---")
for i, l in enumerate(st.session_state.letters):
    if st.button(l, key=f"L_{i}"):
        st.session_state.word += l
        st.rerun()

# 6. Action Buttons
st.write("---")
if st.button("🚀 SUBMIT WORD", type="primary"):
    # Check dictionary
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
        st.error("Invalid word!")

if st.button("🗑️ Clear"):
    st.session_state.word = ""
    st.rerun()
