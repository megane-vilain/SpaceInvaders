import sys
from os import path
from Ennemy import *
from Player import *

from pygame import *

class Game:

    def __init__(self, screen):
        self.screen = screen
        self.clock = time.Clock()
        self.mAllSpritesGroup = sprite.Group()
        self.mEnemiesSpriteGroup = sprite.Group()
        self.mMap = Map(10, 13)
        self.mPlayer = None
        self.mEnemy = None
        self.size = width, height = 900, 668
        self.Fps = 60
        self.running = True
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
        self.load_images()

    def load_images(self):
        IMG_NAMES = ["player_ship", "player_life", "enemy1", "bullet"]
        self.images = {name: image.load("Images/{}.ico".format(name)).convert_alpha()
          for name in IMG_NAMES}

    def load_sounds(self):
        pass

    def add_enemies(self, enemies_number, enemy_img):
        for i in range(enemies_number):
            self.mEnemy = Ennemy(0, 2 + i, enemy_img)
            self.mAllSpritesGroup.add(self.mEnemy)
            self.mEnemiesSpriteGroup.add(self.mEnemy)
            self.mMap.Grid[0][2 + i] = TypeEnum.ENEMY

    def add_player(self, player_img):
        self.mPlayer = Player(9, 6, player_img)
        self.mAllSpritesGroup.add(self.mPlayer)
        self.mMap.Grid[self.mPlayer.row][self.mPlayer.column] = TypeEnum.PLAYER

    def main(self):

        while self.running:
            self.clock.tick(self.Fps)
            for EVENT in event.get():
                if EVENT.type == QUIT:
                    sys.exit()
            coord = self.mPlayer.update()
            coord_enemies = self.mEnemiesSpriteGroup.update(time.get_ticks())
            if coord_enemies.column != coord_enemies.old_column:
                self.mMap.update_map(coord_enemies, TypeEnum.ENEMY)
            self.screen.blit(self.background_img, (0, 0))
            self.mAllSpritesGroup.draw(self.screen)
            if coord.column != coord.old_column:
                self.mMap.update_map(coord, TypeEnum.PLAYER)

            #Print the Grid for degug purpose
            for Row in range(11):
                draw.line(self.screen, (255,255,255), (0,Row * 64),(900,64*Row),4 )
                for Column in range(14):
                    draw.line(self.screen,(255,255,255), (Column*64, 0) , (Column*64, 700) ,4)
            display.update()
            display.flip()

