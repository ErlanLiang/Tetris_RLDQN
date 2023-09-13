from TetrisPiece import TetrisPiece
from TetrisGrid import TetrisGrid

class TetrisModel:
    WIDTH = 10
    HEIGHT = 22
    Grid: TrteisGrid
    score: int
    pcount: int #numbers of pieces play so far
    cur_piece: TetrisPiece
    nxt_piece: TetrisPiece
    action = ["TRANSFORM", "LEFT", "RIGHT", "DROP", "DOWN"]
    enum_action = enumerate(action)
    

    def __init__(self) -> None:
        pass











