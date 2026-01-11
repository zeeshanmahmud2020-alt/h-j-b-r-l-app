# --- IMPROVED REFEREE LOGIC ---
if st.button("Confirm Move & End Turn"):
    if word_to_place:
        # 1. Clean and Normalize
        user_word = unicodedata.normalize('NFC', word_to_place.strip())
        
        # 2. Check for exact match OR a common variation
        if user_word in lexicon:
            # ... (Your existing placement logic) ...
            st.success(f"Perfect! '{user_word}' is valid.")
            st.rerun()
        else:
            # 3. HELPER: Show the user what IS in the dictionary
            # This looks for words that START with what you typed
            suggestions = [w for w in lexicon if w.startswith(user_word[:2])][:3]
            st.error(f"❌ '{user_word}' not found.")
            if suggestions:
                st.info(f"Did you mean: {', '.join(suggestions)}?")
