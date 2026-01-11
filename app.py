import streamlit as st
import requests
import re
import unicodedata

# 1. THE INGESTION ENGINE (The "Consultant's Fix")
@st.cache_data
def ingest_lexicon():
    url = "https://raw.githubusercontent.com/MinhasKamal/BengaliDictionary/master/BengaliDictionary_17.txt"
    # We create a 'Set' for O(1) complexity—the gold standard for Scrabble
    lexicon = set()
    try:
        response = requests.get(url)
        for line in response.text.splitlines():
            # EXTRACT: Take only the first Bengali word before any brackets/spaces
            match = re.search(r'^([^\s\[\(\\]+)', line.strip())
            if match:
                word = match.group(1)
                # NORMALIZE: Ensure "দাগ" is the same in memory as on screen
                clean_word = unicodedata.normalize('NFC', word)
                lexicon.add(clean_word)
        return lexicon
    except Exception:
        return set()

# 2. THE VALIDATION LOGIC
st.title("🏛️ Enterprise Scrabble Validator")
valid_words = ingest_lexicon()

input_word = st.text_input("Submit Token:")

if input_word:
    # Match the input's encoding to the lexicon's encoding
    processed_input = unicodedata.normalize('NFC', input_word.strip())
    
    if processed_input in valid_words:
        st.success(f"TOKEN VALID: {processed_input}")
    else:
        st.error(f"TOKEN INVALID: {processed_input}")
