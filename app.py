if st.button("Confirm Move & End Turn"):
    if word_to_place:
        # 1. PREPARATION: Normalize and Tokenize
        target = unicodedata.normalize('NFC', word_to_place.strip())
        
        # 2. THE REFEREE: Check the Kamal Lexicon
        if target in lexicon:
            tiles = re.findall(r'[\u0980-\u09ff][\u09be-\u09cc\u09cd\u0981\u0982\u0983]*', target)
            
            # 3. PLACEMENT: Update the Board State
            for i, t in enumerate(tiles):
                r = row_idx + (i if orient == "Vertical" else 0)
                c = col_idx + (i if orient == "Horizontal" else 0)
                if r < 9 and c < 9: 
                    st.session_state.board[r][c] = t
            
            # 4. REWARD: Update Score and Swap Turn
            points = len(tiles)
            if st.session_state.turn == "Player 1":
                st.session_state.p1_score += points
                st.session_state.turn = "Player 2"
            else:
                st.session_state.p2_score += points
                st.session_state.turn = "Player 1"
            
            st.success(f"Valid Word! {points} points awarded.")
            st.rerun()
        else:
            # THE PENALTY: Block the turn
            st.error("❌ Invalid Word: Not found in dictionary. Turn not ended.")
