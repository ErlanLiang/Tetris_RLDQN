import numpy as np
import random
from enum import IntEnum

# Define the TetrisAction enum
class TetrisAction(IntEnum):
    PICK = 0
    LEFT = 1
    RIGHT = 2
    COMMIT = 3 # Commit changes to the piece
    DOWN = 4
    UP = 5

# Define the TetrisGrid class
class TetrisGrid:
    WIDTH = 10
    HEIGHT = 22
    
    grid: np.ndarray

    def __init__(self):
        """
        Initialize the grid.
        """
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

    def check_collision(self, piece, y):
        """
        Check if placing the piece at the specified position would cause a collision.
        """
        piece_height = piece.shape.shape[0]
        grid_height = self.grid.shape[0]

        # Check if the piece is out of the board's vertical bounds
        if y < 0 or (y + piece_height) > grid_height:
            return True

        # Extract the relevant part of the board
        grid_slice = self.grid[y:y + piece_height]

        # Check for collision
        and_result = np.logical_and(grid_slice, piece.shape)
        collision = np.any(and_result)

        return collision

# Define the TetrisPiece class
class TetrisPiece:
    shape: np.ndarray
    num_pieces: int

    # Define the standard Tetris pieces as constants
    TETROMINOS = {
        1: np.array([[1,1,0,0,1,1,1,1,1,1], [0,0,0,1,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,1,0]]),
        2: np.array([[0,0,0,0,1,1,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0]]),
        3: np.array([[0,0,0,0,1,0,1,0,1,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0]]),
        4: np.array([[0,0,0,0,1,1,0,0,0,0], [0,0,0,0,1,1,0,0,0,0], [0,0,0,0,0,0,0,0,0,0]]),
        5: np.array([[0,0,0,0,1,1,0,0,0,0], [0,0,0,0,1,1,0,0,0,0], [0,0,0,0,0,1,0,0,0,0]]),
        6: np.array([[0,0,0,0,1,1,1,0,0,0], [0,0,0,0,1,1,1,0,0,0], [0,0,0,0,0,0,0,0,0,0]]),

    }

    def __init__(self, shape: int):
        """
        Initialize a piece with the specified shape.
        """
        self.shape = self.TETROMINOS[shape].copy()

    def copy(self):
        """
        Return a copy of this piece.
        """
        piece_copy = TetrisPiece(self.num_pieces)
        piece_copy.shape = self.shape
        return piece_copy

    def rotate(self):
        """
        Rotate the piece clockwise.
        """
        self.shape = np.rot90(self.shape)
        self.rotation = (self.rotation + 1) % 4

    def update_piece_shape(self):
        """
        Update the piece shape after commiting changes to the piece.
        """
        first_non_empty_row = 0
        last_non_empty_row = self.shape.shape[0] - 1

        # Find the first and last non-empty rows
        while first_non_empty_row <= last_non_empty_row and np.all(self.shape[first_non_empty_row] == 0):
            first_non_empty_row += 1
        while last_non_empty_row >= first_non_empty_row and np.all(self.shape[last_non_empty_row] == 0):
            last_non_empty_row -= 1

        # Slice the array to keep only non-empty edge rows
        self.shape = self.shape[first_non_empty_row:last_non_empty_row+1]

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
        """
        Initialize the Tetris model.
        """
        self.grid = TetrisGrid()
        self.current_piece = None
        self.current_x = 0
        self.current_y = 0
        self.score = 0
        self.game_over = False
        self.setup = True
        self.picker = [0, 0, 0] # [0] Status0: not picked & not on piece; Status1: not picked & on piece; 
                                #     Status2: picked & not stack;        Status3: picked & stack.
                                # [1] x,    [2] y
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
        self.current_x = 0
        self.current_y = 0  # Start at the top of the grid
        first_x = self.WIDTH // 2
        self.setup = True
        self.picker = [0, first_x, 0]
        self.check_picker_status()

        # If the new piece causes a collision, the game is over (Deprecated, the game won't be over anymore)
        # if self.grid.check_collision(self.current_piece, self.current_x, self.current_y):
            # self.game_over = True  # Set the game_over flag

    def check_picker_status(self):
        """
        Check if the picker is on the piece.
        """
        if self.current_piece.shape[self.picker[2]][self.picker[1]] == 1:
            self.picker[0] = 1
        else:
            self.picker[0] = 0

    def check_picker_status_picked(self):
        """
        Check if the picker is on the piece. (When picked)
        """
        if self.current_piece.shape[self.picker[2]][self.picker[1]] == 1:
            self.picker[0] = 3
        else:
            self.picker[0] = 2
            self.current_piece.shape[self.picker[2]][self.picker[1]] = 1

    def executeMove(self, action):
        """
        Execute the specified move. Move the picker to transform the piece.
        """
        if self.picker[0] < 2:
            # No piece is picked
            if action == TetrisAction.PICK:
                if self.picker[0] == 1:
                    self.backup_picker = self.picker.copy()
                    self.picker[0] = 2
                    self.backup_piece = self.current_piece.shape.copy()
                    
            elif action == TetrisAction.UP:
                if self.picker[2] - 1 < 0:
                    pass
                else:
                    self.picker[2] = self.picker[2] - 1
                    self.check_picker_status()

            elif action == TetrisAction.LEFT:
                if self.picker[1] - 1 < 0:
                    pass
                else:
                    self.picker[1] = self.picker[1] - 1
                    self.check_picker_status()

            elif action == TetrisAction.RIGHT:
                if self.picker[1] + 1 > 9:
                    pass
                else:
                    self.picker[1] = self.picker[1] + 1
                    self.check_picker_status()

            elif action == TetrisAction.DOWN:
                if self.picker[2] + 1 > 2:
                    pass
                else:
                    self.picker[2] = self.picker[2] + 1
                    self.check_picker_status()

            elif action == TetrisAction.COMMIT:
                self.current_piece.update_piece_shape()
                self.current_y = self.HEIGHT - self.current_piece.shape.shape[0]
                while self.grid.check_collision(self.current_piece, self.current_y):
                    self.current_y -= 1
                self.setup = False
                self.grid.add_piece(self.current_piece, self.current_x, self.current_y)
                self.score += self.grid.remove_full_lines()
                self.spawn_piece()
        else: 
            # A piece is picked
            if action == TetrisAction.UP:
                if self.picker[2] - 1 < 0:
                    pass
                else:
                    if self.picker[0] != 3:
                        self.current_piece.shape[self.picker[2]][self.picker[1]] = 0
                    self.picker[2] -= 1
                    self.check_picker_status_picked() 
                    
            elif action == TetrisAction.LEFT:
                if self.picker[1] - 1 < 0:
                    pass
                else:
                    if self.picker[0] != 3:
                        self.current_piece.shape[self.picker[2]][self.picker[1]] = 0
                    self.picker[1] -= 1
                    self.check_picker_status_picked()

            elif action == TetrisAction.RIGHT:
                if self.picker[1] + 1 > 9:
                    pass
                else:
                    if self.picker[0] != 3:
                        self.current_piece.shape[self.picker[2]][self.picker[1]] = 0
                    self.picker[1] += 1
                    self.check_picker_status_picked() 

            elif action == TetrisAction.DOWN:
                if self.picker[2] + 1 > 2:
                    pass
                else:
                    if self.picker[0] != 3:
                        self.current_piece.shape[self.picker[2]][self.picker[1]] = 0
                    self.picker[2] += 1
                    self.check_picker_status_picked()
                        
            elif action == TetrisAction.PICK:
                if self.picker[0] == 3:
                    self.current_piece.shape = self.backup_piece
                    self.picker = self.backup_picker
                else:
                    self.picker[0] = 1
                    