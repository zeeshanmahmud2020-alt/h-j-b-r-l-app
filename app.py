import streamlit as st
import requests
import random

# 1. Page Config
st.set_page_config(page_title="H-J-B-R-L BD", page_icon="🎮", layout="centered")

# 2. UI Styling
st.markdown("""
    <style>
    .tile-container { display: flex; justify-content: center; flex-wrap: wrap; margin-bottom: 20px; }
    .tile {
        background-color: #f3cf7a; color: #3d2b1f; padding: 15px;
        border-radius: 8px; font-weight: bold; font-size: 28px;
        margin: 8px; border-bottom: 4px solid #b38b4d;
        width: 65px; height: 65px; display: flex;
        align-items: center; justify-content: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Game Memory
POOL = ['ক', 'খ', 'গ', 'ঘ', 'চ', 'ছ', 'জ', 'ত', 'দ', 'ন', 'প', 'ব', 'ম', 'র', 'ল', 'স', 'হ', 
        'অ', 'আ', 'ই', 'উ', 'এ', 'ও', 'া', 'ি', 'ী', 'ু', 'ূ', 'ে', 'ৈ', 'ো', 'ৌ']

if 's1' not in st.session_state:
    st.session_state.s1, st.session_state.s2, st.session_state.turn = 0, 0, 1
    st.session_state.letters = random.sample(POOL, 10)
    st.session_state.input_val = ""

# 4. Scoreboard
st.title("𝐇-𝐉-𝐁-𝐑-𝐋 𝐁𝐃")
c1, c2 = st.columns(2)
c1.metric("Player 1", st.session_state.s1)
c2.metric("Player 2", st.session_state.s2)
st.write(f"### 👉 Player {st.session_state.turn}'s Turn")

# 5. Wooden Tiles
tiles_html = '<div class="tile-container">' + "".join([f'<div class="tile">{l}</div>' for l in st.session_state.letters]) + '</div>'
st.markdown(tiles_html, unsafe_allow_html=True)

# 6. Special Character Buttons
st.write("Special Characters (Click to add):")
sc1, sc2, sc3, sc4 = st.columns(4)
if sc1.button("্ (Hasant)"): st.session_state.input_val += "্"
if sc2.button("ঁ (Chandrabindu)"): st.session_state.input_val += "ঁ"
if sc3.button("ং (Anusvar)"): st.session_state.input_val += "ং"
if sc4.button("ঃ (Visarga)"): st.session_state.input_val += "ঃ"

# 7. Validation Logic
@st.cache_data
def load_dict():
    url = "https://raw.githubusercontent.com/tahmid02016/bangla-wordlist/master/words.txt"
    return set(requests.get(url).text.split())

words_db = load_dict()
word_input = st.text_input("Type your word here:", value=st.session_state.input_val)

if st.button("Submit Move"):
    if word_input in words_db:
        points = len(word_input)
        if st.session_state.turn == 1:
            st.session_state.s1 += points
            st.session_state.turn = 2
        else:
            st.session_state.s2 += points
            st.session_state.turn = 1
        st.session_state.letters = random.sample(POOL, 10)
        st.session_state.input_val = ""
        st.rerun()
    else:
        st.error("❌ Invalid word!")

if st.sidebar.button("Reset Game"):
    st.session_state.clear()
    st.rerun()
