import streamlit as st
import unicodedata
import requests

# 1. ADVANCED NORMALIZER
def deep_rectify_bangla(text):
    if not text:
        return ""
    # Standardize numerical subscripts (0-9 -> ₀-₉)
    sub_map = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    text = text.translate(sub_map)
    # Normalize and strip invisible chars
    text = unicodedata.normalize('NFC', text)
    invisible_chars = ['\u200d', '\u200c', '\ufeff', '\u200e', '\u200f']
    for char in invisible_chars:
        text = text.replace(char, '')
    # Rectify Khanda-Ta
    text = text.replace('\u09a4\u09cd', '\u09ce')
    return text.strip()

# 2. DATA LOADING (From GitHub)
@st.cache_data
def load_dictionary():
    url = "https://raw.githubusercontent.com/MinhasKamal/BengaliDictionary/master/BengaliDictionary_17.txt"
    response = requests.get(url)
    if response.status_code == 200:
        # Split by lines and clean them
        return response.text.splitlines()
    return []

# 3. STREAMLIT UI
st.set_page_config(page_title="Bangla Deep Search 2026")

st.title("🔎 Bangla Advanced Dictionary Search")
words = load_dictionary()

if not words:
    st.error("Failed to load the word list from GitHub.")
else:
    search_query = st.text_input("Enter Bangla word:")

    if search_query:
        target = deep_rectify_bangla(search_query)
        found = False
        
        # Search through the loaded list
        for word in words:
            if target == deep_rectify_bangla(word):
                st.success(f"✅ Found: **{word.strip()}**")
                found = True
                break
        
        if not found:
            st.warning("❌ Word not found.")
            st.code(f"Search Target (Hex): {[hex(ord(c)) for c in target]}")
