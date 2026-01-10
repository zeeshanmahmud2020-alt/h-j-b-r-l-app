import streamlit as st
import random

# 1. Initialize Memory
if 's1' not in st.session_state:
    st.session_state.s1 = 0
    st.session_state.s2 = 0
    st.session_state.turn = 1
    # Random Bengali letters for the start
    st.session_state.letters = random.sample(['ক', 'খ', 'গ', 'ঘ', 'চ', 'ছ', 'জ', 'ত', 'প', 'ল', 'স', 'ম', 'ন', 'র'], 7)

# 2. UI Header
st.title("𝐇-𝐉-𝐁-𝐑-𝐋 𝐁𝐃")
st.write(f"**Score:** P1: {st.session_state.s1} | P2: {st.session_state.s2}")
st.divider()

# 3. The Letter Bank (Your "Hand")
st.subheader("Your Letters:")
st.header(" ".join(st.session_state.letters)) 

# 4. Game Input
word_input = st.text_input(f"Player {st.session_state.turn}, use the letters above:")

if st.button("End Turn"):
    if word_input:
        points = len(word_input)
        if st.session_state.turn == 1:
            st.session_state.s1 += points
            st.session_state.turn = 2
        else:
            st.session_state.s2 += points
            st.session_state.turn = 1
        
        # Refresh letters for the next player
        st.session_state.letters = random.sample(['ক', 'খ', 'গ', 'ঘ', 'চ', 'ছ', 'জ', 'ত', 'প', 'ল', 'স', 'ম', 'ন', 'র', 'অ', 'আ', 'ই'], 7)
        st.rerun()
