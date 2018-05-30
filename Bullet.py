from collections import namedtuple

from ObjectBoard import *


class Bullet(ObjectBoard):

    def __init__(self, row, column, image, direction):
        super().__init__(image, row, column)
        self.rect.centerx = (self.tile_width * column) + (self.tile_width + self.tile_margin) / 2
        self.rect.top = (self.tile_height * row) + self.tile_height / 2
        self.timer = time.get_ticks()
        self.move_delay = 100
        self.direction = direction

    def update(self, current_time):
        old_row = row = self.row
        old_column = self.column

        if current_time - self.timer > self.move_delay:
            self.row += self.direction
            while self.rect.top != (self.tile_height * row) + self.tile_height / 2:
                self.rect.top += 4 * self.direction
            self.timer += self.move_delay

        Coord = namedtuple('Coord', ['row', 'column', 'old_row', 'old_column'])
        coord = Coord(self.row, column=self.column, old_row=old_row, old_column=old_column)
        return coord
