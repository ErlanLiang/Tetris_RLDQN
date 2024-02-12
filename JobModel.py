from enum import IntEnum
import numpy as np
import csv
from collections import deque

JOB_DATA: dict
SETUP_RULE: dict
NUM_TYPE: int
NUM_COL: int
NUM_HEIGHT = 10
JOB_TYPE_PATH = "./tests/type_info.csv"
JOB_INFO_PATH = "./tests/job_info.csv"
SETUP_PATH = "./tests/setup_info.csv"
MAX_SETUP_TIME: int
JOB_ID: dict # job id -> job name
MAX_JOB_HEIGHT: int

def initialize_job_data():
    global JOB_DATA, NUM_TYPE, NUM_COL, MAX_SETUP_TIME, SETUP_RULE, JOB_ID, MAX_JOB_HEIGHT

    #JOB_DATA[job name] = [order(deque colum order), shape(nparray model), job id(int)]
    JOB_DATA, piece_info, JOB_ID, MAX_JOB_HEIGHT = handle_type_info_file(JOB_TYPE_PATH)                                                                    

    #SETUP_RULE[colum][from job][to job] = setup time(int)
    SETUP_RULE, MAX_SETUP_TIME = handle_setup_file(SETUP_PATH, list(JOB_DATA.keys()))

    NUM_TYPE = int(piece_info[0][1])  # Number of types of job

    NUM_COL = int(piece_info[0][3])   # Number of columns

class ScheduleAction(IntEnum):
    PROGRESS = 0
    BLOCK1 = 1
    BLOCK2 = 2
    BLOCK3 = 3
    BLOCK4 = 4
    BLOCK5 = 5
    BLOCK6 = 6
    BLOCK7 = 7
    BLOCK8 = 8
    BLOCK9 = 9

class Job:
    id: int
    name: str
    order: deque
    shape: np.ndarray
    fix_shape: np.ndarray
    curr_time: int

    def __init__(self, name: str):
        self.name = name
        self.order = JOB_DATA[name][0].copy()          # Order of the columns
        self.shape = JOB_DATA[name][1].copy()          # Shape of the job piece
        self.id = JOB_DATA[name][2]                    # ID of the job piece
        self.fix_shape = np.rot90(self.shape)          # Fixed shape of the job piece
        self.curr_time = 0                             # Current height of the job piece, drop part can not be lower than this height

    def drop_block(self):
        """
        Drop one part of the job piece into the grid,
        update the parameters of the job piece.
        """
        # Update the shape, order of the job piece and the height
        zero = np.zeros((1, self.shape.shape[1]), dtype=int)
        drop_col = self.order.popleft() - 1
        col_len = np.sum(self.shape[drop_col], axis=0) # length of 1 the column

        # update the shape of the job piece
        self.shape[drop_col] = zero
        self.fix_shape = np.rot90(self.shape)

        return col_len, drop_col

class ScheduleGrid:
    HEIGHT: int
    WIDTH: int
    grid: np.ndarray
    curr_top: list[str]
    curr_time: list[int]
    
    def __init__(self, width: int, height: int):
        self.HEIGHT = height
        self.WIDTH = width
        self.grid = np.zeros(
            (self.HEIGHT, self.WIDTH), dtype=int) # Grid of the schedule

        self.curr_top = [None] * self.WIDTH       # Current top of the grid job piece type
        self.curr_time = [0] * self.WIDTH       # Current time of the grid of each column

