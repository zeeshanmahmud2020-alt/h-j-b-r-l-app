import streamlit as st
import requests
import unicodedata
import re

# --- THE BENGALI FILTER (The "King Akbar" Extraction) ---
@st.cache_data
def load_purified_lexicon():
    url = "https://raw.githubusercontent.com/MinhasKamal/BengaliDictionary/master/BengaliDictionary_17.txt"
    lexicon = set()
    try:
        response = requests.get(url)
        for line in response.text.splitlines():
            # Concept: Extract ONLY characters in the Bengali Unicode range (\u0980-\u09FF)
            # This ignores all English words, pipes, and dots automatically.
            bengali_words = re.findall(r'[\u0980-\u09ff]+', line)
            
            for word in bengali_words:
                # Normalize and add to our 'Source of Truth'
                clean_word = unicodedata.normalize('NFC', word)
                if len(clean_word) > 1:  # Ignore single modifiers
                    lexicon.add(clean_word)
        return lexicon
    except Exception as e:
        st.error(f"Ingestion Fault: {e}")
        return set()

# --- THE INTERFACE ---
st.title("🏛️ The Purified Bengali Scrabble Lexicon")

lexicon = load_purified_lexicon()

if lexicon:
    st.info(f"System Ready. {len(lexicon)} unique Bengali words ingested.")
    word_input = st.text_input("Enter word for validation (e.g., বল, দাগ, দায়িত্বশীল):")

    if word_input:
        target = unicodedata.normalize('NFC', word_input.strip())
        if target in lexicon:
            st.success(f"✅ VALID: {target}")
        else:
            st.error(f"❌ INVALID: {target}")
