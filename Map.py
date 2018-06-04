from TypeEnum import *
from pygame import *


class Map(object):

    def __init__(self, row, column):

        self.row_number = row
        self.column_number = column
        self.grid = []
        self.tile_width = 64
        self.tile_height = 64
        self.tile_margin = 4

        self.init_map()

    def init_map(self):
        for row in range(self.row_number):
            self.grid.append([])
            for column in range(self.column_number):
                self.grid[row].append([])
                self.grid[row][column] = TypeEnum.EMPTY

    def update_map(self, coord, type):
        """
        Replace by empty and insert the type of object into the new location
        :param coord: Old and new coordinates of the object
        :param type: TypeEnum to update
        """
        self.grid[coord.old_row][coord.old_column] = TypeEnum.EMPTY
        self.grid[coord.row][coord.column] = type

    def get_row_string(self, row):
        line = ""
        for column in range(self.column_number):
            line += str(self.grid[row][column].value)
        return line

    def is_enemy_first(self, row, column):
        for row in range(row + 1, self.row_number):

            if self.grid[row][column] == TypeEnum.ENEMY:
                return False

        return True

    def check_boundaries(self):
        for row in range(0, self.row_number):
            if self.grid[row][0] == TypeEnum.ENEMY or self.grid[row][13] == TypeEnum.ENEMY:
                return True

        return False
