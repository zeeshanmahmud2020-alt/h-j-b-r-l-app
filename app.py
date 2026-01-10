import streamlit as st
import requests
import random

# 1. Initialize Memory FIRST
if 's1' not in st.session_state:
    st.session_state.s1 = 0
    st.session_state.s2 = 0
    st.session_state.turn = 1
    # Initial set of letters
    st.session_state.letters = random.sample(['ক', 'খ', 'গ', 'ঘ', 'চ', 'ছ', 'জ', 'ত', 'প', 'ল', 'স', 'ম', 'ন', 'র', 'অ', 'আ'], 8)

# 2. UI Header
st.title("𝐇-𝐉-𝐁-𝐑-𝐋 𝐁𝐃")
st.write(f"**Score:** P1: {st.session_state.s1} | P2: {st.session_state.s2}")
st.divider()

# 3. The Letter Bank
st.subheader("Your Letters:")
st.header(" ".join(st.session_state.letters))

# 4. Load Dictionary
@st.cache_data
def load_dictionary():
    url = "https://raw.githubusercontent.com/tahmid02016/bangla-wordlist/master/words.txt"
    try:
        r = requests.get(url)
        return set(r.text.split())
    except:
        return {"কাকা", "মা", "বাবা"}

words_db = load_dictionary()

# 5. Game Input
word_input = st.text_input(f"Player {st.session_state.turn}, enter your word:")

if word_input:
    if word_input in words_db:
        st.success(f"✅ '{word_input}' is a valid word!")
        if st.button("Submit Move"):
            points = len(word_input)
            if st.session_state.turn == 1:
                st.session_state.s1 += points
                st.session_state.turn = 2
            else:
                st.session_state.s2 += points
                st.session_state.turn = 1
            # Refresh letters for next turn
            st.session_state.letters = random.sample(['ক', 'খ', 'গ', 'ঘ', 'চ', 'ছ', 'জ', 'ত', 'প', 'ল', 'স', 'ম', 'ন', 'র', 'অ', 'আ'], 8)
            st.rerun()
    else:
        st.error("❌ Word not in dictionary. Try again!")