class ScheduleModel:
    HEIGHT: int
    WIDTH: int
    data: deque
    base_time: int
    max_time: int
    curr_job: list[Job]
    num_pieces: int
    grid: ScheduleGrid
    grid_history: np.ndarray
    game_over: bool

    def __init__(self):
        initialize_job_data()                     # Initialize the job data
        self.data = deque()                       # Data of upcoming job of the schedule
        with open(JOB_INFO_PATH, encoding='utf-8-sig') as file:
            for line in csv.reader(file):
                self.data.append(line)
        file.close()
        grid_info = self.data.popleft()
        self.data.popleft()

        # Setup the grid
        self.num_pieces = int(grid_info[1])       # Number of pieces
        self.WIDTH = int(grid_info[3])            # Width of the grid(M)
        self.HEIGHT = NUM_HEIGHT + MAX_SETUP_TIME         # Height of the grid(including hidden rows(MAX_SETUP_TIME))
        self.grid = ScheduleGrid(self.WIDTH, self.HEIGHT)

        self.base_time = 0                        # Current time of the grid
        self.max_time = NUM_HEIGHT                # Maximum time of the grid
        self.curr_job = []                        # Current time's job of the grid
        self.grid_history = np.ndarray((0, self.WIDTH), dtype=int) # History of the grid
        self.game_over = False

    def start_game(self):
        """
        Start the game.
        """
        # Add new job to the current job list
        while self.data and self.data[0][2] == '0':
            self.curr_job.append(Job(self.data.popleft()[1]))
            self.num_pieces -= 1
        
        # check the status of the game
        self.check_status()
    
    def end_game(self):
        """
        Check if the game is over.
        """
        print(JOB_ID)
        self.game_over = True

        # append the current grid to the grid history
        for i in range(self.HEIGHT):
            self.grid_history = np.insert(self.grid_history, 0, self.grid.grid[i], axis=0)

        # print the grid history
        print("Schedule Grid History")
        print(self.grid_history)

        
    
    def add_time(self):
        """
        Time goes by one unit.
        update the current time of the grid and the current job.
        """
        self.base_time += 1
        self.max_time += 1
        time = str(self.base_time)

        # Add new job to the current job list
        while self.data and self.data[0][2] == time and self.num_pieces > 0:
            self.curr_job.append(Job(self.data.popleft()[1]))
            self.num_pieces -= 1

        # Update the grid by deleting the bottom row  
        self.remove_bottom()
        self.check_status()


    def check_status(self):
        """
        Check the status of the game. In the folling cases, the time will add 1:
        1, There are no empty spaces in the bottom line.
        2, There are no job in the current job list.
        3, A block is touching the top of the grid.
        this function handle the 1, 2 cases.
        """
        # check if the bottom line is full
        bottom_full = self.check_bottom_full()
        while bottom_full:
            self.add_time()
            bottom_full = self.check_bottom_full()
        
        # check if the current job list is empty
        while not self.curr_job:
            if self.num_pieces == 0:
                self.end_game()
                break
            else:
                self.add_time()
    
    def execute_move(self, action: ScheduleAction):
        """
        Execute the move of the game.
        """
        # pass
        if action == ScheduleAction.PROGRESS:
            self.add_time()
        else:
            self.commit(action)

    def commit(self, action: ScheduleAction):
        """
        Commit the move of the game.
        """
        if action > len(self.curr_job):
            return
        
        job = self.curr_job[action - 1]
        drop_len, drop_col = job.drop_block()
        cur_top = self.grid.curr_top[drop_col]
        col_time = self.grid.curr_time[drop_col]

        # get the setup time
        setup_time = 0
        if cur_top:
            col_str = "M" + str(drop_col + 1) 
            setup_time = SETUP_RULE[col_str][cur_top][job.name]

        # check if the block is touching the top of the grid
        fix = max((job.curr_time + drop_len), (col_time + setup_time + drop_len)) - self.max_time
        if fix > 0:
            for i in range(fix):
                self.add_time()
        elif fix == 0:
            self.add_time()
        
        height = col_time - self.base_time + MAX_SETUP_TIME
        updated_time = col_time + setup_time
        if height < 0:
            height = 0
            updated_time = self.base_time
        self.add_setup_time(setup_time, drop_col, height)

        if updated_time > job.curr_time:
            time = updated_time - self.base_time
            if time < 0:
                time = 0
            height =  time + MAX_SETUP_TIME
            self.update_grid(drop_col, height, job, drop_len)
            self.grid.curr_time[drop_col] = updated_time + drop_len
        else:
            time = job.curr_time - self.base_time
            if time < 0:
                time = 0
            height =  time + MAX_SETUP_TIME
            self.update_grid(drop_col, height, job, drop_len)
            self.grid.curr_time[drop_col] = job.curr_time + drop_len
        
        if not job.order:
            self.curr_job.pop(action - 1)
        else:
            job.curr_time = self.grid.curr_time[drop_col]

        self.check_status()
  
    def add_setup_time(self, setup_time: int, col: int, height: int):
        """
        Add the setup time to the grid.
        """
        for i in range(setup_time):
            self.grid.grid[height + i][col] = 1
    
    def update_grid(self, col: int, height: int, job: Job, drop_len: int):
        """
        Update the grid by adding the job piece to the grid.
        """
        for i in range(drop_len):
            self.grid.grid[height + i][col] = job.id
        self.grid.curr_top[col] = job.name
    
    def check_bottom_full(self):
        """
        Check if the bottom line is full.
        """
        for i in self.grid.grid[MAX_SETUP_TIME]:
            if i == 0:
                return False
        return True       

    def remove_bottom(self):
        """
        Remove the bottom row of the grid.
        """
        """
        Remove the bottom row of the grid, store the row into the hidden row,
        check the hidden row is full or not, if so, store the hidden row into the grid history.
        """
        # pop the bottom row, and all the rows above it move down one row, and the top row is all 0
        bottom = self.grid.grid[MAX_SETUP_TIME]       
        self.grid.grid = np.delete(self.grid.grid, MAX_SETUP_TIME, axis=0)       
        self.grid.grid = np.insert(self.grid.grid, self.HEIGHT - 1, np.zeros(self.WIDTH), axis=0)

        # store the bottom row into the hidden row
        hidden_bottom = self.grid.grid[0]
        self.grid.grid = np.delete(self.grid.grid, 0, axis=0)
        self.grid.grid = np.insert(self.grid.grid, MAX_SETUP_TIME - 1, bottom, axis=0)

        #append the hidden row into the grid history
        self.grid_history = np.insert(self.grid_history, 0, hidden_bottom, axis=0)
        
