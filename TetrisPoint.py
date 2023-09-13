class TetrisPoint:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, TetrisPoint):
            return self.x == __value.x and self.y == __value.y
        return False
        
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def compare(self, point: 'TetrisPoint') -> bool:
        if self.x == point.x and self.y == point.y:
            return 0
        if self.x > point.x or (self.x == point.x and self.y > point.y):
            return 1
        return -1

    def clone(self) -> 'TetrisPoint':
        return TetrisPoint(self.x, self.y)

if __name__ == "__main__":
    p = TetrisPoint(1, 2)
    print(p)
