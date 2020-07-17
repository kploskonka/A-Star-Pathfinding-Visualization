import pygame
from utils import colors, config, validator
from entity import Node

SIZE = config.SIZE
ROWS = config.ROWS
GAP = config.GAP

WINDOW = pygame.display.set_mode((SIZE, SIZE))

start = None
end = None


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

    if node.is_start():
        start = None
    elif node.is_end():
        end = None

    node.reset()


def main():
    grid = make_grid()

    is_running = True
    while is_running:
        draw(grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            # LMB
            if pygame.mouse.get_pressed()[0]:
                mouse_position = pygame.mouse.get_pos()
                draw_on_position(mouse_position, grid)

            # RMB
            elif pygame.mouse.get_pressed()[2]:
                mouse_position = pygame.mouse.get_pos()
                reset_on_position(mouse_position, grid)

    pygame.quit()


main()
