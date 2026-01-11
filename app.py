import numpy as np

# --- THE SPATIAL GRID ---
def initialize_board():
    # ' ' represents an empty square
    return [[" " for _ in range(9)] for _ in range(9)]

# --- THE MULTIPLIER MAP ---
# 1 = Normal, 2 = DL, 3 = TL, 4 = DW, 5 = TW
BOARD_LAYOUT = np.array([
    [5, 1, 1, 2, 1, 2, 1, 1, 5],
    [1, 4, 1, 1, 1, 1, 1, 4, 1],
    [1, 1, 4, 1, 1, 1, 4, 1, 1],
    [2, 1, 1, 4, 1, 4, 1, 1, 2],
    [1, 1, 1, 1, 4, 1, 1, 1, 1], # Center (4,4) is DW
    [2, 1, 1, 4, 1, 4, 1, 1, 2],
    [1, 1, 4, 1, 1, 1, 4, 1, 1],
    [1, 4, 1, 1, 1, 1, 1, 4, 1],
    [5, 1, 1, 2, 1, 2, 1, 1, 5]
])
