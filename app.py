import streamlit as st
import unicodedata

# 1. ADVANCED NORMALIZER
def deep_rectify_bangla(text):
    if not text:
        return ""
    
    # Standardize numerical subscripts (0-9 -> ₀-₉)
    # This ensures "H2O" becomes "H₂O" for exact matching
    sub_map = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    text = text.translate(sub_map)
    
    # Normalize to NFC (Composed Form)
    # This unifies various ways of representing conjuncts and nuktas
    text = unicodedata.normalize('NFC', text)
    
    # Strip invisible control/rendering characters
    # \u200d = ZWJ, \u200c = ZWNJ, \ufeff = BOM
    invisible_chars = ['\u200d', '\u200c', '\ufeff', '\u200e', '\u200f']
    for char in invisible_chars:
        text = text.replace(char, '')
        
    # Rectify Khanda-Ta (U+09CE) variations
    text = text.replace('\u09a4\u09cd', '\u09ce')
    
    return text.strip()

# 2. STREAMLIT UI & SEARCH LOGIC
st.set_page_config(page_title="Bangla Deep Search 2026")

# Inject Noto Sans Bengali for correct rendering of subscripts
st.markdown("""
    <style>
    @import url('fonts.googleapis.com');
    * { font-family: 'Noto Sans Bengali', sans-serif !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🔎 Bangla Advanced Dictionary Search")
st.info("Feature: Auto-handles numerical subscripts and complex conjuncts.")

search_query = st.text_input("Enter Bangla word or chemical formula (e.g., H2O):")

if search_query:
    target = deep_rectify_bangla(search_query)
    found = False
    
    try:
        # 'utf-8-sig' ignores potential BOM markers in words.txt
        with open('words.txt', 'r', encoding='utf-8-sig') as f:
            for line in f:
                clean_line = deep_rectify_bangla(line)
                
                if target == clean_line:
                    st.success(f"✅ Found: **{line.strip()}**")
                    found = True
                    break
        
        if not found:
            st.warning("❌ Word not found. Checking for byte-level mismatches...")
            # Debugging tool: Shows the user exactly what bytes are being searched
            st.code(f"Search Target (Hex): {[hex(ord(c)) for c in target]}")
            
    except FileNotFoundError:
        st.error("Missing words.txt file. Please upload it to the directory.")

