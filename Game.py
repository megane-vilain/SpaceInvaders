import sys
from os import path
from Enemy import *
from Player import *
from Bullet import *
import random

from pygame import *


class Game:

    def __init__(self, screen):
        self.screen = screen
        self.clock = time.Clock()
        self.mAllSpritesGroup = sprite.Group()
        self.mEnemiesSpriteGroup = sprite.Group()
        self.mBulletsSpriteGroup = sprite.Group()
        self.mMap = Map(10, 20)
        self.mPlayer = None
        self.mEnemy = None
        self.mBullet = None
        self.size = width, height = 900, 668
        self.Fps = 60
        self.running = True
        self.Sound_dir = path.join(path.dirname(__file__), 'Sounds')
        self.Img_dir = path.join(path.dirname(__file__), 'Images')
        self.background_img = image.load(path.join(self.Img_dir, 'space.jpg')).convert()

        self.init_pygame()

    def init_pygame(self):
        init()
        mixer.init()
        display.set_caption('Space Invaders')
        mixer.music.load(path.join(self.Sound_dir, 'main.wav'))
        mixer.music.set_volume(0.05)
        timer = time.get_ticks()
        self.load_images()
        self.load_sounds()

    def load_images(self):
        IMG_NAMES = ["player_ship", "player_life", "enemy1", "bullet"]
        self.images = {name: image.load("Images/{}.ico".format(name)).convert_alpha()
                       for name in IMG_NAMES}
        self.images["player_life"] = transform.scale(self.images["player_life"], (30, 30))
        self.images["player_life"].set_colorkey((0, 0, 0))

    def load_sounds(self):
        SND_NAMES = ["shoot", "expl3", "main"]
        self.sounds = {name: mixer.Sound("Sounds/{}.wav".format(name)) for name in SND_NAMES}
        mixer.music.load("Sounds/main.wav")
        mixer.music.set_volume(0.2)
        mixer.music.play(loops=-1)

    def draw_lives(self, img, lives):
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.left = self.mMap.TileWidth * (11 + i) + self.mMap.TileMargin
            img_rect.y = self.mMap.TileHeight / 2
            self.screen.blit(img, img_rect)

    def add_enemies(self, enemies_number, row, enemy_img):
        for i in range(enemies_number):
            self.mEnemy = Enemy(row, 3 + i, enemy_img)
            self.mAllSpritesGroup.add(self.mEnemy)
            self.mEnemiesSpriteGroup.add(self.mEnemy)
            self.mMap.Grid[0][2 + i] = TypeEnum.ENEMY

    def add_player(self, player_img):
        self.mPlayer = Player(9, 6, player_img)
        self.mAllSpritesGroup.add(self.mPlayer)
        self.mMap.Grid[self.mPlayer.row][self.mPlayer.column] = TypeEnum.PLAYER

    def add_bullet(self, bullet_img, row, column, direction):
        self.mBullet = Bullet(row, column, bullet_img, direction)
        self.mAllSpritesGroup.add(self.mBullet)
        self.mBulletsSpriteGroup.add(self.mBullet)
        self.mMap.Grid[row][column] = TypeEnum.BULLET
        self.sounds["shoot"].play()

    def main(self):
        move_down = False
        row = 1
        while self.running:

            self.clock.tick(self.Fps)
            for EVENT in event.get():
                if EVENT.type == QUIT:
                    sys.exit()
                if EVENT.type == KEYDOWN and EVENT.key == K_SPACE:
                    if self.mPlayer.shoot(time.get_ticks()):
                        self.add_bullet(self.images["bullet"], self.mPlayer.row - 1 , self.mPlayer.column, -1)

            coord = self.mPlayer.update()
            if coord.column != coord.old_column:
                self.mMap.update_map(coord, TypeEnum.PLAYER)

            if self.mMap.Grid[row][13] == TypeEnum.ENEMY or self.mMap.Grid[row][0] == TypeEnum.ENEMY:
                move_down = True
                row += 1

            for enemy in self.mEnemiesSpriteGroup:
                coord_enemies = enemy.update(time.get_ticks(), move_down)
                self.mMap.update_map(coord_enemies, TypeEnum.ENEMY)

            for bullet in self.mBulletsSpriteGroup:
                coord_bullets = bullet.update(time.get_ticks())
                if coord_bullets.row != coord_bullets.old_row:
                    if coord_bullets.row == -1 or coord_bullets.row > 0:
                        self.mMap.update_map(coord_bullets, TypeEnum.BULLET)
                    if coord_bullets.row < -1:
                        bullet.kill()

            for enemy in sprite.groupcollide(self.mEnemiesSpriteGroup, self.mBulletsSpriteGroup, True, True):
                self.mMap.Grid[enemy.row][enemy.column] = TypeEnum.EMPTY
                self.sounds["expl3"].play()

            if sprite.spritecollide(self.mPlayer, self.mEnemiesSpriteGroup, False):
                if self.mPlayer.lives != 0:
                    self.mPlayer.lives -= 1
                    # player.hide()
                    player_invulnerable_frames = 30
                else:
                    self.running = False

            move_down = False

            if not self.mEnemiesSpriteGroup:
                self.running = False

            self.screen.blit(self.background_img, (0, 0))
            self.mAllSpritesGroup.draw(self.screen)

            ##################TEST TIR ENEMIE###########
            # print(random.randint(0,8))
            #
            # random_enemy = random.choice(self.mEnemiesSpriteGroup.sprites())
            # if(random_enemy.shoot(time.get_ticks())):
            #     self.add_bullet(self.images["bullet"], random_enemy.row+1, random_enemy.column, 1)
            ##################################

            # Print the Grid for degug purpose
            for Row in range(11):
                draw.line(self.screen, (255, 255, 255), (0, Row * 64), (900, 64 * Row), 4)
                for Column in range(14):
                    draw.line(self.screen, (255, 255, 255), (Column * 64, 0), (Column * 64, 700), 4)

            self.draw_lives(self.images["player_life"], 3)

            display.update()
            display.flip()
