from collections import namedtuple

from ObjectBoard import *
import time as time2


class Player(ObjectBoard):
    def __init__(self, row, column, image):
        self.row = row
        self.column = column
        self.lives = 3
        self.image = image
        self.invulnerability_frame = 0
        super().__init__(image, self.row, self.column)

    def update(self):
        """
        Update the position of the player
        :return: The old and new coordinates of player
        """
        old_row = self.row
        old_column = self.column

        keys = key.get_pressed()
        if keys[K_LEFT] or keys[K_q] or keys[K_a]:
            if self.column > 0:
                self.column = self.column - 1
                while self.rect.left != (self.TileWidth * self.column + self.TileMargin):
                    time2.sleep(0.0050)
                    self.rect.left = self.rect.left - 8
        if keys[K_RIGHT] or keys[K_d]:
            if self.column <= 12:
                self.column = self.column + 1
                while self.rect.left != (self.TileWidth * self.column + self.TileMargin):
                    time2.sleep(0.0050)
                    self.rect.left = self.rect.left + 8

        Coord = namedtuple('Coord', ['row', 'column', 'old_row', 'old_column'])
        coord = Coord(self.row, column=self.column, old_row=old_row, old_column=old_column)
        return coord

