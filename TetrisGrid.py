from TetrisPiece import TetrisPiece
import numpy as np
from enum import IntEnum

class AddStatus(IntEnum):
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
    
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
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
        for i in range(self.width):
            for j in range(self.height):
                if self.Grid[j][i]:
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
            return AddStatus.ADD_OOB
        for point in piece.body:
            if  (row + point.y) >= self.height or (col + point.x) >= self.width:
                return AddStatus.ADD_OOB
            if self.Grid[row - point.y][col - point.x]:
                return AddStatus.ADD_BAD
        for point in piece.body:
            self.Grid[row + point.y][col + point.x] = True
            self.colCount[point.x] += 1
            self.rowCount[point.y] += 1
            self.updatecolrowcount()
        for i in range(self.height): # double check(not sure if correct)
            if self.rowCount[i] == self.width:
                return AddStatus.ADD_ROW_FILLED
        return AddStatus.ADD_OK
    
    def clearRows(self) -> int:
        self.updatecolrowcount()
        cleaCount = 0
        rowC = []
        for i in range(self.getMaxheight()):
            fil = False
            # if self.rowCount[i] == self.width:
            #     cleaCount += 1
            for j in range(self.width):
                if not self.Grid[i][j]:
                    fil = True
                    break
            if not fil:
                cleaCount += 1
                for j in range(self.width):
                    self.Grid[i][j] = False
                    # self.colCount[j] -= 1
                    # self.rowCount[i] -= 1
                rowC.append(i)
                self.updatecolrowcount()
        if cleaCount == 0:
            return 0
        curR = -1
        for i in rowC:
            for j in range(i, self.getMaxheight):
                for k in range(self.width):
                    self.Grid[k][j - curR] = self.Grid[k][j + 1]
                    self.Grid[k][j + 1 - curR] = False
        self.updatecolrowcount
        return cleaCount

        

        
