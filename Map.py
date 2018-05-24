from TypeEnum import *


class Map(object):

    def __init__(self, row, column):
        self.MapRow = row
        self.MapColumn = column
        self.Grid = []
        # Creating grid
        for Row in range(self.MapRow):
            self.Grid.append([])
            for Column in range(self.MapColumn):
                self.Grid[Row].append([])
                self.Grid[Row][Column] = TypeEnum.EMPTY

    def update_map(self, row, column, mtype):
        self.Grid[row][column] = mtype
