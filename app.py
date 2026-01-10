import streamlit as st
import requests
import random

# 1. THE SOUL: Fast, Tight Layout
st.set_page_config(page_title="হ য ব র ল", layout="centered")

@st.cache_resource # Only download the dictionary ONCE (Crucial for playability)
def load_dict():
    url = "https://raw.githubusercontent.com/tahmid02016/bangla-wordlist/master/words.txt"
    try:
        words = set(requests.get(url).text.split())
        return words
    except:
        return {"কাকা", "বাবা", "মা", "নাম"} # Fallback

WORDS_DB = load_dict()

st.markdown("""
    <style>
    .block-container { max-width: 500px !important; padding: 1rem !important; }
    
    /* Authentic Wooden Tiles */
    div.stButton > button { 
        background-color: #f3cf7a !important; color: #3d2b1f !important; 
        font-weight: bold !important; font-size: 24px !important;
        border-radius: 8px !important; border-bottom: 5px solid #b38b4d !important;
        width: 100% !important; height: 65px !important; margin: 0px !important;
    }
    
    /* Display Area */
    .main-word { 
        font-size: 60px; text-align: center; color: #f1c40f; 
        background: #1e272e; border: 3px solid #34495e;
        border-radius: 15px; margin: 10px 0; min-height: 80px;
    }

    /* Scoreboard */
    .sb { display: flex; justify-content: space-between; font-size: 20px; font-weight: bold; }
    .active { color: #00d2ff; text-decoration: underline; }
    </style>
    """, unsafe_allow_html=True)

# 2. State Setup
POOL = ['ক', 'খ', 'গ', 'ঘ', 'চ', 'ছ', 'জ', 'ত', 'দ', 'ন', 'প', 'ব', 'ম', 'র', 'ল', 'স', 'হ', 'া', 'ি', 'ু', 'ে', 'ো', 'ং', '্']
if 's1' not in st.session_state:
    st.session_state.update({'s1':0, 's2':0, 'turn':1, 'word':"", 'letters':random.sample(POOL, 7)})

# 3. Scoreboard & UI
turn = st.session_state.turn
st.markdown(f"""
<div class="sb">
    <div class="{'active' if turn==1 else ''}">P1: {st.session_state.s1}</div>
    <div class="{'active' if turn==2 else ''}">P2: {st.session_state.s2}</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"<div class='main-word'>{st.session_state.word}</div>", unsafe_allow_html=True)

# 4. Interactive Tiles
cols = st.columns(7)
for i, l in enumerate(st.session_state.letters):
    if cols[i].button(l, key=f"t_{i}"):
        st.session_state.word += l
        st.rerun()

# 5. Logic Controls
st.write("---")
c1, c2, c3 = st.columns([2, 1, 1])

if c1.button("🔥 SUBMIT", use_container_width=True, type="primary"):
    if st.session_state.word in WORDS_DB:
        pts = len(st.session_state.word)
        if st.session_state.turn == 1: st.session_state.s1 += pts
        else: st.session_state.s2 += pts
        
        st.session_state.turn = 2 if st.session_state.turn == 1 else 1
        st.session_state.letters = random.sample(POOL, 7)
        st.session_state.word = ""
        st.toast("Valid Word!")
        st.rerun()
    else:
        st.error("Not in dictionary!")

if c2.button("🔙 Del", use_container_width=True):
    st.session_state.word = st.session_state.word[:-1]
    st.rerun()

if c3.button("🔄 Swap", use_container_width=True):
    st.session_state.turn = 2 if st.session_state.turn == 1 else 1
    st.session_state.letters = random.sample(POOL, 7)
    st.session_state.word = ""
    st.rerun()
