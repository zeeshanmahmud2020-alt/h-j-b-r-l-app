import streamlit as st
import unicodedata
import requests
import re

# --- THE POETIC SANITIZER ---
# We reduce the complexity of the world to its purest essence (NFC Normalization)
def canonical_form(text):
    if not text: return ""
    # Standardize Unicode: Unifies different ways of encoding the same glyph
    text = unicodedata.normalize('NFC', text.strip())
    # Remove 'ZWN' characters which act as invisible ghosts in the machine
    text = re.sub(r'[\u200d\u200c\ufeff]', '', text)
    return text

@st.cache_data
def load_and_purify():
    url = "https://raw.githubusercontent.com/MinhasKamal/BengaliDictionary/master/BengaliDictionary_17.txt"
    try:
        response = requests.get(url)
        # We transform the raw list into a 'Set' of pure forms for O(1) speed
        return {canonical_form(line.split()[0]) for line in response.text.splitlines() if line}
    except:
        return set()

# --- THE AESTHETIC INTERFACE ---
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>✧ The Bengali Lexicon ✧</h1>", unsafe_allow_html=True)

dictionary = load_and_purify()

# We design for the human: Large, centered, and inviting
word = st.text_input("Speak a word into the void:", placeholder="e.g., দাগ")

if word:
    pure_word = canonical_form(word)
    
    if pure_word in dictionary:
        st.markdown(f"<div style='padding:20px; border-radius:10px; background-color:#d4edda; color:#155724; text-align:center;'><b>{word}</b> is a masterpiece of the language. (VALID)</div>", unsafe_allow_html=True)
        st.balloons()
    else:
        st.markdown(f"<div style='padding:20px; border-radius:10px; background-color:#f8d7da; color:#721c24; text-align:center;'><b>{word}</b> exists outside the known scrolls. (INVALID)</div>", unsafe_allow_html=True)
