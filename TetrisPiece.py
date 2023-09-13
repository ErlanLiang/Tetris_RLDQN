from TetrisPoint import TetrisPoint
from TetrisModel import TetrisModel

# def parsePoint(pointstr: str) -> TetrisPoint:


STICK_STR	= "0 0	0 1	 0 2  0 3"
L1_STR		= "0 0	0 1	 0 2  1 0"
L2_STR		= "0 0	1 0  1 1  1 2"
S1_STR		= "0 0	1 0	 1 1  2 1"
S2_STR		= "0 1	1 1  1 0  2 0"
SQUARE_STR	= "0 0  0 1  1 0  1 1"
PYRAMID_STR	= "0 0  1 0  1 1  2 0"

def parsePoints(string: str) -> list[TetrisPoint]:
    """Parses points from a string.

    Arguments:
        string: A string containing points to parse.

    Returns:
        A list of points parsed from the string.
    """
    points = []
    tok = string.split()
    try:
        while len(tok) > 0:
            x = int(tok.pop(0))
            y = int(tok.pop(0))
            points.append(TetrisPoint(x, y))
    except ValueError:
        raise ValueError(f"Could not parse x,y string: {string}")
    # Make an array out of the collection
    array = [None] * len(points)
    for i in range(len(points)):
        array[i] = points[i]
    return array

class TetrisPiece:
    body: list[TetrisPoint]
    lowestYVals: list[int]
    width: int
    height: int
    next: 'TetrisPiece'
    pieces: list['TetrisPiece']  # May not be needed
    
    def __init__(self, points: list['TetrisPoint']) -> None:
        self.body = points
 
        # Compute the lowest y value for each column
        self.lowestYVals = [0] * TetrisModel.WIDTH
        maxX = 0
        maxY = 0
        minX = 0
        minY = 0
        for tp in self.body:
            x = tp.x
            y = tp.y
            if self.lowestYVals[x] < y:
                self.lowestYVals[x] = y
            if x > maxX:
                maxX = x
            if y > maxY:
                maxY = y
            if x < minX:
                minX = x
            if y < minY:
                minY = y
        self.width = maxX - minX + 1
        self.height = maxY - minY + 1

        self.next = None
        self.pieces = []

    # create a piece from a string
    def createFromString(self, str: str) -> 'TetrisPiece':
        points = parsePoints(str)
        return TetrisPiece(points)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TetrisPiece):
            return False
        if self.width != other.width \
            or self.height != other.height \
            or len(self.body) != len(other.body):
            return False
        for tp in self.body:
            if not tp in other.body:
                return False
        return True
    
    def negativeYExists(self) -> bool:
        for y in self.lowestYVals:
            if y < 0:
                return True
        return False
    
    def __str__(self) -> str:
        return str(self.body)
    
    def __repr__(self) -> str:
        return str(self.body)


if __name__ == "__main__":
    print(TetrisModel.WIDTH)
    