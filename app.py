# Use a container for the board to keep it visually separate from UI logic
board_container = st.container()

with board_container:
    for r in range(11):
        cols = st.columns(11)
        for c in range(11):
            tile_label = st.session_state.board[r][c] or " "
            # If a tile is clicked and one is selected from the rack, place it
            if cols[c].button(tile_label, key=f"b_{r}_{c}"):
                if st.session_state.sel_idx is not None:
                    char, pts = st.session_state.hand[st.session_state.sel_idx]
                    st.session_state.board[r][c] = char
                    st.session_state.placed_tiles.append(pts)
                    # Replace used tile in hand
                    st.session_state.hand[st.session_state.sel_idx] = random.choice(TILES)
                    st.session_state.sel_idx = None
                    st.rerun()
