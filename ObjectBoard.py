from pygame import *
from Map import *


class ObjectBoard(sprite.Sprite, Map):
    def __init__(self, image, row, column ):
        sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.TileWidth = 64
        self.TileHeight = 64
        self.TileMargin = 4
        self.rect.left = (self.TileWidth * column + self.TileMargin)
        self.rect.top = (self.TileHeight * row + self.TileMargin)
        self.shoot_delay = 700
        self.last_shot = time.get_ticks()

    def shoot(self, current_time):
        if current_time - self.last_shot > self.shoot_delay:
            self.last_shot += self.shoot_delay
            return True

        else:
            return False