from collections import namedtuple

from ObjectBoard import *
import time as time2


class Player(ObjectBoard):
    def __init__(self, row, column, image):
        self.row = row
        self.column = column
        self.lives = 3
        self.image = image
        self.hide_timer = 1000
        self.hide = False
        self.hide_time = time.get_ticks()
        super().__init__(image, self.row, self.column)

    def update(self, current_time):
        """
        Update the position of the player
        :return: The old and new coordinates of player
        """
        old_row = self.row
        old_column = self.column
        if self.hide and current_time - self.hide_time > self.hide_timer:
            self.hide = False
            self.rect.left = (self.TileWidth * self.column + self.TileMargin)
            event.pump()
        else:
            keys = key.get_pressed()
            if keys[K_LEFT] or keys[K_q] or keys[K_a]:
                if self.column > 0:
                    self.column = self.column - 1
                    while self.rect.left != (self.TileWidth * self.column + self.TileMargin):
                        time2.sleep(0.0050)
                        self.rect.left = self.rect.left - 4
            if keys[K_RIGHT] or keys[K_d]:
                if self.column <= 12:
                    self.column = self.column + 1
                    while self.rect.left != (self.TileWidth * self.column + self.TileMargin):
                        time2.sleep(0.0050)
                        self.rect.left = self.rect.left + 4
        Coord = namedtuple('Coord', ['row', 'column', 'old_row', 'old_column'])
        coord = Coord(self.row, column=self.column, old_row=old_row, old_column=old_column)
        return coord

    def hide_player(self):
        self.hide = True
        self.hide_time = time.get_ticks()
        self.rect.left = (self.TileWidth * 14 + self.TileMargin)

