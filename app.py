import streamlit as st
import requests
import unicodedata
import re

# --- 1. THE ARCHITECT'S ENGINE: DATA INGESTION & PURIFICATION ---
@st.cache_data
def load_authoritative_lexicon():
    # Fetching the raw truth from the repository
    url = "https://raw.githubusercontent.com/MinhasKamal/BengaliDictionary/master/BengaliDictionary_17.txt"
    lexicon = set()
    try:
        response = requests.get(url)
        for line in response.text.splitlines():
            # Regex: Extract only the Bengali script, ignoring English/Pipes
            found_words = re.findall(r'[\u0980-\u09ff]+', line)
            for word in found_words:
                clean = unicodedata.normalize('NFC', word)
                if len(clean) > 1: lexicon.add(clean)
        return lexicon
    except:
        return set()

# --- 2. THE LINGUISTIC ENGINE: GRAPHEME CLUSTERING ---
def get_akshara_tiles(word):
    # This keeps 'দা' together as one tile instead of 'দ' + 'া'
    cluster_pattern = r'[\u0985-\u09b9\u09ce\u09dc-\u09df][\u09be-\u09cc\u09cd\u0981\u0982\u0983]*|[\u0985-\u0994]'
    return re.findall(cluster_pattern, word)

# --- 3. THE ECONOMIC ENGINE: SCORING ---
BENGALI_TILES = {
    'ক': 1, 'ব': 1, 'ল': 1, 'ন': 1, 'ম': 1, 'প': 1, 'র': 1, 'স': 1, 'ত': 1, 'া': 1, 'ি': 1,
    'গ': 2, 'দ': 2, 'চ': 2, 'জ': 2, 'হ': 2, 'ু': 2, 'ে': 2, 'ো': 2,
    'খ': 3, 'ট': 3, 'ড': 3, 'থ': 3, 'ফ': 3, 'ী': 3, 'ূ': 3,
    'ঘ': 5, 'ঝ': 5, 'ঠ': 5, 'ঢ': 5, 'ভ': 5, 'ষ': 5, 'ঙ': 5, 'ঞ': 5,
    'য': 8, 'র': 8, 'ৎ': 10, 'ঃ': 10, 'ঁ': 10, 'য়': 10
}

def calculate_score(tiles):
    # Base score of the first character of each tile + 1 bonus for the vowel/modifier
    score = 0
    for tile in tiles:
        base = tile[0]
        points = BENGALI_TILES.get(base, 1)
        if len(tile) > 1: points += 1
        score += points
    return score

# --- 4. THE INTERFACE: STREAMLIT ---
st.set_page_config(page_title="Bengali Scrabble Master", page_icon="🏛️")
st.title("🏛️ Bengali Scrabble Authority")

lexicon = load_authoritative_lexicon()

if not lexicon:
    st.error("System Failure: Could not reach the Lexicon.")
else:
    st.info(f"Connected. {len(lexicon)} words validated.")
    user_input = st.text_input("Place a Word:", placeholder="e.g. দায়িত্বশীল").strip()

    if user_input:
        target = unicodedata.normalize('NFC', user_input)
        if target in lexicon:
            tiles = get_akshara_tiles(target)
            score = calculate_score(tiles)
            
            st.success(f"### ✅ VALID WORD")
            col1, col2 = st.columns(2)
            col1.metric("Points", f"{score}")
            col2.write("**Tiles:**")
            col2.write(tiles)
        else:
            st.error("❌ INVALID WORD: Not in the sacred scrolls.")
