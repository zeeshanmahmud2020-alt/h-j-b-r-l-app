import streamlit as st
import requests

# 1. Title & Style
st.set_page_config(page_title="H-J-B-R-L", page_icon="🎮")
st.title("𝐇-𝐉-𝐁-𝐑-𝐋 🇧🇩")
st.caption("The 24-Hour 'Borno-Baji' Sprint")

# 2. The Brain: Load 450,000+ words from GitHub
@st.cache_data
def load_dictionary():
    url = "https://raw.githubusercontent.com/tahmid02016/bangla-wordlist/master/words.txt"
    try:
        r = requests.get(url)
        return set(r.text.split())
    except:
        return {"কাকা", "মা", "বাবা"} # Fallback if offline

words_db = load_dictionary()

# 3. The Numerical Assignments (Scoring)
POINTS = {
    'ক্ষ': 10, 'জ্ঞ': 10, 'ঞ্চ': 10, 'স্ত': 8,
    'খ': 5, 'ঘ': 5, 'ছ': 5, 'ঝ': 8, 'ঙ': 10,
    'অ': 1, 'আ': 1, 'ই': 1, 'উ': 1, 'এ': 1,
    'ক': 1, 'ন': 1, 'র': 1, 'স': 1, 'ল': 1
}

# 4. The Game UI
word_input = st.text_input("Enter a word to score:", placeholder="যেমন: ক্ষণ")

if word_input:
    # Logic: Check if word is real
    if word_input in words_db:
        # Calculate score: sum of points or default 1
        score = sum(POINTS.get(char, 1) for char in word_input)
        st.success(f"✅ '{word_input}' is a valid word!")
        st.metric(label="Scrabble Points", value=score)
        
        if score > 15:
            st.balloons()
            st.write("💥 High score! You're a word master.")
    else:
        st.error(f"❌ '{word_input}' not found in the dictionary.")

st.divider()
st.info("Tip: Use complex Juktoborno like 'ক্ষ' for massive points!")