# ========================================================================================================
# initialize function below
# ========================================================================================================
def handle_type_info_file(type_info_file: str):
    """
    Handle the type info file and 
    return the job model and the piece info.
    """
    max_job_height = 0
    id_dict = {}
    cur_id = 2
    piece_info = []
    i = 0
    with open(type_info_file, encoding='utf-8-sig') as file:
        data = {}
        for line in csv.reader(file):
            if i < 2:
                piece_info.append(line)
                i += 1
            else:
                if line[0] != '':
                    key = line[0]
                    order = line[1].split(",")
                    cur_data = line[2:]
                    order, shape, height = get_job_model(cur_data, order)
                    if height > max_job_height:
                        max_job_height = height
                    data[key] = [order, shape, cur_id]
                    id_dict[cur_id] = key
                    cur_id += 1
    file.close()
    return data, piece_info, id_dict, max_job_height

def handle_setup_file(setup_file: str, job_list: list):
    """
    Handle the setup file
    """
    max_time = 0 # max time for a setup
    setup_rule = {}
    num_col = 0
    num_job = 0
    cur_col = [0, None]
    cur_job = 0
    first_line = True
    with open(setup_file, encoding='utf-8-sig') as file:
        for line in csv.reader(file):
            if first_line:
                first_line = False
                num_col = int(line[1])
                num_job = int(line[3])
            else:
                if cur_col[0] > num_col:
                    break
                if cur_job == 0:
                    cur_col[1] = line[0]
                    setup_rule[line[0]] = {}
                    for i in job_list:
                        setup_rule[line[0]][i] = {}
                        for j in job_list:
                            setup_rule[line[0]][i][j] = 0
                    cur_job += 1
                else:
                    job_name = line[0]
                    for i in range(1, len(line)):
                        setup_rule[cur_col[1]][job_name][job_list[i - 1]] = int(line[i])
                        if int(line[i]) > max_time:
                            max_time = int(line[i])
                    cur_job += 1
                    if cur_job > num_job:
                        cur_job = 0
                        cur_col[0] += 1
    file.close()
    return setup_rule, max_time

def get_job_model(lst: list, order: list):
    """
    Get the job nparray model from the list of job info.
    """
    pointer = 0
    int_order = deque()
    col = sum([int(i) for i in lst])
    shape = np.zeros((len(lst), col), dtype=int)
    for i in order:
        i = int(i)
        int_order.append(i)
        cur_row = shape[i - 1]
        cur_len = int(lst[i - 1])
        for j in range(cur_len):
            cur_row[pointer + j] = 1
        pointer += cur_len
    return int_order, shape, col