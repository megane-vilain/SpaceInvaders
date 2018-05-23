import pygame


class ObjectBoard(pygame.sprite.Sprite):
    def __init__(self, image, collumn, row, ):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.TileWidth = 64
        self.TileHeight = 64
        self.TileMargin = 4
        self.rect.left = (self.TileWidth * row + self.TileMargin)
        self.rect.top = (self.TileHeight * collumn + self.TileMargin)
