from enum import IntEnum
import numpy as np
import csv
from collections import deque

JOB_DATA: dict
SETUP_RULE: dict
NUM_TYPE: int
NUM_COL: int
JOB_TYPE_PATH = "./data/type_info.csv"
JOB_INFO_PATH = "./data/job_info.csv"
SETUP_PATH = "./data/setup_info.csv"
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
    COMMIT = 10

class Job:
    id: int
    name: str
    order: deque
    shape: np.ndarray
    fix_shape: np.ndarray
    curr_height: int

    def __init__(self, name: str):
        self.name = name
        self.order = JOB_DATA[name][0].copy()          # Order of the columns
        self.shape = JOB_DATA[name][1].copy()          # Shape of the job piece
        self.id = JOB_DATA[name][2]                    # ID of the job piece
        self.fix_shape = np.rot90(self.shape)          # Fixed shape of the job piece
        self.curr_height = 0                           # Current height of the job piece, drop part can not be lower than this height

    
    def update_drop_block(self, height: int):
        """
        Drop one part of the job piece into the grid,
        update the parameters of the job piece.
        """
        # Update the shape, order of the job piece and the height
        zero = np.zeros(1, self.shape.shape[1])
        self.shape[self.order.popleft()] = zero
        self.fix_shape = np.rot90(self.shape)
        self.curr_height = height  


class ScheduleGrid:
    HEIGHT: int
    WIDTH: int
    grid: np.ndarray
    curr_top: list[str]
    curr_height: list[int]
    
    def __init__(self, width: int, height: int):
        self.HEIGHT = height
        self.WIDTH = width
        self.grid = np.zeros(
            (self.HEIGHT, self.WIDTH), dtype=int) # Grid of the schedule

        self.curr_top = [None] * self.WIDTH       # Current top of the grid job piece type
        self.curr_height = [1] * self.WIDTH       # Current height of the grid
    
class ScheduleModel:
    HEIGHT: int
    WIDTH: int
    data: deque
    curr_time: int
    curr_job: list[Job]
    num_pieces: int
    grid: ScheduleGrid
    picked_job: int
    grid_history: np.ndarray

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
        self.HEIGHT = 22 + MAX_SETUP_TIME         # Height of the grid(including hidden rows(MAX_SETUP_TIME))
        self.grid = ScheduleGrid(self.WIDTH, self.HEIGHT)

        self.curr_time = -1                       # Current time of the grid
        self.curr_job = []                        # Current time's job of the grid
        self.picked_job = 0                       # Picked job of the grid

    def start_game(self):
        """
        Start the game.
        """
        self.add_time()
    
    def add_time(self):
        """
        Time goes by one unit.
        update the current time of the grid and the current job.
        """
        self.curr_time += 1
        time = str(self.curr_time)

        # Update all current job's height
        for i in self.curr_job:
            if i.curr_height != 0:
                i.curr_height -= 1

        # Add new job to the current job list
        while self.data and self.data[0][2] == time:
            self.curr_job.append(Job(self.data.popleft()[1]))

        # current height all minus 1
        self.grid.curr_height = [i - 1 for i in self.grid.curr_height]

        # Update the grid by deleting the bottom row  
    
    def execute_move(self, action: ScheduleAction):
        """
        Execute the move of the game.
        """
        # pass
        if action == ScheduleAction.PROGRESS:
            self.add_time()
        elif action == ScheduleAction.COMMIT:
            self.commit()
        else:
            self.select(action)
        
    def commit(self):
        """
        Commit the current job to the grid.
        """
        pass

    def select(self, action: ScheduleAction):
        """
        Select the current job.
        """
        pass


# initialize function below
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




