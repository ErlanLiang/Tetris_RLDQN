from TetrisPiece import TetrisPiece
from TetrisGrid import TetrisGrid
from enum import Enum

class TetrisAction(Enum):
    TRANSFORM = 0
    LEFT = 1
    RIGHT = 2
    DROP = 3
    DOWN = 4

class TetrisModel:
    WIDTH = 10
    HEIGHT = 22
    grid: TetrisGrid
    score: int
    pcount: int #numbers of pieces play so far
    cur_piece: TetrisPiece
    nxt_piece: TetrisPiece
    currentX: int
    currentY: int
    newX: int
    newY: int
    
    
    def __init__(self) -> None:
        self.grid = TetrisGrid(self.WIDTH, self.HEIGHT)
        # self.piece = 
        self.gameon = False

    def startGame(self) -> None:
        self.score = 0
        self.pcount = 0
        self.gameon = True

    def computeNewPostion(self, action: TetrisAction) -> None:
        self.newX = self.currentX
        self.newY = self.currentY
        if action == TetrisAction.TRANSFORM:
            self.cur_piece.transform()
        elif action == TetrisAction.LEFT:
            self.newX -= 1
        elif action == TetrisAction.RIGHT:
            self.newY += 1
        elif action == TetrisAction.DOWN:
            self.newY -= 1
        elif action == TetrisAction.DROP:
            self.newY = self.grid.placementHeight(self.nxt_piece, self.currentX)
            if self.newY > self.currentY:
                self.newY = self.currentY
        else:
            raise ValueError("Action not defined")
        
    def setCurrent(self, piece: TetrisPiece, x: int, y: int) -> int:
        result = self.grid.placePiece(piece, x, y)

        if (result <= TetrisGrid.ADD_ROW_FILLED):
            self.cur_piece = piece
            self.currentX = x
            self.currentY = y
        return result

    












