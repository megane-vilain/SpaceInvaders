from TypeEnum import *


class Map(object):

    def __init__(self, row, column):

        self.MapRow = row
        self.MapColumn = column
        self.Grid = []

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
