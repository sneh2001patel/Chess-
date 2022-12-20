# Game Properties
TILE = 100  # Change this to resize the window to fit the board 100 is recommended if need smaller try 80
BOARDLEN = 8
WIDTH = TILE * BOARDLEN  # (800)
HEIGHT = TILE * BOARDLEN  # (800)
TITLE = "Chess"
FPS = 60

# SCORES FOR THE PIECES
PIECES_SCORE = {
    "P": 1,
    "H": 3,
    "B": 3,
    "R": 5,
    "Q": 9,
    "K": 0
}

# CHECKMATE HAS TO HAVE A HIGHER SCORE THAN ANYTHING PIECES CAN HAVE
CHECKMATE_SCORE = {
    "WIN": 1000,
    "LOSE": -1000,
    "TIE": 0
}

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
NAVY = (28, 42, 80)

# alpha and beta init values
ALPHA = float('-inf')
BETA = float('inf')

# Pieces Path
BKING = "pieces/black/BKing.png"
WKING = "pieces/white/WKing.png"

BQUEEN = "pieces/black/BQueen.png"
WQUEEN = "pieces/white/WQueen.png"

BROOK = "pieces/black/BRook.png"
WROOK = "pieces/white/WRook.png"

BBISHOP = "pieces/black/BBishop.png"
WBISHOP = "pieces/white/WBishop.png"

BKNIGHT = "pieces/black/BKnight.png"
WKNIGHT = "pieces/white/WKnight.png"

BPAWN = "pieces/black/BPawn.png"
WPAWN = "pieces/white/WPawn.png"
