import pygame

from pgu import gui as pgui
from colors import WHITE


def radio_button_action(args):
    model, value = args
    # 'manhattan' or 'euclidean'
    if value == 1:
        model.heuristic = 'manhattan'
    elif value == 2:
        model.heuristic = 'euclidean'


def create_radio_button(container, windos_size, model):
    font = pygame.font.SysFont("default", 30)

    rbt = pgui.Table()
    radio = pgui.Group()
    r_button1 = pgui.Radio(radio, 1)
    r_button1_label = pgui.Label(" Manhattan", font=font, color=WHITE)
    rbt.add(r_button1)
    rbt.add(r_button1_label)
    rbt.tr()
    r_button2 = pgui.Radio(radio, 2)
    r_button2_label = pgui.Label("Euclidean", font=font, color=WHITE)
    rbt.add(r_button2)
    rbt.add(r_button2_label)
    rbt.tr()
    container.add(rbt, 20, windos_size[1] - 50)  # coordinate (x, y)
    radio.value = 1
    radio.connect(pgui.CHANGE, radio_button_action, (model, radio.value))


def start_button_action(model):
    model.search()


def random_button_action(args):
    model, ratio = args
    model.set_random_walls(ratio)


def reset_button_action(model):
    model.init_algorithm()


def create_button(container, window_size, model, obstacle_ratio=0.2):
    font = pygame.font.SysFont("default", 30)

    start_button = pgui.Button("Start A* Search", width=50, height=30, font=font)
    start_button.connect(pgui.CLICK, start_button_action, model)

    random_button = pgui.Button("Random walls", width=50, height=30, font=font)
    random_button.connect(pgui.CLICK, random_button_action, (model, obstacle_ratio))

    reset_button = pgui.Button("Reset", width=50, height=30, font=font)
    reset_button.connect(pgui.CLICK, reset_button_action, model)

    container.add(start_button, 200, window_size[1] - 45)
    container.add(random_button, 400, window_size[1] - 45)
    container.add(reset_button, 600, window_size[1] - 45)
