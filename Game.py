from os import path
from Map import *
from Ennemy import *
from TypeEnum import *

import pygame


class Game:



    def __init__(self):
        self.mAllSpritesGroup = pygame.sprite.Group()
        self.mEnemiesSpriteGroup = pygame.sprite.Group()
        self.mMap = Map(9, 12)
        self.size = width, height = 900, 700
        self.Fps = 60
        self.running = True
        # Directories
        self.Sound_dir = path.join(path.dirname(__file__), 'Sounds')
        self.Img_dir = path.join(path.dirname(__file__), 'Images')

        self.initpygame()



    def initpygame(self):
        pygame.init()
        pygame.mixer.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Space Invaders')
        pygame.mixer.music.load(path.join(self.Sound_dir, 'main.wav'))
        pygame.mixer.music.set_volume(0.05)
        timer = pygame.time.get_ticks()

    def addenemies(self, enemiesNumber, enemyImg):
        for i in range(enemiesNumber):
            mEnemy = Ennemy(0, 2 + i, enemyImg)
            self.mAllSpritesGroup.add(mEnemy)
            self.mEnemiesSpriteGroup.add(mEnemy)
            self.mMap.Grid[0][2 + i] = TypeEnum.ENEMY

    def addplayer(self, playerImg):
        self.mAllSpritesGroup.add()