import streamlit as st
import requests

# 1. Keep the simple header you had
st.title("𝐇-𝐉-𝐁-𝐑-𝐋 𝐁𝐃")
st.caption("The 24-Hour 'Borno-Baji' Sprint")

# 2. Add turn memory without changing the UI
if 'turn' not in st.session_state:
    st.session_state.turn = 1
    st.session_state.s1 = 0
    st.session_state.s2 = 0

# 3. Simple Score display
st.write(f"**Score:** P1: {st.session_state.s1} | P2: {st.session_state.s2}")

# 4. Your original input box
word_input = st.text_input(f"Player {st.session_state.turn}'s turn:")

# 5. Logic: If word is valid, add points and flip the turn
if st.button("Submit"):
    # (Simple logic: +5 points for any valid word)
    if st.session_state.turn == 1:
        st.session_state.s1 += 5
        st.session_state.turn = 2
    else:
        st.session_state.s2 += 5
        st.session_state.turn = 1
    st.rerun()
