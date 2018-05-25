from collections import namedtuple

from ObjectBoard import *


class Ennemy(ObjectBoard):
    def __init__(self, row, column, image):
        self.row = row
        self.column = column
        self.speed = 1
        self.move_time = 10
        self.image = image
        self.timer = time.get_ticks()
        self.move_time = 500
        self.move_down = False
        super().__init__(self.image, self.row, self.column)

    def update(self, current_time):
        """
        Update the position of the player
        :return: The old and new coordinates of player
        """
        old_row = self.row
        old_column = self.column
        if current_time - self.timer > self.move_time:

            print("move_down " + str(self.move_down))
            self.rect.left = (self.TileWidth * self.column + self.TileMargin)
            if self.column == 14 or self.column < 0:
                self.row += 1
                print("Collision mur : " + str(self.column))
                self.speed *= -1
                self.move_down = True
            if self.self.Grid[self.row][14] == TypeEnum.ENEMY:
                self.rect.top = (self.TileHeight * self.row + self.TileMargin)
            self.column += self.speed
            self.timer += self.move_time
        Coord = namedtuple('Coord', ['row', 'column', 'old_row', 'old_column'])
        coord = Coord(self.row, column=self.column, old_row=old_row, old_column=old_column)
        return coord
