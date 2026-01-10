# --- Updated Validation Logic ---
if col_a.button("🔥 SUBMIT WORD", use_container_width=True, type="primary"):
    # 1. Join the tiles placed this turn
    played_word = "".join([m['char'] for m in st.session_state.turn_moves])
    # 2. Normalize to handle Bangla Unicode correctly
    clean_word = unicodedata.normalize('NFC', played_word)
    
    # 3. Check against the real Dictionary
    if clean_word in WORDS_DB:
        points = len(clean_word)
        # Add points and switch turn
        if st.session_state.turn == 1: st.session_state.s1 += points
        else: st.session_state.s2 += points
        
        st.session_state.hand = [get_random_tile() if t=="Used" else t for t in st.session_state.hand]
        st.session_state.turn = 2 if st.session_state.turn == 1 else 1
        st.session_state.turn_moves = []
        st.success(f"সঠিক শব্দ: {clean_word}")
        st.rerun()
    else:
        # FAILED: The word isn't real, so clear the board (Self-Healing)
        for m in st.session_state.turn_moves:
            st.session_state.board[m['r']][m['c']] = ""
        # Put the tiles back in the hand
        st.session_state.hand = [get_random_tile() if t=="Used" else t for t in st.session_state.hand]
        st.session_state.turn_moves = []
        st.error(f"'{clean_word}' কোনো বৈধ শব্দ নয়!")
