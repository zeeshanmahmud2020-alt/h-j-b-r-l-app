import streamlit as st
import requests
import random

# 1. Setup
st.set_page_config(page_title="H-J-B-R-L BD", layout="centered")

# 2. UI Styling
st.markdown("""
    <style>
    .tile-container { display: flex; justify-content: center; margin-bottom: 10px; }
    .tile {
        background-color: #f3cf7a; color: #3d2b1f; padding: 10px;
        border-radius: 8px; font-weight: bold; font-size: 24px;
        margin: 5px; border-bottom: 4px solid #b38b4d;
        width: 50px; height: 50px; display: flex;
        align-items: center; justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Logic & Vowels
POOL = ['ক', 'খ', 'গ', 'ঘ', 'চ', 'ছ', 'জ', 'ত', 'দ', 'ন', 'প', 'ব', 'ম', 'র', 'ল', 'স', 'হ', 
        'অ', 'আ', 'ই', 'উ', 'এ', 'ও', 'া', 'ি', 'ী', 'ু', 'ূ', 'ে', 'ৈ', 'ো', 'ৌ']

if 's1' not in st.session_state:
    st.session_state.update({'s1':0, 's2':0, 'turn':1, 'input_val':"", 'letters':random.sample(POOL, 7)})

# 4. Display
st.title("𝐇-𝐉-𝐁-𝐑-𝐋 𝐁𝐃")
st.write(f"**P1:** {st.session_state.s1} | **P2:** {st.session_state.s2} — **Player {st.session_state.turn}'s Turn**")

# Show tiles visually
tiles_html = '<div class="tile-container">' + "".join([f'<div class="tile">{l}</div>' for l in st.session_state.letters]) + '</div>'
st.markdown(tiles_html, unsafe_allow_html=True)

# Make letters clickable via buttons
st.write("Click to type:")
cols = st.columns(7)
for i, l in enumerate(st.session_state.letters):
    if cols[i].button(l, key=f"btn_{i}"):
        st.session_state.input_val += l

# 5. Validation Logic
@st.cache_data
def load_dict():
    return set(requests.get("https://raw.githubusercontent.com/tahmid02016/bangla-wordlist/master/words.txt").text.split())

words_db = load_dict()
word_input = st.text_input("Your Word:", value=st.session_state.input_val)

if st.button("Submit Move", type="primary"):
    # Check if word is in Dictionary AND letters are in Hand
    in_dict = word_input in words_db
    in_hand = all(word_input.count(char) <= st.session_state.letters.count(char) for char in word_input)
    
    if in_dict and in_hand:
        points = len(word_input)
        if st.session_state.turn == 1: st.session_state.s1 += points
        else: st.session_state.s2 += points
        
        # Reset turn
        st.session_state.turn = 2 if st.session_state.turn == 1 else 1
        st.session_state.letters = random.sample(POOL, 7)
        st.session_state.input_val = ""
        st.rerun()
    elif not in_hand:
        st.error("❌ Use ONLY the letters provided in your hand!")
    else:
        st.error("❌ Not a valid Bengali word.")

if st.button("Clear Input"):
    st.session_state.input_val = ""
    st.rerun()
