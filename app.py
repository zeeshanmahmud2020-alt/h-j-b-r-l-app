import streamlit as st
import random

# ... (CSS and State Setup remain the same) ...

# NEW: Track coordinates of tiles placed THIS turn
if 'turn_coords' not in st.session_state: 
    st.session_state.turn_coords = []

# 4. THE BOARD (Placement Logic)
for r in range(11):
    cols = st.columns(11)
    for c in range(11):
        val = st.session_state.board[r][c]
        if cols[c].button(val if val else " ", key=f"b_{r}_{c}"):
            if st.session_state.sel_idx is not None:
                char, pts = st.session_state.hand[st.session_state.sel_idx]
                
                # Update Board and Memory
                st.session_state.board[r][c] = char
                st.session_state.current_move.append(char)
                st.session_state.turn_coords.append((r, c)) # Remember this spot!
                
                st.session_state.hand[st.session_state.sel_idx] = random.choice(POOL)
                st.session_state.sel_idx = None
                st.rerun()

# 6. THE SMART SUBMIT
word = "".join(st.session_state.current_move)
if st.button("🔥 SUBMIT WORD", use_container_width=True, type="primary"):
    if word in WORDS_DB:
        # SUCCESS: Lock them in and clear the turn memory
        st.session_state.scores[st.session_state.turn] += len(word)
        st.session_state.turn = "P2" if st.session_state.turn == "P1" else "P1"
        st.session_state.current_move = []
        st.session_state.turn_coords = [] 
        st.success(f"'{word}' Accepted!")
        st.rerun()
    else:
        # FAILURE: Wipe ONLY the letters from this turn
        for r, c in st.session_state.turn_coords:
            st.session_state.board[r][c] = ""
        
        st.session_state.current_move = []
        st.session_state.turn_coords = []
        st.error(f"'{word}' is invalid. Board cleaned!")
        st.rerun()
