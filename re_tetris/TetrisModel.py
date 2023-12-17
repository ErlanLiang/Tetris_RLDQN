import numpy as np
import random
from enum import IntEnum

# Define the TetrisAction enum
class TetrisAction(IntEnum):
    PICK = 0
    LEFT = 1
    RIGHT = 2
    DONESETUP = 3
    DOWN = 4
    UP = 5

# Define the TetrisGrid class
class TetrisGrid:
    WIDTH = 10
    HEIGHT = 22
    
    grid: np.ndarray

    def __init__(self):
        self.grid = np.zeros((self.HEIGHT, self.WIDTH), dtype=bool)

    def add_piece(self, piece, x, y):
        """
        Add the piece to the grid at the specified position.
        """
        for i in range(piece.shape.shape[0]):
            for j in range(piece.shape.shape[1]):
                if piece.shape[i][j]:
                    self.grid[y + i][x + j] = True

    def remove_full_lines(self):
        """
        Remove full lines from the grid and return the number of lines removed.
        """
        lines_removed = 0
        rows_to_check = []

        # Check each row to see if it's full
        for i in range(self.HEIGHT):
            if all(self.grid[i]):
                rows_to_check.append(i)

        # For each full row, move all rows above it down by one
        for row in rows_to_check:
            self.grid[1:row+1] = self.grid[:row]
            lines_removed += 1

        # Clear the top rows
        for i in range(lines_removed):
            self.grid[i].fill(False)

        return lines_removed

    def check_collision(self, piece, x, y):
        """
        Check if placing the piece at the specified position would cause a collision.
        """
        for i in range(piece.shape.shape[0]):
            for j in range(piece.shape.shape[1]):
                if piece.shape[i][j]:
                    # Check if piece is outside the grid
                    if x + j < 0 or x + j >= self.WIDTH or y + i >= self.HEIGHT:
                        return True
                    # Check if piece collides with another piece
                    if self.grid[y + i][x + j]:
                        return True
        return False

# Define the TetrisPiece class
class TetrisPiece:
    shape: np.ndarray
    num_pieces: int
    rotation: int
    original_shape: np.ndarray

    # Define the standard Tetris pieces as constants
    TETROMINOS = {
        1: np.array([[1,1,1,0,1,1,1,1,1,1], [0,0,0,1,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0]]),
        # 2: np.array([[1, 1]]),
        # 3: np.array([[1, 0], [1, 1]]),
        # 4: np.array([[1, 1], [1, 1]]),
        # 5: np.array([[1, 0],[1, 1], [1, 1]]),
        # 5: np.array([[1, 1, 0],[1, 1, 1]]),

    }

    def __init__(self, shape: int):
        self.shape = self.TETROMINOS[shape]
        self.original_shape = self.shape
        self.num_pieces = shape
        self.rotation = 0
        # self.shape = self.TETROMINOS[shape][0]
        # self.original_shape = 0
        # self.num_pieces = shape
        # self.rotation = 0
        # self.length = self.shape.shape[0]
        # self.transform_length = len(self.TETROMINOS[shape])

    def copy(self):
        """
        Return a copy of this piece.
        """
        piece_copy = TetrisPiece(self.num_pieces)
        piece_copy.shape = self.shape
        piece_copy.rotation = self.rotation
        piece_copy.original_shape = self.original_shape
        return piece_copy

    def rotate(self):
        # Rotate the piece
        self.shape = np.rot90(self.shape)
        self.rotation = (self.rotation + 1) % 4

    def transform(self):
        pass

