import streamlit as st
import requests
import unicodedata

# --- THE AUDITOR ---
@st.cache_data
def load_and_audit_lexicon():
    url = "https://raw.githubusercontent.com/MinhasKamal/BengaliDictionary/master/BengaliDictionary_17.txt"
    lexicon = set()
    try:
        response = requests.get(url)
        lines = response.text.splitlines()
        for line in lines:
            if not line.strip(): continue
            
            # THE FIX: Split by space or tab and take the very first part
            # This handles "বল [বিশেষ্য]" -> "বল"
            raw_word = line.split()[0]
            
            # NORMALIZE: Force it into NFC
            clean_word = unicodedata.normalize('NFC', raw_word.strip())
            lexicon.add(clean_word)
            
        return lexicon
    except:
        return set()

# --- THE INTERFACE ---
st.title("🏛️ Scrabble Logic Diagnostic")

lexicon = load_and_audit_lexicon()

user_word = st.text_input("Enter test word (e.g., বল or দাগ):")

if user_word:
    # Normalize user input to match the lexicon's "Uniform"
    clean_input = unicodedata.normalize('NFC', user_word.strip())
    
    if clean_input in lexicon:
        st.success(f"MATCH FOUND: {clean_input}")
    else:
        st.error(f"NO MATCH: {clean_input}")
        
        # THE DIAGNOSTIC: Show the bytes. This is the "King Akbar" level of truth.
        st.write("Diagnostic - Your Input Hex:")
        st.code([hex(ord(c)) for c in clean_input])
        
        # Show a sample of the lexicon to see why it's failing
        st.write("Sample of loaded words (First 5):")
        st.code(list(lexicon)[:5])
