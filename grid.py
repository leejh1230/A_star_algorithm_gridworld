import pygame
import random
from colors import *


class GridWorld:
    def __init__(self, world_size, rows, cols, margin=1):
        self.rows = rows
        self.cols = cols
        self.margin = margin

        self.cell_width = world_size[0] // cols - margin
        self.cell_height = world_size[1] // rows - margin
        self.world_size = [(self.cell_width + margin) * cols, (self.cell_height + margin) * rows]

        self.start_pos = [rows // 2, 0]
        self.goal_pos = [rows // 2, cols - 1]
        self.grid = None
        self.back_rect = None

        self.previous_pos = [0, 0]

    def init_grid(self):
        grid = []
        for row in range(self.rows):
            grid.append([])
            for col in range(self.cols):
                rect_dict = {'rect': pygame.Rect([(self.margin + self.cell_width) * col + self.margin,
                                                  (self.margin + self.cell_height) * row + self.margin,
                                                  self.cell_width,
                                                  self.cell_height]),
                             'state': 'load',
                             'event': 0}
                grid[row].append(rect_dict.copy())

        grid[self.start_pos[0]][self.start_pos[1]]['state'] = 'start'
        grid[self.goal_pos[0]][self.goal_pos[1]]['state'] = 'goal'

        back_height = self.rows * (self.cell_height + self.margin) + self.margin
        back_width = self.cols * (self.cell_width + self.margin) + self.margin

        back_rect = {'rect': pygame.Rect([0, 0, back_width, back_height])}

        self.grid = grid
        self.back_rect = back_rect

    def get_block_pos(self, pos):
        col = pos[0] // (self.cell_width + self.margin)
        row = pos[1] // (self.cell_height + self.margin)

        return row, col

    def check_block(self):
        """
        self.start_pos 나 self.goal_pos 의 좌표와
        self.grid 내의 'start', 'goal' 좌표가 다른 경우, 예외 발생.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                state = self.grid[row][col]['state']
                if state == 'start':
                    assert [row, col] == [self.start_pos[0], self.start_pos[1]]
                elif state == 'goal':
                    assert [row, col] == [self.goal_pos[0], self.goal_pos[1]]

    def draw_grid(self, screen):
        # Screen 백그라운드 설정
        screen.fill(GRAY2)
        pygame.draw.rect(screen, BLACK, self.back_rect['rect'])

        # Draw the grid
        for row in range(self.rows):
            for col in range(self.cols):
                state = self.grid[row][col]['state']
                color = None
                if state == 'load':
                    color = WHITE
                elif state == 'obstacle':
                    color = GRAY
                elif state == 'start':
                    color = GREEN
                elif state == 'goal':
                    color = RED
                else:
                    print("Wrong state in {0}, {1}".format(row, col))
                    exit(0)
                # rect_grid[row][col].inflate_ip(3, 3)
                pygame.draw.rect(screen, color, self.grid[row][col]['rect'])

    def block_click(self, pos):
        """
        :param pos: current mouse coordinate.
        :return: state which the current block must be changed.
        """
        if pos[0] < self.world_size[0] and pos[1] < self.world_size[1]:

            row, col = self.get_block_pos(pos)
            rect_dict = self.grid[row][col]

            self.previous_pos = [row, col]

            if rect_dict['state'] == 'start':
                return 'start'
            elif rect_dict['state'] == 'goal':
                return 'goal'
            elif rect_dict['state'] == 'load':
                rect_dict['state'] = 'obstacle'
            elif rect_dict['state'] == 'obstacle':
                rect_dict['state'] = 'load'

            self.check_block()

            return rect_dict['state']

    def block_drag(self, pos, state):
        """
        :param pos: current mouse coordinate.
        :param state: state which the current block must be changed.
        :return:
        """
        if pos[0] < self.world_size[0] and pos[1] < self.world_size[1]:
            row, col = self.get_block_pos(pos)
            pre_row, pre_col = self.previous_pos
            if [pre_row, pre_col] != [row, col]:     # 마우스가 다른 block 으로 이동했는가
                rect_dict = self.grid[row][col]
                cur_block_state = rect_dict['state']

                pre_rect_dict = self.grid[pre_row][pre_col]

                if state == 'load' or state == 'obstacle':      # drag 'load' or 'obstacle' block.
                    if cur_block_state == 'load' or cur_block_state == 'obstacle':
                        rect_dict['state'] = state
                        self.previous_pos = [row, col]

                elif state == 'start':              # drag the 'start' block.
                    if cur_block_state == 'load':
                        rect_dict['state'] = state
                        pre_rect_dict['state'] = 'load'
                        self.start_pos = [row, col]
                        self.previous_pos = [row, col]

                elif state == 'goal':               # drag the 'goal' block.
                    if cur_block_state == 'load':
                        rect_dict['state'] = state
                        pre_rect_dict['state'] = 'load'
                        self.goal_pos = [row, col]
                        self.previous_pos = [row, col]

            self.check_block()

    def set_random_walls(self, obstacle_ratio=0.2):
        self.init_grid()

        rect_list = []
        for row in range(self.rows):
            for col in range(self.cols):
                rect_list.append([row, col])

        random.shuffle(rect_list)
        nof_grid = (self.cols + 1) * (self.rows + 1)
        nof_obstacle = int(obstacle_ratio * nof_grid)

        rect_list = rect_list[:nof_obstacle]

        for rect_row, rect_col in rect_list:
            if [rect_row, rect_col] != self.start_pos and [rect_row, rect_col] != self.goal_pos:
                self.grid[rect_row][rect_col]['state'] = 'obstacle'

