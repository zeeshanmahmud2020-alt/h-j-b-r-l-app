import streamlit as st
import requests
import random

# 1. Page Config
st.set_page_config(page_title="H-J-B-R-L BD", layout="centered")

# 2. Memory Setup
POOL = ['ক', 'খ', 'গ', 'ঘ', 'চ', 'ছ', 'জ', 'ত', 'দ', 'ন', 'প', 'ব', 'ম', 'র', 'ল', 'স', 'হ', 
        'অ', 'আ', 'ই', 'উ', 'এ', 'ও', 'া', 'ি', 'ী', 'ু', 'ূ', 'ে', 'ৈ', 'ো', 'ৌ']

if 's1' not in st.session_state:
    st.session_state.update({'s1':0, 's2':0, 'turn':1, 'word':"", 'letters':random.sample(POOL, 7)})

# 3. Header & Scores
st.title("𝐇-𝐉-𝐁-𝐑-𝐋 𝐁𝐃")
st.write(f"**P1:** {st.session_state.s1} | **P2:** {st.session_state.s2} — **Player {st.session_state.turn}'s Turn**")

# 4. Clickable Tiles
st.write("### Your Tiles (Click to type):")
cols = st.columns(7)
for i, l in enumerate(st.session_state.letters):
    if cols[i].button(l, key=f"tile_{i}"):
        st.session_state.word += l
        st.rerun()

# 5. Display the word being built
st.markdown(f"## Current: `{st.session_state.word}`")

# 6. Action Buttons
col_a, col_b, col_c = st.columns([2, 1, 1])

if col_a.button("🚀 SUBMIT MOVE", type="primary"):
    # Load dictionary only on click to save speed
    dict_url = "https://raw.githubusercontent.com/tahmid02016/bangla-wordlist/master/words.txt"
    words_db = set(requests.get(dict_url).text.split())
    
    if st.session_state.word in words_db:
        pts = len(st.session_state.word)
        if st.session_state.turn == 1: st.session_state.s1 += pts
        else: st.session_state.s2 += pts
        
        # Next Turn Logic
        st.session_state.turn = 2 if st.session_state.turn == 1 else 1
        st.session_state.letters = random.sample(POOL, 7)
        st.session_state.word = ""
        st.success("Valid Word! Points added.")
        st.rerun()
    else:
        st.error("❌ Invalid Word")

if col_b.button("🔙 Delete"):
    st.session_state.word = st.session_state.word[:-1]
    st.rerun()

if col_c.button("🗑️ Clear"):
    st.session_state.word = ""
    st.rerun()
