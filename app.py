import streamlit as st

# --- INITIALIZE GAME STATE ---
if 'player1_score' not in st.session_state:
    st.session_state.player1_score = 0
if 'player2_score' not in st.session_state:
    st.session_state.player2_score = 0
if 'current_turn' not in st.session_state:
    st.session_state.current_turn = "Player 1"

# --- SCOREBOARD UI ---
st.sidebar.title("🏆 Scoreboard")
st.sidebar.metric("Player 1", f"{st.session_state.player1_score} pts")
st.sidebar.metric("Player 2", f"{st.session_state.player2_score} pts")
st.sidebar.write(f"**Current Turn:** {st.session_state.current_turn}")

# --- THE SWAP & SUBMIT LOGIC ---
if st.button("End Turn & Validate Word"):
    # 1. Logic to read the board and validate word goes here
    # 2. Add points based on the word found
    # 3. Swap players
    if st.session_state.current_turn == "Player 1":
        st.session_state.current_turn = "Player 2"
    else:
        st.session_state.current_turn = "Player 1"
    st.rerun()

if st.button("Reset Game"):
    st.session_state.board = [["" for _ in range(9)] for _ in range(9)]
    st.session_state.player1_score = 0
    st.session_state.player2_score = 0
    st.rerun()
