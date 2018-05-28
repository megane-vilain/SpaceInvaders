from collections import namedtuple

from ObjectBoard import *


class Enemy(ObjectBoard):
    def __init__(self, row, column, image):
        self.row = row
        self.column = column
        self.speed = 1
        self.image = image
        self.timer = time.get_ticks()
        self.move_time = 700
        super().__init__(self.image, self.row, self.column)

    def update(self, current_time, move_down ):
        """
        Update the position of the player
        :return: The old and new coordinates of player
        """
        old_row = self.row
        old_column = self.column
        if move_down:
            self.row += 1
            self.speed *= -1
            self.rect.top = (self.TileHeight * self.row + self.TileMargin)
            self.rect.left = (self.TileWidth * self.column + self.TileMargin)
            self.column += self.speed
            self.timer += self.move_time
        if current_time - self.timer > self.move_time:
            self.rect.left = (self.TileWidth * self.column + self.TileMargin)
            self.column += self.speed
            self.timer += self.move_time
        Coord = namedtuple('Coord', ['row', 'column', 'old_row', 'old_column'])
        coord = Coord(self.row, column=self.column, old_row=old_row, old_column=old_column)
        return coord
