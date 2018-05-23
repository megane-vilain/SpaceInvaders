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

