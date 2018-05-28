from TypeEnum import *
from pygame import *


class Map(object):

    def __init__(self, row, column):

        self.MapRow = row
        self.MapColumn = column
        self.Grid = []
        self.TileWidth = 64
        self.TileHeight = 64
        self.TileMargin = 4

        for Row in range(self.MapRow):
            self.Grid.append([])
            for Column in range(self.MapColumn):
                self.Grid[Row].append([])
                self.Grid[Row][Column] = TypeEnum.EMPTY

    def update_map(self, coord, type):
        """
        Replace by empty and insert the type of object into the new location
        :param coord: Old and new coordinates of the object
        :param type: TypeEnum to update
        """
        self.Grid[coord.old_row][coord.old_column] = TypeEnum.EMPTY
        self.Grid[coord.row][coord.column] = type

    def check_collision(self, row, column, type):
        if self.Grid[row-1][column] != TypeEnum.EMPTY:
            self.Grid[row-1][column] = TypeEnum.EMPTY
            return True

    def is_first(self, row, column ):
        for i in range(row +1, self.MapRow -1):
            if self.Grid[i][column] != TypeEnum.EMPTY:
                return False

        return True