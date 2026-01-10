import streamlit as st
import requests
import unicodedata

# 1. THE RAW LINK (Crucial: uses raw.githubusercontent.com)
RAW_DICT_URL = "https://raw.githubusercontent.com/zeeshanmahmud2020-alt/h-j-b-r-l-app/main/requirements.txt"

@st.cache_resource
def load_dictionary():
    try:
        r = requests.get(RAW_DICT_URL, timeout=10)
        # Normalize the 450k words so the search is 100% accurate
        return set(unicodedata.normalize('NFC', w.strip()) for w in r.text.split())
    except Exception as e:
        st.error(f"Error loading words: {e}")
        return set()

WORDS_DB = load_dictionary()

# 2. THE SIMPLE SUBMIT (1D Style)
if st.button("🔥 SUBMIT WORD"):
    # Join tiles into a string
    played_word = "".join([m['char'] for m in st.session_state.turn_moves])
    # Normalize to match the dictionary format
    clean_word = unicodedata.normalize('NFC', played_word.strip())
    
    if clean_word in WORDS_DB:
        st.success(f"PASSED! '{clean_word}' found in requirements.txt")
        # Update score logic...
    else:
        st.error(f"REJECTED! '{clean_word}' is not in your list.")
        # Board wipe logic...
