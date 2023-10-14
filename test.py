# import random
# from collections import deque, namedtuple
# import time
#
# from ale_py import ALEInterface
# import numpy as np
#
#
#
# def to_bits(n):
#         return [int(x) for x in np.binary_repr(n, 8)]
#
# def get_grid(ale: ALEInterface) -> np.ndarray:
#         grid = np.empty([22, 10], dtype=int)
#         screen = ale.getRAM()[0:44]
#         col = 0
#         for i in range(22):
#             cur = to_bits(screen[i])
#             for y in range(2, 8):
#                 grid[i][col] = cur[y]
#                 col += 1
#             col = 0
#
#         for i in range(22):
#             col = 6
#             cur = to_bits(screen[i+22])
#             for y in range(7, 3, -1):
#                 grid[i][col] = cur[y]
#                 col += 1
#         return grid
#
# # Get Grid.
# class Grid:
#     def __init__(self, ale: ALEInterface) -> None:
#         self.grid = get_grid(ale)
#         self.height = 0

import numpy as np
import random
from enum import IntEnum

TETROMINOS = {
    # 'I': np.array([[1, 1, 1, 1]]),
    # 'O': np.array([[1, 1], [1, 1]]),
    # 'T': np.array([[0, 1, 0], [1, 1, 1]]),
    # 'S': np.array([[0, 1, 1], [1, 1, 0]]),
    # 'Z': np.array([[1, 1, 0], [0, 1, 1]]),
    # 'J': np.array([[1, 0, 0], [1, 1, 1]]),
    # 'L': np.array([[0, 0, 1], [1, 1, 1]])
    '1': np.array([[1]]),
    '2': np.array([[1, 1]]),
    '3': np.array([[1, 0], [1, 1]]),
    '4': np.array([[1, 1], [1, 1]]),
    '5': np.array([[1, 0],[1, 1], [1, 1]]),

}

print(type(TETROMINOS.))




