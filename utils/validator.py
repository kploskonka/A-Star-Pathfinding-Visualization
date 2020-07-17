from utils.config import ROWS


def is_position_out_of_bounds(row, column):
    return not (ROWS - 1 > row > 0 and ROWS - 1 > column > 0)
