import pygame

WIDTH = 800
ROWS = 50
GAP = WIDTH // ROWS

WINDOW = pygame.display.set_mode((WIDTH, WIDTH))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

start = None
end = None


class Node:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.x = row * GAP
        self.y = column * GAP
        self.color = WHITE
        self.neighbors = []

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def is_empty(self):
        return self.color == WHITE

    def reset(self):
        self.color = WHITE

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def draw(self):
        pygame.draw.rect(WINDOW, self.color, (self.x, self.y, GAP, GAP))

    def lower_neighbor(self, grid):
        return grid[self.row + 1][self.column]

    def upper_neighbor(self, grid):
        return grid[self.row - 1][self.column]

    def right_neighbor(self, grid):
        return grid[self.row][self.column + 1]

    def left_neighbor(self, grid):
        return grid[self.row][self.column - 1]

    def is_position_out_of_bounds(self):
        return not (ROWS - 1 > self.row > 0 and ROWS - 1 > self.column > 0)

    def update_neighbors(self, grid):
        if self.is_position_out_of_bounds():
            return

        self.neighbors = []

        if not self.lower_neighbor(grid).is_barrier():
            self.neighbors.append(self.lower_neighbor(grid))

        if not self.upper_neighbor(grid).is_barrier():
            self.neighbors.append(self.upper_neighbor(grid))

        if not self.upper_neighbor(grid).is_barrier():
            self.neighbors.append(self.upper_neighbor(grid))

        if not self.left_neighbor(grid).is_barrier():
            self.neighbors.append(self.left_neighbor(grid))


def make_grid():
    grid = []

    for i in range(ROWS):
        grid.append([])
        for j in range(ROWS):
            node = Node(i, j)
            grid[i].append(node)

    return grid


def draw_grid():
    for i in range(ROWS):
        pygame.draw.line(WINDOW, GREY, (0, i * GAP), (WIDTH, i * GAP))

        for j in range(ROWS):
            pygame.draw.line(WINDOW, GREY, (j * GAP, 0), (j * GAP, WIDTH))


def draw(grid):
    WINDOW.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw()

    draw_grid()
    pygame.display.update()


def get_clicked_position(position):
    y, x = position

    row = y // GAP
    column = x // GAP

    return row, column


def draw_on_position(mouse_position, grid):
    global start, end

    row, col = get_clicked_position(mouse_position)
    node = grid[row][col]

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
    row, col = get_clicked_position(mouse_position)
    node = grid[row][col]

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
