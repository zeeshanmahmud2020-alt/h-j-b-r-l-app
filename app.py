import streamlit as st
import random

# 1. Unique "Safety" Styling
st.markdown("""
    <style>
    .board-cell { width: 40px; height: 40px; border: 1px solid #444; text-align: center; line-height: 40px; border-radius: 4px; }
    .bonus-3w { background-color: #ff9f43; color: white; } /* Unique Orange instead of Red */
    .bonus-2w { background-color: #54a0ff; color: white; } /* Unique Blue instead of Pink */
    </style>
    """, unsafe_allow_html=True)

# 2. Logic: Syllable Bag with Numbering
CONSONANTS = {'ক': 1, 'ম': 1, 'প': 2, 'ব': 2, 'ঘ': 8, 'ঙ': 10}
MATRAS = {'': 0, 'া': 1, 'ি': 2, 'ু': 3, 'ে': 4, 'ো': 5}

@st.cache_resource
def get_safe_bag():
    bag = []
    for c, cp in CONSONANTS.items():
        for m, mp in MATRAS.items():
            bag.append((c + m, cp + mp))
    return bag

if 'hand' not in st.session_state:
    st.session_state.hand = random.sample(get_safe_bag(), 7)

# 3. The 13x13 Board (Avoiding the 15x15 Scrabble Trademark)
st.title("𝐇-𝐉-𝐁-𝐑-𝐋 𝐏𝐑𝐎")
st.write("### Game Board (13x13)")

for r in range(13):
    cols = st.columns(13)
    for c in range(13):
        # Unique Bonus Logic (not the Scrabble pattern)
        if (r + c) % 5 == 0:
            cols[c].markdown("<div class='board-cell bonus-3w'>3x</div>", unsafe_allow_html=True)
        else:
            cols[c].markdown("<div class='board-cell'> </div>", unsafe_allow_html=True)

# 4. The Player Holder
st.write("---")
st.write("### Your Tiles")
h_cols = st.columns(7)
for i, (tile, pts) in enumerate(st.session_state.hand):
    h_cols[i].button(f"{tile}\n{pts}", key=f"h_{i}")
