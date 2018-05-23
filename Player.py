from ObjectBoard import *
import time


class Player(ObjectBoard):
    def __init__(self, column, row, image):
        self.row = row
        self.column = column
        self.lives = 3
        self.image = image
        super().__init__(image, self.column, self.row)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            if self.row > 0:
                self.row = self.row - 1
                while self.rect.left != (self.TileWidth * self.row + self.TileMargin):
                    time.sleep(0.0050)
                    self.rect.left = self.rect.left - 4

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.row < 13:
                self.row = self.row + 1
                while self.rect.left != (self.TileWidth * self.row + self.TileMargin):
                    time.sleep(0.0050)
                    self.rect.left = self.rect.left + 4
