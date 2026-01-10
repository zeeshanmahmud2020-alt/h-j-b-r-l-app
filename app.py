import streamlit as st
import requests

# 1. Access the CORRECT file
@st.cache_resource
def load_dict():
    # CHANGE THIS to the raw link of your new ID file
    url = "https://raw.githubusercontent.com/username/repo/main/dictionary.txt"
    try:
        r = requests.get(url, timeout=5)
        # Load the English IDs into memory
        return set(w.strip().upper() for w in r.text.split())
    except Exception as e:
        st.error(f"Failed to load dictionary: {e}")
        return set()

WORDS_DB = load_dict()

# 2. The Validation Bridge
# This translates the tiles you played into the ID format stored in dictionary.txt
if st.button("🔥 SUBMIT WORD"):
    # Translate the board move using your TILE_MAP
    attempted_id = "".join([TILE_MAP.get(m['char'], '') for m in st.session_state.turn_moves]).upper()
    
    if attempted_id in WORDS_DB:
        st.success(f"Audit Passed: {attempted_id} is a valid word!")
        # Proceed to update score...
    else:
        st.error(f"Audit Failed: {attempted_id} not in dictionary.")
        # Wipe board...
