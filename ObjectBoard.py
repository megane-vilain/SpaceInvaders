from pygame import *
from Map import *


class ObjectBoard(sprite.Sprite):
    def __init__(self, image, row, column ):
        sprite.Sprite.__init__(self)
        self.image = image
        self.row = row
        self.column = column
        self.rect = self.image.get_rect()
        self.tile_width = 64
        self.tile_height = 64
        self.tile_margin = 4
        self.direction = 1
        self.rect.left = (self.tile_width * column + self.tile_margin)
        self.rect.top = (self.tile_height * row + self.tile_margin)
        self.shoot_delay = 400
        self.last_shot = time.get_ticks()

    def shoot(self, current_time):
        if current_time - self.last_shot > self.shoot_delay:
            self.last_shot = time.get_ticks()
            return True

        else:
            return False