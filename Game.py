import sys
from os import path
from Map import *
from Ennemy import *
from TypeEnum import *
from Player import *

from pygame import *


class Game:

    def __init__(self, screen):
        self.screen = screen
        self.clock = time.Clock()
        self.mAllSpritesGroup = sprite.Group()
        self.mEnemiesSpriteGroup = sprite.Group()
        self.mMap = Map(11, 14)
        self.size = width, height = 900, 668
        self.Fps = 60
        self.running = True
        # Directories
        self.Sound_dir = path.join(path.dirname(__file__), 'Sounds')
        self.Img_dir = path.join(path.dirname(__file__), 'Images')
        self.background_img = image.load(path.join(self.Img_dir, 'space.jpg')).convert()
        self.running = True

        self.init_pygame()

    def init_pygame(self):
        init()
        mixer.init()
        display.set_caption('Space Invaders')
        mixer.music.load(path.join(self.Sound_dir, 'main.wav'))
        mixer.music.set_volume(0.05)
        timer = time.get_ticks()

    def add_enemies(self, enemies_number, enemy_img):
        for i in range(enemies_number):
            self.mEnemy = Ennemy(0, 2 + i, enemy_img)
            self.mAllSpritesGroup.add(self.mEnemy)
            self.mEnemiesSpriteGroup.add(self.mEnemy)
            self.mMap.Grid[0][2 + i] = TypeEnum.ENEMY

    def add_player(self, playerimg):
        self.mPlayer = Player(9,6, playerimg)
        self.mAllSpritesGroup.add(self.mPlayer)
        self.mMap.Grid[self.mPlayer.row][self.mPlayer.column] = TypeEnum.PLAYER

    def main(self):
        while self.running:
            self.clock.tick(self.Fps)
            for EVENT in event.get():
                if EVENT.type == QUIT:
                    sys.exit()
            coord = self.mPlayer.update()
            print("Row : " + str(coord.row) + " column : " + str(coord.column))
            self.screen.blit(self.background_img, (0, 0))
            self.mAllSpritesGroup.draw(self.screen)
            display.flip()