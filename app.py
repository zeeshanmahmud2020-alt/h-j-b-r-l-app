import streamlit as st
import random
import requests

st.set_page_config(page_title="হ য ব র ল PRO", layout="centered")

@st.cache_resource
def load_dict():
    url = "https://raw.githubusercontent.com/tahmid02016/bangla-wordlist/master/words.txt"
    try:
        r = requests.get(url, timeout=5)
        return set(word.strip() for word in r.text.split())
    except:
        return {"কাকা", "বাবা", "মামা", "বাঘ"}

WORDS_DB = load_dict()

# 1. CSS: Locked Square Grid
st.markdown("""
    <style>
    .block-container { max-width: 550px !important; padding: 10px !important; }
    .game-title { text-align: center; font-size: 45px; font-weight: bold; color: #f1c40f; }
    div.stButton > button[key^="b_"] {
        background-color: #1e272e !important; color: #ecf0f1 !important;
        width: 44px !important; height: 44px !important;
        border: 1px solid #3d4e5f !important; padding: 0px !important; font-size: 16px !important;
    }
    .rack-container {
        display: flex; justify-content: center; gap: 4px;
        background: linear-gradient(#8b5a2b, #5d3a1a); padding: 12px;
        border-bottom: 6px solid #3d2611; border-radius: 4px; margin-top: 10px;
    }
    div.stButton > button[key^="h_"] {
        background-color: #f3cf7a !important; color: #3e2723 !important;
        width: 52px !important; height: 60px !important; font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. STATE INITIALIZATION
SUB = {"1":"₁", "2":"₂", "3":"₃", "4":"₄", "5":"₅"}
POOL = [('কা',1), ('কি',2), ('কু',2), ('কে',3), ('পা',1), ('মা',1), ('বা',1), ('রা',2), ('না',1)]

if 'board' not in st.session_state: st.session_state.board = [["" for _ in range(11)] for _ in range(11)]
if 'hand' not in st.session_state: st.session_state.hand = random.sample(POOL, 7)
if 's1' not in st.session_state: st.session_state.s1 = 0
if 's2' not in st.session_state: st.session_state.s2 = 0
if 'turn' not in st.session_state: st.session_state.turn = 1
if 'sel_idx' not in st.session_state: st.session_state.sel_idx = None
if 'turn_buffer' not in st.session_state: st.session_state.turn_buffer = []

# 3. SIDEBAR
with st.sidebar:
    st.header("📊 Scoreboard")
    st.write(f"**Player 1:** {st.session_state.s1}")
    st.write(f"**Player 2:** {st.session_state.s2}")
    st.write("---")
    st.write(f"👉 **Player {st.session_state.turn}'s Turn**")
    if st.button("🔄 Reset Game"):
        st.session_state.clear()
        st.rerun()

# 4. MAIN GAME UI
st.markdown("<div class='game-title'>হ য ব র ল</div>", unsafe_allow_html=True)

for r in range(11):
    cols = st.columns(11)
    for c in range(11):
        val = st.session_state.board[r][c]
        if cols[c].button(val if val else " ", key=f"b_{r}_{c}"):
            if st.session_state.sel_idx is not None:
                char, pts = st.session_state.hand[st.session_state.sel_idx]
                st.session_state.board[r][c] = char
                # Memory of what was placed this specific turn
                st.session_state.turn_buffer.append({'pos': (r, c), 'char': char, 'pts': pts})
                st.session_state.hand[st.session_state.sel_idx] = random.choice(POOL)
                st.session_state.sel_idx = None
                st.rerun()

st.markdown("<div class='rack-container'>", unsafe_allow_html=True)
h_cols = st.columns(7)
for i, (char, pts) in enumerate(st.session_state.hand):
    if h_cols[i].button(f"{char}{SUB.get(str(pts), '')}", key=f"h_{i}"):
        st.session_state.sel_idx = i
        st.rerun()

# 5. THE GATEKEEPER LOGIC
word = "".join([move['char'] for move in st.session_state.turn_buffer])
st.write(f"Current Attempt: **{word if word else '...'}**")

if st.button("🔥 SUBMIT WORD", use_container_width=True, type="primary"):
    # STRICT CHECK: Must be in WORDS_DB
    if word in WORDS_DB and len(word) > 1:
        pts_earned = sum([move['pts'] for move in st.session_state.turn_buffer])
        if st.session_state.turn == 1: st.session_state.s1 += pts_earned
        else: st.session_state.s2 += pts_earned
        
        # Switch Turn and Clear Buffer
        st.session_state.turn = 2 if st.session_state.turn == 1 else 1
        st.session_state.turn_buffer = []
        st.success(f"Valid! +{pts_earned} points.")
        st.rerun()
    else:
        # GIBBERISH REJECTION: Undo all moves from this turn
        for move in st.session_state.turn_buffer:
            r, c = move['pos']
            st.session_state.board[r][c] = ""
        st.session_state.turn_buffer = []
        st.error("Not a valid word! Moves reverted.")
        st.rerun()