# Define the TetrisModel class
class TetrisModel:
    WIDTH = 10
    HEIGHT = 22

    grid: TetrisGrid
    game_over: bool
    current_piece: TetrisPiece
    current_x: int
    current_y: int
    score: int
    setup: bool
    picker: list

    def __init__(self):
        self.grid = TetrisGrid()
        self.current_piece = None
        self.current_x = 0
        self.current_y = 0
        self.score = 0
        self.game_over = False
        self.setup = True
        self.picker = [0, 0, 0] # [0] 0: not picked & not on piece, 1: not picked & on piece, 2: picked & not stack, 3: picked & stack
                                # [1] x, [2] y
        self.backup_piece = None #back up the piece when picked
        self.backup_picker = None #back up the picker when picked

    def startGame(self):
        """
        Start the game by selecting a random piece.
        """
        self.spawn_piece()

    def spawn_piece(self):
        """
        Spawn a new piece at the top-middle of the grid.
        """
        self.current_piece = TetrisPiece(random.choice(list(TetrisPiece.TETROMINOS.keys())))
        # self.current_x = self.WIDTH // 2 - self.current_piece.shape.shape[1] // 2
        # self.current_y = 0  # Start at the top of the grid
        self.current_x = 0
        self.current_y = 0  # Start at the top of the grid
        first_x = self.WIDTH // 2
        self.setup = True
        self.picker = [0, first_x, 0]

        # If the new piece causes a collision, the game is over
        # if self.grid.check_collision(self.current_piece, self.current_x, self.current_y):
            # self.game_over = True  # Set the game_over flag

    # Check if the picker is on the piece
    def check_picker_status1(self):
        if self.current_piece[self.picker[2]][self.picker[1]] == 1:
            self.picker[0] = 1
        else:
            self.picker[0] = 0

    # Ceck if the picker is on the piece(Picked)
    def check_picker_status2(self):
        if self.current_piece[self.picker[2]][self.picker[1]] == 1:
            self.picker[0] = 3
        else:
            self.picker[0] = 2
            self.current_piece[self.picker[2]][self.picker[1]] = 1

    def executeMove(self, action):
        """
        Execute the specified move. Move the picker to transform the piece.
        """
        # Not picked
        if self.picker[0] < 2:
            if action == TetrisAction.PICK: #pick
                if self.picker[0] == 1:
                    self.backup_picker = self.picker.copy()
                    self.picker[0] = 2
                    self.backup_piece = self.current_piece.copy()
                    
            elif action == TetrisAction.UP: #UP
                if self.picker[2] - 1 < 0:
                    pass
                else:
                    self.picker[2] = self.picker[2] - 1
                self.check_picker_status1
            elif action == TetrisAction.LEFT:
                if self.picker[1] - 1 < 0:
                    pass
                else:
                    self.picker[1] = self.picker[1] - 1
                self.check_picker_status1
            elif action == TetrisAction.RIGHT:
                if self.picker[1] + 1 > 9:
                    pass
                else:
                    self.picker[1] = self.picker[1] + 1
                self.check_picker_status1
            elif action == TetrisAction.DOWN:
                if self.picker[2] + 1 > 2:
                    pass
                else:
                    self.picker[2] = self.picker[2] + 1
                self.check_picker_status1
            elif action == TetrisAction.DONESETUP:
                while not self.grid.check_collision(self.current_piece, self.current_x, self.current_y + 1):
                    self.current_y += 1
                self.setup = False
                self.grid.add_piece(self.current_piece, self.current_x, self.current_y)
                self.score += self.grid.remove_full_lines()
                self.spawn_piece()
        #Picked
        else: 
            if action == TetrisAction.UP: #UP
                if self.picker[2] - 1 < 0:
                    pass
                else:
                    if self.picker[0] != 3:
                        self.current_piece[self.picker[2]][self.picker[1]] = 0
                    self.picker[2] -= 1
                    self.check_picker_status2
            elif action == TetrisAction.LEFT:
                if self.picker[1] - 1 < 0:
                    pass
                else:
                    if self.picker[0] != 3:
                        self.current_piece[self.picker[2]][self.picker[1]] = 0
                    self.picker[1] -= 1
                    self.check_picker_status2
            elif action == TetrisAction.RIGHT:
                if self.picker[1] + 1 > 9:
                    pass
                else:
                    if self.picker[0] != 3:
                        self.current_piece[self.picker[2]][self.picker[1]] = 0
                    self.picker[1] += 1
                    self.check_picker_status2
            elif action == TetrisAction.DOWN:
                if self.picker[2] + 1 > 2:
                    pass
                else:
                    if self.picker[0] != 3:
                        self.current_piece[self.picker[2]][self.picker[1]] = 0
                    self.picker[2] += 1
                    self.check_picker_status2
            elif action == TetrisAction.PICK: #pick
                if self.picker[0] == 3:
                    self.current_piece = self.backup_piece
                    self.picker = self.backup_picker
                else:
                    self.picker[0] = 1

    # def canPerformAction(self, action):
    #     """
    #     Check if the specified action can be performed.
    #     """
    #     if action == TetrisAction.TRANSFORM:
    #         backup_piece = self.current_piece.copy()
    #         self.current_piece.rotate()
    #         can_perform = not self.grid.check_collision(self.current_piece, self.current_x, self.current_y)
    #         self.current_piece = backup_piece
    #         return can_perform
    #     elif action == TetrisAction.LEFT:
    #         return not self.grid.check_collision(self.current_piece, self.current_x - 1, self.current_y)

    #     elif action == TetrisAction.RIGHT:
    #         return not self.grid.check_collision(self.current_piece, self.current_x + 1, self.current_y)

    #     elif action == TetrisAction.DOWN:
    #         return not self.grid.check_collision(self.current_piece, self.current_x, self.current_y + 1)

    #     elif action == TetrisAction.DONESETUP:
    #         return True  # Always allowed
    #     return False