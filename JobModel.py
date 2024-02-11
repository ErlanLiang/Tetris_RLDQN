import numpy as np
import csv
from collections import deque
from enum import IntEnum

JOB_DATA: dict
SETUP_RULE: dict
NUM_TYPE: int
NUM_COL: int
JOB_TYPE_PATH = "./data/type_info.csv"
JOB_INFO_PATH = "./data/job_info.csv"
SETUP_PATH = "./data/setup.csv"
MAX_SETUP_TIME: int

def initialize_job_data():
    global JOB_DATA, NUM_TYPE, NUM_COL, MAX_SETUP_TIME, SETUP_RULE

    JOB_DATA, piece_info = handle_type_info_file          #JOB_DATA[job name]  
    (JOB_TYPE_PATH)                                       # = [order(colum order), shape(nparay model)]

    SETUP_RULE, MAX_SETUP_TIME = handle_setup_file        #SETUP_RULE[colum][from job][to job]
    (SETUP_PATH, list(JOB_DATA.keys()))                   # = time(int)

    NUM_TYPE = int(piece_info[0][1])                      # Number of types of job

    NUM_COL = int(piece_info[0][3])                       # Number of columns

class ScheduleGrid:
    HEIGHT: int

    def __init__(self):
        self.data = deque()                       # Data of upcoming job of the schedule
        with open(JOB_INFO_PATH, encoding='utf-8-sig') as file:
            for line in csv.reader(file):
                self.data.append(line)
        file.close()
        grid_info = self.data.popleft()
        self.data.popleft()

        self.num_pieces = int(grid_info[1])       # Number of pieces
        self.WIDTH = int(grid_info[3])            # Width of the grid(M)
        self.HEIGHT = 22 + MAX_SETUP_TIME         # Height of the grid(including hidden rows(MAX_SETUP_TIME))
        self.grid = np.zeros(
            (self.HEIGHT, self.WIDTH), dtype=int) # Grid of the schedule

        self.curr_top = [None] * self.WIDTH       # Current top of the grid job piece type
        self.curr_height = [0] * self.WIDTH       # Current height of the grid
        self.curr_time = 0                        # Current time of the grid
        self.curr_job = []                        # Current time's job of the grid
    
    def addtime(self):
        """
        Time goes by one unit.
        update the current time of the grid and the current job.
        """
        self.curr_time += 1
        time = str(self.curr_time)

        # Add new job to the current job list
        while self.data[0][2] == time:
            self.curr_job.append(Job(self.data.popleft()[1]))

        # current height all minus 1
        self.curr_height = [i - 1 for i in self.curr_height]

        # Update the grid 





class Job:

    def __init__(self, name: str):
        self.name = name
        self.order = JOB_DATA[name][0].copy() # Order of the columns
        self.shape = JOB_DATA[name][1].copy() # Shape of the job piece
    
    def drop(self):
        """
        Drop one part of the job piece into the grid,
        update the shape and order of the job piece.
        """
        pass


    

def handle_type_info_file(type_info_file: str):
    """
    Handle the type info file and 
    return the job model and the piece info.
    """
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
                    order, shape = get_job_model(cur_data, order)
                    data[key] = [order, shape]
    file.close()
    return data, piece_info

def handle_setup_file(setup_file: str, job_list: list):
    """
    Handle the setup file, return the setup rule 
    with a nested dictionary and the max setup time.
    """
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
                    cur_job += 1
                    if cur_job > num_job:
                        cur_job = 0
                        cur_col[0] += 1
    file.close()
    return setup_rule

def get_job_model(lst: list, order: list):
    """
    Get the job nparray model from the list of job info.
    """
    pointer = 0
    int_order = []
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
    return int_order, shape


