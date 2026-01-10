import streamlit as st
import requests
import random

# 1. Page Configuration for Mobile
st.set_page_config(page_title="H-J-B-R-L BD", page_icon="🎮", layout="centered")

# 2. Custom CSS for Wooden Scrabble Tiles
st.markdown("""
    <style>
    .tile-container { display: flex; justify-content: center; flex-wrap: wrap; margin-bottom: 20px; }
    .tile {
        background-color: #f3cf7a;
        color: #3d2b1f;
        padding: 15px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 28px;
        margin: 8px;
        border-bottom: 4px solid #b38b4d;
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Initialize Memory
if 's1' not in st.session_state:
    st.session_state.s1, st.session_state.s2, st.session_state.turn = 0, 0, 1
    st.session_state.letters = random.sample(['ক', 'খ', 'গ', 'ঘ', 'চ', 'ছ', 'জ', 'ত', 'প', 'ল', 'স', 'ম', 'ন', 'র', 'অ', 'আ'], 8)

# 4. Professional Scoreboard
st.title("𝐇-𝐉-𝐁-𝐑-𝐋 𝐁𝐃")
col1, col2 = st.columns(2)
col1.metric("Player 1", st.session_state.s1)
col2.metric("Player 2", st.session_state.s2)
st.write(f"### 👉 Player {st.session_state.turn}'s Turn")

# 5. Display Wooden Tiles
tiles_html = '<div class="tile-container">' + "".join([f'<div class="tile">{l}</div>' for l in st.session_state.letters]) + '</div>'
st.markdown(tiles_html, unsafe_allow_html=True)

# 6. Dictionary & Game Logic
@st.cache_data
def load_dict():
    url = "https://raw.githubusercontent.com/tahmid02016/bangla-wordlist/master/words.txt"
    return set(requests.get(url).text.split())

words_db = load_dict()
word_input = st.text_input("Enter your word:")

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
            st.session_state.letters = random.sample(['ক', 'খ', 'গ', 'ঘ', 'চ', 'ছ', 'জ', 'ত', 'প', 'ল', 'স', 'ম', 'ন', 'র', 'অ', 'আ'], 8)
            st.rerun()
    else:
        st.error("❌ Not in the dictionary.")
