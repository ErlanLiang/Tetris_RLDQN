from TetrisPiece import TetrisPiece
from TetrisModel import TetrisModel
import numpy as np

ADD_OK = 0
ADD_ROW_FILLED = 1
ADD_OOB = 2
ADD_BAD = 3

class TetrisGrid:
    width: int
    height: int
    Grid: np.ndarray
    colCount: np.ndarray
    rowCount: np.ndarray
    
    def __init__(self) -> None:
        self.width = TetrisModel.WIDTH
        self.height = TetrisModel.HEIGHT
        self.Grid = np.zeros((self.height, self.width), dtype=bool)
        self.colCount = np.zeros(self.width, dtype=int)
        self.rowCount = np.zeros(self.height, dtype=int)

    def getMaxheight(self) -> int:
        return np.max(self.colCount)
    
    def getColumnHeight(self, col: int) -> int:
        return self.colCount[col]
    
    def getRowWidth(self, row: int) -> int:
        return self.rowCount[row]
    
    def checkblockfill(self, x:int, y:int) -> bool:
        if(x >= 0 and x < self.width and y >= 0 and y < self.height):
            return self.Grid[y][x]
        return False
    
    def placementHeight(self, piece: TetrisPiece, col: int) -> int:
        if col < 0 or col >= self.width:
            return -1
        lowestY = piece.lowestYVals
        HestH = -lowestY[0] + self.getColumnHeight(col)
        for i in range(1, len(lowestY)):
            HestH = max(HestH, -lowestY[i] + self.getColumnHeight(col + i))
        return HestH
    
    def updatecolrowcount(self) -> None:
        self.colCount = np.zeros(self.width, dtype=int)
        self.rowCount = np.zeros(self.height, dtype=int)
        for i in range(self.height):
            for j in range(self.width):
                if self.Grid[i][j]:
                    self.colCount[i] = 1 + j
                    self.rowCount[j] += 1
    
    def placePiece(self, piece: TetrisPiece, col: int, row: int) -> int:
        """
        ADD_OK = 0
        ADD_ROW_FILLED = 1
        ADD_OOB = 2
        ADD_BAD = 3
        """
        if col < 0 or col >= self.width or row < 0 or row >= self.height:
            return ADD_OOB
        for point in piece.body:
            if  (row + point.y) >= self.height or (col + point.x) >= self.width:
                return ADD_OOB
            if self.Grid[row + point.y][col + point.x]:
                return ADD_BAD
        for point in piece.body:
            self.Grid[row + point.y][col + point.x] = True
            self.colCount[col + point.x] += 1
            self.rowCount[row + point.y] += 1
            self.updatecolrowcount()
        for i in range(self.height): # double check(not sure if correct)
            if self.rowCount[i] == self.width:
                return ADD_ROW_FILLED
        return ADD_OK
    
    def clearRows(self) -> int:
        self.updatecolrowcount()
        cleaCount = 0
        for i in range(self.height):
            if self.rowCount[i] == self.width:
                cleaCount += 1
                for j in range(self.width):
                    fil = False
                    self.Grid[i][j] = False
                    self.colCount[j] -= 1
                    self.rowCount[i] -= 1

        
