import pygame
import math

from grid import GridWorld
from colors import *


class AStarAlgorithm(GridWorld):
    def __init__(self, world_size, rows, cols, margin=1):
        super(AStarAlgorithm, self).__init__(world_size, rows, cols, margin)

        self.heuristic = 'manhattan'        # 'manhattan' or 'euclidean'
        self.path_list = []

        self.open_list = None
        self.close_list = None
        self.cost_grid = None

        self.init_grid()

    def init_algorithm(self, init_grid=True):
        if init_grid:
            self.init_grid()

        cost_grid = []
        for row in range(self.rows):
            cost_grid.append([])
            for col in range(self.cols):
                # parent_pos : [row, col]
                parent_pos = [float('inf'), float('inf')]

                # costs : [F, G, H, parent_pos]
                costs = [float('inf'), float('inf'), float('inf'), parent_pos]
                cost_grid[row].append(costs)

                state = self.grid[row][col]['state']
                if state == 'open' or state == 'close':
                    self.grid[row][col]['state'] = 'load'

        self.path_list = []
        self.open_list = []
        self.close_list = []
        self.cost_grid = cost_grid

    def get_heuristic(self, pos):
        if self.heuristic == 'manhattan':
            d_y = abs(pos[0] - self.goal_pos[0])
            d_x = abs(pos[1] - self.goal_pos[1])
            return 10. * (d_x + d_y)
        elif self.heuristic == 'euclidean':
            distance = math.sqrt(math.pow(pos[0] - self.goal_pos[0], 2) + math.pow(pos[1] - self.goal_pos[1], 2))
            distance *= 10.
            return distance
        else:
            raise Exception("Wrong heuristic!!!")

    def get_minimum_f_pos(self):
        if self.open_list:
            min_f_node = self.open_list[0]
            for node in self.open_list:
                f = self.cost_grid[node[0]][node[1]][0]
                min_f = self.cost_grid[min_f_node[0]][min_f_node[1]][0]
                if f <= min_f:
                    min_f_node = node

            return True, min_f_node
        else:
            # No path.
            return False, None

    def get_minimum_f_pos_in_close_list(self):
        if self.close_list:
            if self.goal_pos in self.close_list:
                raise Exception("Goal is in close list.")
            else:
                min_f_node = self.close_list[0]
                for node in self.close_list:
                    f = self.cost_grid[node[0]][node[1]][0]
                    min_f = self.cost_grid[min_f_node[0]][min_f_node[1]][0]
                    if f <= min_f:
                        min_f_node = node

                return min_f_node
        else:
            raise Exception("Close list is Empty!!")

    def get_center_coordinate(self, rect_pos):
        row, col = rect_pos
        x = (self.margin + self.cell_width) * col + self.margin
        x += self.cell_width // 2
        y = (self.margin + self.cell_height) * row + self.margin
        y += self.cell_height // 2

        return [x, y]

    def search(self):
        self.init_algorithm(False)

        self.open_list.append(self.start_pos)
        h = self.get_heuristic(self.start_pos)
        self.cost_grid[self.start_pos[0]][self.start_pos[1]] = [h, 0, h, None]
        result, pos = self.get_minimum_f_pos()

        path = False

        if not result:
            raise Exception("Something wrong with start node.")
        elif pos == self.goal_pos:
            raise Exception("Start node is Goal node..??")

        final_pos = None
        while True:
            self.check_neighbor(pos)

            result, pos = self.get_minimum_f_pos()

            if not result:
                print("NO Path!!!")
                final_pos = self.get_minimum_f_pos_in_close_list()
                break
            elif pos == self.goal_pos:
                final_pos = self.goal_pos
                path = True
                break

            self.grid[pos[0]][pos[1]]['state'] = 'close'

        self.find_path(final_pos)
        if path:
            print("The number of explored nodes : {}".format(len(self.path_list) - 2))

    def find_path(self, final_pos):
        path_list = []
        pos = final_pos
        while True:
            center_coordinate = self.get_center_coordinate(pos)
            path_list.append(center_coordinate)
            parent_pos = self.cost_grid[pos[0]][pos[1]][3]

            if not parent_pos:
                break
            else:
                if parent_pos not in self.close_list:
                    raise Exception("error: Can not find path..!!")
                pos = parent_pos

        self.path_list = path_list

    def check_neighbor(self, pos):
        """
        :param pos: pos of selected node. -> [row, col]
        """
        row, col = pos

        # [east, west, south, north]
        nebr_list = [[row, col + 1], [row, col - 1], [row - 1, col], [row + 1, col]]

        for nebr in nebr_list:
            nebr_row, nebr_col = nebr
            if 0 <= nebr_row <= self.rows - 1 and 0 <= nebr_col <= self.cols - 1:
                if self.grid[nebr_row][nebr_col]['state'] != 'obstacle':
                    if nebr not in self.close_list:

                        g = self.cost_grid[row][col][1]
                        if nebr in self.open_list:
                            nebr_g = self.cost_grid[nebr_row][nebr_col][1]
                            new_nebr_g = g + 10.   # 현재 노드를 거쳐가는 비용
                            if new_nebr_g < nebr_g:
                                nebr_h = self.cost_grid[nebr_row][nebr_col][2]
                                self.cost_grid[nebr_row][nebr_col] = [new_nebr_g + nebr_h, new_nebr_g,
                                                                      nebr_h, [row, col]]
                        else:
                            nebr_g = g + 10.
                            nebr_h = self.get_heuristic(nebr)
                            nebr_f = nebr_g + nebr_h
                            self.cost_grid[nebr_row][nebr_col] = [nebr_f, nebr_g, nebr_h, [row, col]]
                            self.open_list.append(nebr)
                            if nebr != self.goal_pos:
                                self.grid[nebr_row][nebr_col]['state'] = 'open'     # goal 의 색 변경 방지

        self.open_list.remove(pos)
        self.close_list.append(pos)

    def draw_grid(self, screen):
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
                elif state == 'close':
                    color = SKY
                elif state == 'open':
                    color = WHITE_GREEN
                else:
                    print("Wrong state in {0}, {1}".format(row, col))
                    exit(0)
                # rect_grid[row][col].inflate_ip(3, 3)
                pygame.draw.rect(screen, color, self.grid[row][col]['rect'])

        if len(self.path_list) >= 2:
            pygame.draw.lines(screen, YELLOW, False, self.path_list, 2)
