import pygame
from utils import grid_util


def main():
    grid = grid_util.make_grid()

    is_running = True
    while is_running:
        grid_util.draw(grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            # LMB
            if pygame.mouse.get_pressed()[0]:
                mouse_position = pygame.mouse.get_pos()
                grid_util.draw_on_position(mouse_position, grid)

            # RMB
            elif pygame.mouse.get_pressed()[2]:
                mouse_position = pygame.mouse.get_pos()
                grid_util.reset_on_position(mouse_position, grid)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and grid_util.get_start() and grid_util.get_end():
                    grid_util.update_neighbors_for_all(grid)
                    grid_util.a_star_algorithm(grid)

                if event.key == pygame.K_c:
                    grid = grid_util.clear()

    pygame.quit()


main()
