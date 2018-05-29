import sys
from os import path
from Enemy import *
from Player import *
from Bullet import *
from pygame import *
import random


class Game:

    def __init__(self, screen):
        self.screen = screen
        self.clock = time.Clock()
        self.mAllSpritesGroup = sprite.Group()
        self.mEnemiesSpriteGroup = sprite.Group()
        self.mEnemiesBulletsSpriteGroup = sprite.Group()
        self.mPlayerBulletsSpriteGroup = sprite.Group()
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
        self.shoot_time = 900
        self.move_time = 900
        self.row = 1
        self.score = 0
        self.font_name = font.match_font('arial')
        self.game_over = False

        # Custom Pygame events
        self.enemy_shoot_event = USEREVENT + 1
        self.enemy_move_event = USEREVENT + 2

        self.init()

    def init(self):
        init()
        mixer.init()
        display.set_caption('Space Invaders')
        mixer.music.load(path.join(self.Sound_dir, 'main.wav'))
        time.set_timer(self.enemy_shoot_event, self.shoot_time)
        time.set_timer(self.enemy_move_event, self.move_time)
        self.load_images()
        self.load_sounds()

    def load_images(self):
        img_names = ["player_ship", "player_life", "enemy1", "enemy2", "enemy3", "enemy_laser", "player_laser", "space_invaders_main"]
        self.images = {name: image.load("Images/{}.ico".format(name)).convert_alpha()
                       for name in img_names}
        self.images["player_life"] = transform.scale(self.images["player_life"], (30, 30))
        self.images["player_life"].set_colorkey((0, 0, 0))

    def load_sounds(self):
        snd_names = ["shoot", "expl3", "main", "shipexplosion"]
        self.sounds = {name: mixer.Sound("Sounds/{}.wav".format(name)) for name in snd_names}
        self.sounds["shoot"].set_volume(0.3)
        self.sounds["expl3"].set_volume(0.3)
        mixer.music.load("Sounds/main.wav")
        mixer.music.play(loops=-1)

    def draw_lives(self, img, lives):
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.left = self.mMap.TileWidth * (11 + i) + self.mMap.TileMargin
            img_rect.y = self.mMap.TileHeight / 2
            self.screen.blit(img, img_rect)

    def draw_text(self, text, size, x, y, color):
        mfont = font.Font(self.font_name, size)
        text_surface = mfont.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def add_enemies(self, enemies_number, row, enemy_img):
        for i in range(enemies_number):
            self.mEnemy = Enemy(row, 3 + i, enemy_img)
            self.mAllSpritesGroup.add(self.mEnemy)
            self.mEnemiesSpriteGroup.add(self.mEnemy)
            self.mMap.Grid[row][3 + i] = TypeEnum.ENEMY

    def add_player(self, player_img):
        self.mPlayer = Player(9, 6, player_img)
        self.mAllSpritesGroup.add(self.mPlayer)
        self.mMap.Grid[self.mPlayer.row][self.mPlayer.column] = TypeEnum.PLAYER

    def add_bullet(self, bullet_img, row, column, direction, type):
        self.mBullet = Bullet(row, column, bullet_img, direction)
        self.mAllSpritesGroup.add(self.mBullet)
        self.mMap.Grid[row][column] = TypeEnum.BULLET
        if type == TypeEnum.PLAYER:
            self.mPlayerBulletsSpriteGroup.add(self.mBullet)
        else:
            self.mEnemiesBulletsSpriteGroup.add(self.mBullet)

        self.sounds["shoot"].play()

    def get_event(self):

        for EVENT in event.get():
            if EVENT.type == QUIT:
                sys.exit()
            if EVENT.type == KEYDOWN and EVENT.key == K_SPACE:
                if self.mPlayer.shoot(time.get_ticks()):
                    self.add_bullet(self.images["player_laser"], self.mPlayer.row - 1, self.mPlayer.column, -1,
                                    TypeEnum.PLAYER)

            if EVENT.type == self.enemy_shoot_event:
                random_enemy = random.choice(self.mEnemiesSpriteGroup.sprites())
                self.add_bullet(self.images["enemy_laser"], random_enemy.row + 1, random_enemy.column, 1,
                                TypeEnum.ENEMY)
                time.set_timer(self.enemy_shoot_event, self.shoot_time)

            if EVENT.type == self.enemy_move_event:
                if self.mMap.Grid[self.row][14] == TypeEnum.ENEMY or self.mMap.Grid[self.row][-1] == TypeEnum.ENEMY:
                    move_down = True
                    self.row += 1
                else:
                    move_down = False

                for enemy in self.mEnemiesSpriteGroup:
                    coord_enemies = enemy.update(time.get_ticks(), move_down)
                    self.screen.blit(enemy.image, enemy.rect)
                    self.mMap.update_map(coord_enemies, TypeEnum.ENEMY)
                time.set_timer(self.enemy_move_event, self.move_time)

    def show_game_over_screen(self, current_time, timer):
        self.screen.blit(self.background_img, (0,0))
        self.draw_text("GAME OVER", 64 , self.mMap.TileWidth * 7 , self.mMap.TileHeight * 2, (255, 255, 255))
        self.draw_text(("SCORE " + str(self.score)), 25, self.mMap.TileWidth * 7, self.mMap.TileHeight * 4 , (255,255,255))
        self.draw_text("Press a key to start again" , 25,self.mMap.TileWidth * 7, self.mMap.TileHeight * 6,(255, 255, 255))
        display.flip()
        waiting = True
        while waiting:
            self.clock.tick(self.Fps)
            for EVENT in event.get():
                if EVENT.type == QUIT:
                    quit()
                if EVENT.type == KEYUP:
                    if time.get_ticks() - current_time > timer:
                        waiting = False

    def reset(self):
        self.mPlayer.lives = 3
        self.score = 0
        self.mEnemiesSpriteGroup.empty()
        self.mAllSpritesGroup.empty()

        self.add_enemies(8, 1, self.images["enemy1"])
        self.add_enemies(8, 2, self.images["enemy2"])
        self.add_enemies(8, 3, self.images["enemy3"])

        self.add_player(self.images["player_ship"])

        display.flip()

    def main(self):

        while self.running:

            self.clock.tick(self.Fps)

            if self.game_over:
                self.show_game_over_screen(time.get_ticks(), 1000)
                self.reset()
                self.game_over = False

            if self.mPlayer.invulnerability_frame > 0:
                self.mPlayer.invulnerability_frame -= 1

            self.get_event()

            coord = self.mPlayer.update()
            if coord.column != coord.old_column:
                self.mMap.update_map(coord, TypeEnum.PLAYER)

            for bullet in self.mEnemiesBulletsSpriteGroup:
                coord_bullets = bullet.update(time.get_ticks())
                self.screen.blit(self.images["enemy_laser"], bullet.rect)
                if coord_bullets.row != coord_bullets.old_row:
                    if coord_bullets.row == -1 or 0 < coord_bullets.row < 10:
                        self.mMap.update_map(coord_bullets, TypeEnum.BULLET)
                    if coord_bullets.row < -1 or coord_bullets.row > 10:
                        bullet.kill()

            for bullet in self.mPlayerBulletsSpriteGroup:
                coord_bullets = bullet.update(time.get_ticks())
                self.screen.blit(self.images["player_laser"], bullet.rect)
                if coord_bullets.row != coord_bullets.old_row:
                    if coord_bullets.row == -1 or 0 < coord_bullets.row < 10:
                        self.mMap.update_map(coord_bullets, TypeEnum.BULLET)
                    if coord_bullets.row < -1 or coord_bullets.row > 10:
                        bullet.kill()

            for enemy in sprite.groupcollide(self.mEnemiesSpriteGroup, self.mPlayerBulletsSpriteGroup, True, True):
                self.mMap.Grid[enemy.row][enemy.column] = TypeEnum.EMPTY
                self.sounds["expl3"].play()
                self.score += enemy.value

            if sprite.spritecollide(self.mPlayer, self.mEnemiesSpriteGroup, False):
                self.game_over = True

            if sprite.spritecollide(self.mPlayer, self.mEnemiesBulletsSpriteGroup, False):
                if self.mPlayer.lives >= 0 >= self.mPlayer.invulnerability_frame:
                    self.mPlayer.invulnerability_frame = 120
                    self.sounds["shipexplosion"].play()
                    self.mPlayer.lives -= 1

                if self.mPlayer.lives <= 0:
                    self.sounds["shipexplosion"].play()
                    self.game_over = True

            if not self.mEnemiesSpriteGroup:
                self.running = False

            if len(self.mEnemiesSpriteGroup) <= 5 and self.shoot_time != 1500:
                self.shoot_time = 1500

            self.screen.blit(self.background_img, (0, 0))
            self.mAllSpritesGroup.draw(self.screen)

            self.draw_text("SCORE ", 25, self.mMap.TileWidth, 10, (255, 255, 255))
            self.draw_text(str(self.score), 25, self.mMap.TileWidth * 2, 10, (78, 255, 87))

            self.draw_lives(self.images["player_life"], self.mPlayer.lives)

            display.update()
            display.flip()
