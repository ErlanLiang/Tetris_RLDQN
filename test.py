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

for i in range(1, 2):
    print("1")




