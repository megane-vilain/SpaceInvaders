from ObjectBoard import *

class Ennemy(ObjectBoard):
    def __init__(self, row, column, image):
        self.row = row
        self.column = column
        self.move_delay = 1000
        self.last_time_moved = time.get_ticks()
        self.speed = 1
        self.image = image
        super().__init__(self.image, self.row, self.column)