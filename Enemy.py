from collections import namedtuple

from ObjectBoard import *


class Enemy(ObjectBoard):
    def __init__(self, row, column, image):
        self.value = 50
        super().__init__(image, row, column)

    def update(self, current_time, move_down ):
        """
        Update the position of the player
        :return: The old and new coordinates of player
        """
        old_row = self.row
        old_column = self.column
        if move_down:
            self.row += 1
            self.direction *= -1
            self.rect.top = (self.tile_height * self.row + self.tile_margin)
            self.rect.left = (self.tile_width * self.column + self.tile_margin)
            self.column += self.direction
        else:
            self.column += self.direction
            self.rect.left = (self.tile_width * self.column + self.tile_margin)

        Coord = namedtuple('Coord', ['row', 'column', 'old_row', 'old_column'])
        coord = Coord(self.row, column=self.column, old_row=old_row, old_column=old_column)
        return coord
