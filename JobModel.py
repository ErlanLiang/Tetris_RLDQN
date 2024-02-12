from enum import IntEnum
import numpy as np
import csv
from collections import deque

JOB_TYPE_PATH = "./tests/type_info.csv"
JOB_INFO_PATH = "./tests/job_info.csv"
SETUP_PATH = "./tests/setup_info.csv"
GRID_BASE_HEIGHT = 10

job_data: dict
setup_rule: dict
num_types: int
num_cols: int
max_setup_time: int
job_id: dict # job id -> job name
max_job_height: int

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
    id: int                         # ID of the job, used for drawing the grid with different colors
    job_type: str                   # Type of the job
    pieces: deque                   # Order of the columns to be dropped
    shape: np.ndarray               # Shape of the job
    rotated_shape: np.ndarray       # Fixed shape of the job for drawing
    lowest_time: int                # The lowest time of the next job piece to be dropped

    def __init__(self, name: str, time: int = 0):
        self.job_type = name
        self.pieces = job_data[name][0].copy()          # Order of the columns
        self.shape = job_data[name][1].copy()           # Shape of the job
        self.id = job_data[name][2]                     # ID of the job
        self.rotated_shape = np.rot90(self.shape)       # Fixed shape of the job
        self.lowest_time = time                         # The lowest time of the next job piece to be dropped

    def drop_block(self):
        """
        Drop one part of the job piece into the grid,
        update the parameters of the job piece.
        """
        # Update the shape, order of the job piece and the height
        drop_col = self.pieces.popleft() - 1
        col_len = np.sum(self.shape[drop_col], axis=0) # length of 1 the column

        # update the shape of the job piece
        self.shape[drop_col] = np.zeros((1, self.shape.shape[1]), dtype=int)
        self.rotated_shape = np.rot90(self.shape)

        return col_len, drop_col
        

class ScheduleGrid:
    HEIGHT: int
    WIDTH: int
    grid: np.ndarray
    
    def __init__(self, width: int, height: int):
        self.HEIGHT = height
        self.WIDTH = width
        self.grid = np.zeros((self.HEIGHT, self.WIDTH), dtype=int)  # Grid of the schedule

    
