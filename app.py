import streamlit as st
import unicodedata
import requests

# 1. ADVANCED NORMALIZER (Required for Bangla script matching)
def deep_rectify_bangla(text):
    if not text: return ""
    text = unicodedata.normalize('NFC', text)
    invisible_chars = ['\u200d', '\u200c', '\ufeff', '\u200e', '\u200f']
    for char in invisible_chars:
        text = text.replace(char, '')
    return text.strip()

# 2. DATA LOADING (Optimized with Caching)
@st.cache_data
def load_scrabble_dictionary():
    url = "https://raw.githubusercontent.com/MinhasKamal/BengaliDictionary/master/BengaliDictionary_17.txt"
    try:
        response = requests.get(url)
        # Convert the list into a 'set' for lightning-fast Scrabble lookups
        raw_words = response.text.splitlines()
        return {deep_rectify_bangla(w) for w in raw_words if w.strip()}
    except:
        return set()

# 3. SCRABBLE UI
st.set_page_config(page_title="Bangla Scrabble Checker", page_icon="📝")
st.title("📝 Bangla Scrabble Word Validator")

scrabble_dict = load_scrabble_dictionary()

if not scrabble_dict:
    st.error("Could not load dictionary. Please check your internet connection.")
else:
    word_input = st.text_input("Enter word to validate:", placeholder="যেমন: অমর", help="Type a word to see if it's in the Scrabble dictionary.")

    if word_input:
        processed_input = deep_rectify_bangla(word_input)
        
        if processed_input in scrabble_dict:
            st.balloons()
            st.success(f"### ✅ VALID WORD: **{word_input}**")
            st.info("This word is in the official list and can be used in your game.")
        else:
            st.error(f"### ❌ INVALID WORD: **{word_input}**")
            st.warning("This word was not found in the dictionary.")


