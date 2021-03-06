from utils import colors, validator
from utils.config import GAP


class Node:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.x = row * GAP
        self.y = column * GAP
        self.color = colors.WHITE
        self.neighbors = []

    def is_barrier(self):
        return self.color == colors.BLACK

    def is_start(self):
        return self.color == colors.ORANGE

    def is_end(self):
        return self.color == colors.TURQUOISE

    def is_empty(self):
        return self.color == colors.WHITE

    def is_path(self):
        return self.color == colors.PURPLE

    def is_open(self):
        return self.color == colors.GREEN

    def is_closed(self):
        return self.color == colors.RED

    def reset(self):
        self.color = colors.WHITE

    def make_barrier(self):
        self.color = colors.BLACK

    def make_start(self):
        self.color = colors.ORANGE

    def make_end(self):
        self.color = colors.TURQUOISE

    def make_path(self):
        self.color = colors.PURPLE

    def make_open(self):
        self.color = colors.GREEN

    def make_closed(self):
        self.color = colors.RED

    def clear(self):
        self.color = colors.WHITE

    def lower_neighbor(self, grid):
        return grid[self.row + 1][self.column]

    def upper_neighbor(self, grid):
        return grid[self.row - 1][self.column]

    def right_neighbor(self, grid):
        return grid[self.row][self.column + 1]

    def left_neighbor(self, grid):
        return grid[self.row][self.column - 1]

    def update_neighbors(self, grid):
        if validator.is_position_out_of_bounds(self.row, self.column):
            return

        self.neighbors = []

        if not self.lower_neighbor(grid).is_barrier():
            self.neighbors.append(self.lower_neighbor(grid))

        if not self.upper_neighbor(grid).is_barrier():
            self.neighbors.append(self.upper_neighbor(grid))

        if not self.right_neighbor(grid).is_barrier():
            self.neighbors.append(self.right_neighbor(grid))

        if not self.left_neighbor(grid).is_barrier():
            self.neighbors.append(self.left_neighbor(grid))

    def get_position(self):
        return self.row, self.column