class ScheduleModel:
    pending_jobs: deque
    curr_time: int
    job_list: list[Job]
    num_jobs: int
    grid: ScheduleGrid

    def __init__(self):
        # Initialize the job data
        initialize_job_data()                       # Initialize the job data

        # Read the jobs from the file
        self.pending_jobs = deque()
        with open(JOB_INFO_PATH, encoding='utf-8-sig') as file:
            for line in csv.reader(file):
                self.pending_jobs.append(line)

        # Set up the grid
        grid_info = self.pending_jobs.popleft()     # Get grid info from the first line of the file
        self.pending_jobs.popleft()                 # Remove the second line of the file
        self.num_jobs = int(grid_info[1])         # Number of jobs
        width = int(grid_info[3])                   # Width of the grid(M)
        height = GRID_BASE_HEIGHT + max_setup_time  # Height of the grid(including hidden rows(MAX_SETUP_TIME))
        self.grid = ScheduleGrid(width, height)     # Initialize the grid

        self.curr_time = -1                         # Current time of the grid
        self.job_list = []                          # Current time's job of the grid

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
        for i in self.job_list:
            if i.lowest_time != max_job_height:
                i.lowest_time -= 1

        # Add new job to the current job list
        while self.pending_jobs and self.pending_jobs[0][2] == time:
            self.job_list.append(Job(self.pending_jobs.popleft()[1], self.curr_time))       

        # Update the grid by deleting the bottom row  
        self.remove_bottom()
    
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
        Commit the current job to the grid.
        """
        if action > len(self.job_list):
            return
        job = self.job_list[action - 1]
        drop_len, drop_col = job.drop_block()
        cur_top = self.grid.curr_top[drop_col]
        cur_height = self.grid.curr_height[drop_col]
        print("current top: ", cur_top)
        # get the setup time
        setup_time = 0
        is_bottom = False
        if cur_top:
            col_str = "M" + str(drop_col + 1) 
            setup_time = setup_rule[col_str][cur_top][job.job_type]

        # Handle height after drop > grid height
        rows_needed = max(cur_height, job.lowest_time) + setup_time + drop_len - self.grid.HEIGHT + 1
        print("rows needed: ", rows_needed)
        if rows_needed > 0:
            for i in range(rows_needed):
                self.add_time()
                cur_height -= 1
        
        if setup_time:
            # add setup time to the grid
            is_bottom = self.add_setup_time(setup_time, drop_col, cur_height)

        # update the grid             !!!! Still need to handle if the height is higher than the grid height
        print("current height: ", cur_height, "setup: ", setup_time,  "job height: ", job.lowest_time, "drop len: ", drop_len)
        if cur_height + setup_time < job.lowest_time:
            self.update_grid(drop_col, job.lowest_time, job, drop_len, is_bottom)
        else:
            self.update_grid(drop_col, cur_height + setup_time, job, drop_len, is_bottom)

        # check if the job is finished if so, remove it from the current job list, 
        # else update the current height
        if not job.pieces:
            self.job_list.pop(action - 1)
        else:
            job.lowest_time = self.grid.curr_height[drop_col]

        # check the game status
        self.check_status()
        
    def add_setup_time(self, setup_time: int, col: int, height: int):
        """
        Add the setup time to the grid.
        """
        is_bottom = False
        print("add setup time")
        print("height: ", height)
        if height == max_setup_time - 1:
            is_bottom = True
        for i in range(setup_time):
            self.grid.grid[height + 1 + i][col] = 1
        return is_bottom
    
    def update_grid(self, col: int, height: int, job: Job, drop_len: int, is_bottom: bool):
        """
        Update the grid by adding the job piece to the grid.
        """
        print("update grid")
        print("height: ", height)
        if height == max_setup_time and not is_bottom:
            height -= 1
        for i in range(drop_len):
            self.grid.grid[height + i + 1][col] = job.id
        self.grid.curr_top[col] = job.job_type
        self.grid.curr_height[col] = height + drop_len
    
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
            print("bottom line is full")
            self.add_time()
            bottom_full = self.check_bottom_full()
        
        # check if the current job list is empty
        while not self.job_list:
            print("current job list is empty")
            self.add_time()

    def check_bottom_full(self):
        """
        Check if the bottom line is full.
        """
        for i in self.grid.grid[max_setup_time]:
            if i == 0:
                return False
        return True
    
    def remove_bottom(self):
        """
        Remove the bottom row of the grid, store the row into the hidden row,
        check the hidden row is full or not, if so, store the hidden row into the grid history.
        """
        # pop the bottom row, and all the rows above it move down one row, and the top row is all 0
        bottom = self.grid.grid[max_setup_time]
        
        self.grid.grid = np.delete(self.grid.grid, max_setup_time, axis=0)
        
        self.grid.grid = np.insert(self.grid.grid, self.grid.HEIGHT - 1, np.zeros(self.grid.WIDTH), axis=0)

        # store the bottom row into the hidden row
        hidden_bottom = self.grid.grid[0]
        # print("current grid:")
        # print(self.grid.grid)
        self.grid.grid = np.delete(self.grid.grid, 0, axis=0)
        # print("after delete:")
        # print(self.grid.grid)
        self.grid.grid = np.insert(self.grid.grid, max_setup_time - 1, bottom, axis=0)
        # print("hidden bottom changed:")
        # print(self.grid.grid)


def initialize_job_data():
    global job_data, num_types, num_cols, max_setup_time, setup_rule, job_id, max_job_height

    #JOB_DATA[job name] = [order(deque colum order), shape(nparray model), job id(int)]
    job_data, piece_info, job_id, max_job_height = handle_type_info_file(JOB_TYPE_PATH)                                                                    

    #SETUP_RULE[colum][from job][to job] = setup time(int)
    setup_rule, max_setup_time = handle_setup_file(SETUP_PATH, list(job_data.keys()))

    num_types = int(piece_info[0][1])  # Number of types of job

    num_cols = int(piece_info[0][3])   # Number of columns

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




