from collections import namedtuple

from ObjectBoard import *
import time


class Player(ObjectBoard):
    def __init__(self, row, column, image):
        self.row = row
        self.column = column
        self.lives = 3
        self.image = image
        self.invulnerability_frames = 0
        self.hidden = False
        self.hide_timer = 1000
        super().__init__(image, self.row, self.column)

    def update(self):
        """
        Update the position of the player
        :return: The old and new coordinates of player
        """

        keys = key.get_pressed()
        old_row = self.row
        old_column = self.column
        if keys[K_LEFT] or keys[K_q]:
            if self.column > 0:
                self.column = self.column - 1
                while self.rect.left != (self.TileWidth * self.column + self.TileMargin):
                    time.sleep(0.0050)
                    self.rect.left = self.rect.left - 4
        if keys[K_RIGHT] or keys[K_d]:
            if self.column <= 12:
                self.column = self.column + 1
                while self.rect.left != (self.TileWidth * self.column + self.TileMargin):
                    time.sleep(0.0050)
                    self.rect.left = self.rect.left + 4
        Coord = namedtuple('Coord', ['row', 'column', 'old_row', 'old_column'])
        coord = Coord(self.row, column=self.column, old_row=old_row, old_column=old_column)
        return coord

