from TetrisPiece import TetrisPiece
from TetrisGrid import TetrisGrid
from TetrisGrid import AddStatus
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
    gameon: bool
    
    
    def __init__(self) -> None:
        self.grid = TetrisGrid(self.WIDTH, self.HEIGHT)
        self.score = 0
        # self.piece = 
        self.gameon = False

    def startGame(self) -> None:
        self.score = 0
        self.pcount = 0
        self.gameon = True
        self.nxt_piece = TetrisPiece.createRandomPiece()
        self.currentX = self.WIDTH // 2
        self.currentY = self.HEIGHT - self.nxt_piece.height - 1

    def computeNewPostion(self, action: TetrisAction) -> None:
        self.newX = self.currentX
        self.newY = self.currentY
        if action == TetrisAction.TRANSFORM:
            self.cur_piece.transform()
        elif action == TetrisAction.LEFT:
            self.newX -= 1
        elif action == TetrisAction.RIGHT:
            self.newX += 1
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

        print(result)

        if (result <= AddStatus.ADD_ROW_FILLED):
            self.cur_piece = piece
            self.currentX = x
            self.currentY = y
        return result
    
    def addNewPiece(self) -> int:
        self.pcount += 1
        self.score += 1

        pic = self.nxt_piece
        self.nxt_piece = TetrisPiece.createRandomPiece()
        x = (self.grid.width - pic.width) // 2
        y = self.grid.height - pic.height#pic.lowestYVals[0] - 1
        if self.setCurrent(pic, x, y) > AddStatus.ADD_ROW_FILLED:
            self.gameon = False

    def executeMove(self, action: TetrisAction) -> None:
        self.computeNewPostion(action)
        result = self.setCurrent(self.nxt_piece, self.newX, self.newY)
        failed = result >= AddStatus.ADD_OOB
        if(failed):
            self.grid.placePiece(self.cur_piece, self.currentX, self.currentY)
        if(failed and action == TetrisAction.DOWN):
            cleared = self.grid.clearRows()
            if cleared > 0:
                if cleared == 1:
                    self.score += 5
                elif cleared == 2:
                    self.score += 10
                elif cleared == 3:
                    self.score += 20
                elif cleared == 4:
                    self.score += 40

            if (self.grid.getMaxheight() > self.grid.height):
                self.gameon = False
            else:
                print("add new piece")
                self.addNewPiece()

    










