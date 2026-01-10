import streamlit as st
import unicodedata

# --- 1. ADVANCED NORMALIZER & RECTIFIER ---
def deep_rectify_bangla(text):
    if not text:
        return ""
    
    # Map standard digits to Unicode Subscripts (₀-₉)
    sub_map = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    text = text.translate(sub_map)
    
    # Normalize to NFC (Standardizes conjuncts/nuktas)
    text = unicodedata.normalize('NFC', text)
    
    # Strip invisible markers (ZWJ/ZWNJ/BOM) that cause search failure
    invisible_chars = ['\u200d', '\u200c', '\ufeff', '\u200e', '\u200f']
    for char in invisible_chars:
        text = text.replace(char, '')
        
    # Rectify Khanda-Ta variations
    text = text.replace('\u09a4\u09cd', '\u09ce')
    
    return text.strip()

# --- 2. PERFORMANCE OPTIMIZATION FOR 400K WORDS ---
@st.cache_data
def load_and_index_dictionary(file_path):
    """Loads file into a Set for O(1) instant pinpointing."""
    vocab_set = set()
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            for line in f:
                cleaned = deep_rectify_bangla(line)
                if cleaned:
                    vocab_set.add(cleaned)
        return vocab_set
    except FileNotFoundError:
        return None

# --- 3. UI CONFIGURATION & CSS INJECTION ---
st.set_page_config(page_title="Bangla Deep Search 2026", layout="centered")

# CSS to: 1. Use Noto Sans, 2. Disable clickable dictionary links
st.markdown("""
    <style>
    @import url('fonts.googleapis.com');
    * { font-family: 'Noto Sans Bengali', sans-serif !important; }
    
    /* STOP REDIRECTS: Disables all click/link interactions on text results */
    .stCode, .stMarkdown, .element-container {
        pointer-events: none !important;
        cursor: default !important;
    }
    .stTextInput { pointer-events: auto !important; } /* Allow typing */
    </style>
""", unsafe_allow_html=True)

# --- 4. MAIN APP INTERFACE ---
st.title("🔎 Advanced Bangla Search")
st.write("Ensures exact pinpointing for complex words and chemical subscripts.")

# Load the 400k word dictionary
vocab = load_and_index_dictionary('words.txt')

if vocab is None:
    st.error("⚠️ 'words.txt' not found! Please upload it to your GitHub repository.")
else:
    search_query = st.text_input("Search (e.g., H2O or complex conjuncts):")

    if search_query:
        target = deep_rectify_bangla(search_query)
        
        # Instant lookup in our optimized Set
        if target in vocab:
            st.write("### ✅ Exact Match Found")
            # Use st.code to display text in a non-clickable, raw format
            st.code(target, language=None)
        else:
            st.warning("❌ Word not found in the 400,000 word dataset.")
            # Debugging Hex codes for pinpointing errors
            with st.expander("Show Byte-Level Debugging"):
                st.write(f"Normalized Search Hex: {[hex(ord(c)) for c in target]}")

# --- 5. FOOTER ---
st.caption("2026 Rectified Version | Numerical Subscripts Enabled")
