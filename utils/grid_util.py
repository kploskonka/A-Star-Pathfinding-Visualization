import pygame
from entity import Node
from utils import colors, validator
from utils.config import ROWS, SIZE, GAP
from queue import PriorityQueue


WINDOW = pygame.display.set_mode((SIZE, SIZE))

start = None
end = None


def guess_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, grid):
    while current in came_from:
        current = came_from[current]
        if current != start:
            current.make_path()
        draw(grid)


def a_star_algorithm(grid):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = guess_distance(start.get_position(), end.get_position())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, grid)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + guess_distance(neighbor.get_position(), end.get_position())

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw(grid)

        if current != start:
            current.make_closed()

    return False


def make_grid():
    grid = []

    for i in range(ROWS):
        grid.append([])
        for j in range(ROWS):
            node = Node.Node(i, j)
            grid[i].append(node)

    return grid


def draw_grid():
    for i in range(ROWS + 1):
        pygame.draw.line(WINDOW, colors.GREY, (0, i * GAP), (SIZE, i * GAP))

        for j in range(ROWS + 1):
            pygame.draw.line(WINDOW, colors.GREY, (j * GAP, 0), (j * GAP, SIZE))


def draw_node(node):
    pygame.draw.rect(WINDOW, node.color, (node.x, node.y, GAP, GAP))


def draw(grid):
    WINDOW.fill(colors.WHITE)

    for row in grid:
        for node in row:
            draw_node(node)

    draw_grid()
    pygame.display.update()


def get_clicked_position(position):
    y, x = position

    row = y // GAP
    column = x // GAP

    return row, column


def draw_on_position(mouse_position, grid):
    global start, end

    row, column = get_clicked_position(mouse_position)

    if validator.is_position_out_of_bounds(row, column):
        return

    node = grid[row][column]

    if start is None and node != end:
        start = node
        start.make_start()
    elif end is None and node != start:
        end = node
        end.make_end()
    elif node != end and node != start:
        node.make_barrier()


def reset_on_position(mouse_position, grid):
    global start, end

    row, column = get_clicked_position(mouse_position)
    if validator.is_position_out_of_bounds(row, column):
        return

    node = grid[row][column]

    if node.is_empty():
        return

    if node == start:
        start = None
    elif node == end:
        end = None

    node.clear()


def update_neighbors_for_all(grid):
    for row in grid:
        for node in row:
            node.update_neighbors(grid)


def clear():
    global start, end

    start = None
    end = None

    return make_grid()


def get_start():
    return start


def get_end():
    return end

