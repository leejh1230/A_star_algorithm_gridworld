import argparse

from pygame.locals import *
from A_star_algorithm import *
from button_utils import *

parser = argparse.ArgumentParser(description='Grid World Property.')
parser.add_argument('--M', type=int, default=30, help='the number of rows of grid.')
parser.add_argument('--N', type=int, default=30, help='the number of columns of grid.')
parser.add_argument('--obstacle_ratio', default=0.2, help='the proportion of obstacles in grid world.')

args = parser.parse_args()

TARGET_FPS = 60  # Frame per second.

WINDOW_SIZE = [800, 800]

screen = None


def init_pygame():
    global screen
    pygame.init()
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('A* Algorithm')


def run():
    global screen
    init_pygame()

    QUIT = False
    dragging = False
    state = 'obstacle'

    model = AStarAlgorithm([WINDOW_SIZE[0], WINDOW_SIZE[1] - 50], args.M, args.N)
    model.init_algorithm()

    clock = pygame.time.Clock()

    app = pgui.App()
    container = pgui.Container(width=800)  # 가운데 정렬..
    create_radio_button(container, WINDOW_SIZE, model)
    create_button(container, WINDOW_SIZE, model, args.obstacle_ratio)

    app.init(container)

    while not QUIT:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QUIT = True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                QUIT = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # if click left button on mouse.
                if event.button == 1:
                    dragging = True
                    pos = pygame.mouse.get_pos()
                    state = model.block_click(pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    pos = pygame.mouse.get_pos()
                    model.block_drag(pos, state)
            app.event(event)
        model.draw_grid(screen)
        app.paint(screen)
        clock.tick(TARGET_FPS)

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    run()
