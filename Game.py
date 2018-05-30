from os import path
import sys
import csv
from Enemy import *
from Player import *
from Bullet import *
from pygame import *
from settings import *
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
        self.running = True
        self.Sound_dir = path.join(path.dirname(__file__), 'Sounds')
        self.Img_dir = path.join(path.dirname(__file__), 'Images')
        self.background_img = image.load(path.join(self.Img_dir, 'space.jpg')).convert()
        self.shoot_time = 900
        self.score = 0
        self.row = 1
        self.font_name = font.match_font('arial')
        self.end_game = False
        self.load_screen = True
        self.game_over = False
        self.high_score = 0
        self.enemies_moving = False

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
        time.set_timer(self.enemy_move_event, ENEMY_MOVE_TIME)
        self.load_images()
        self.load_sounds()
        self.add_objects()
        self.get_data()

    def load_images(self):
        img_names = ["player_ship", "player_life", "enemy1", "enemy2", "enemy3", "enemy_laser", "player_laser",
                     "space_invaders_main"]
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

    def add_objects(self):
        self.add_enemies(8, 1, self.images["enemy1"])
        self.add_enemies(8, 2, self.images["enemy2"])
        self.add_enemies(8, 3, self.images["enemy3"])
        self.add_player(9,6,self.images["player_ship"])

    def draw_lives(self, img, lives):
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.left = self.mMap.tile_width * (11 + i) + self.mMap.tile_margin
            img_rect.y = self.mMap.tile_height / 2
            self.screen.blit(img, img_rect)

    def draw_text(self, screen, text, size, x, y, color):
        mfont = font.Font(self.font_name, size)
        text_surface = mfont.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

    def add_enemies(self, enemies_number, row, enemy_img):
        for i in range(enemies_number):
            self.mEnemy = Enemy(row, 3 + i, enemy_img)
            self.mAllSpritesGroup.add(self.mEnemy)
            self.mEnemiesSpriteGroup.add(self.mEnemy)
            self.mMap.grid[row][3 + i] = TypeEnum.ENEMY

    def add_player(self,row, column,  player_img):
        self.mPlayer = Player(row, column, player_img)
        self.mAllSpritesGroup.add(self.mPlayer)
        self.mMap.grid[self.mPlayer.row][self.mPlayer.column] = TypeEnum.PLAYER

    def add_bullet(self, bullet_img, row, column, direction, object_type):
        self.mBullet = Bullet(row, column, bullet_img, direction)
        self.mAllSpritesGroup.add(self.mBullet)
        if row != -1 and row != 10:
            self.mMap.grid[row][column] = TypeEnum.BULLET
            if object_type == TypeEnum.PLAYER:
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

            if EVENT.type == KEYDOWN and EVENT.key == K_ESCAPE:
                self.show_beak_screen()
            if EVENT.type == self.enemy_shoot_event:
                if not self.enemies_moving:
                    random_enemy = random.choice(self.mEnemiesSpriteGroup.sprites())
                    self.add_bullet(self.images["enemy_laser"], random_enemy.row + 1, random_enemy.column, 1,
                                    TypeEnum.ENEMY)
                    time.set_timer(self.enemy_shoot_event, self.shoot_time)

            if EVENT.type == self.enemy_move_event:
                self.enemies_moving = True
                if self.mMap.grid[self.row][13] == TypeEnum.ENEMY or self.mMap.grid[self.row][1] == TypeEnum.ENEMY:
                    move_down = True
                    self.row += 1
                else:
                    move_down = False

                for enemy in self.mEnemiesSpriteGroup:
                    coord_enemies = enemy.update(time.get_ticks(), move_down)
                    self.screen.blit(enemy.image, enemy.rect)
                    self.mMap.update_map(coord_enemies, TypeEnum.ENEMY)

                time.set_timer(self.enemy_move_event, ENEMY_MOVE_TIME)
                self.enemies_moving = False

    def show_game_over_screen(self, title, current_time, timer):
        self.screen.blit(self.background_img, (0, 0))
        self.draw_text(self.screen, title, 64, self.mMap.tile_width * 7, self.mMap.tile_height * 2, WHITE)

        if self.score > self.high_score:
            self.draw_text(("NEW HIGH SCORE " + str(self.score)), 25, self.mMap.tile_width * 7,
                           self.mMap.tile_height * 4,
                           WHITE)
        else:
            self.draw_text(("SCORE " + str(self.score)), 25, self.mMap.tile_width * 7,
                           self.mMap.tile_height * 4,
                           WHITE)
        self.draw_text(self.screen, "Press a key to start again", 25, self.mMap.tile_width * 7,
                       self.mMap.tile_height * 6,
                       WHITE)
        display.flip()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for EVENT in event.get():
                if EVENT.type == QUIT:
                    quit()
                if EVENT.type == KEYUP:
                    if time.get_ticks() - current_time > timer:
                        waiting = False

    def show_load_screen(self, current_time, timer):
        self.screen.blit(self.background_img, (0, 0))
        self.draw_text(self.screen, " SPACE INVADERS", 64, self.mMap.tile_width * 7, self.mMap.tile_height * 2, WHITE)
        self.draw_text(self.screen, "HIGH SCORE " + str(self.high_score), 35, self.mMap.tile_width * 7,
                       self.mMap.tile_width * 4,
                       WHITE)
        self.screen.blit(self.images["space_invaders_main"], (self.mMap.tile_width * 6, self.mMap.tile_height * 5))
        self.draw_text(self.screen, "Press a key to start", 25, self.mMap.tile_width * 7, self.mMap.tile_height * 7,
                       WHITE)
        display.flip()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for EVENT in event.get():
                if EVENT.type == QUIT:
                    quit()
                if EVENT.type == KEYUP:
                    if time.get_ticks() - current_time > timer:
                        waiting = False

    def show_beak_screen(self):
        self.screen.blit(self.background_img, (0, 0))
        rect = Rect(400, 200, 100, 50)
        rect2 = Rect(400, 600, 100, 50)
        self.draw_text(self.screen, "Sauvegarder", 25, 400, 200, WHITE)
        self.draw_text(self.screen, "Charger", 25, 600, 200, WHITE)

        display.flip()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for EVENT in event.get():
                if EVENT.type == MOUSEBUTTONDOWN:
                    pos = mouse.get_pos()
                    if 500 > pos[0] > 300 and 300 > pos[1] > 200:
                        self.save_game()
                        waiting = False

                    if 700 > pos[0] > 500 and 300 > pos[1] > 200:
                        self.load_map()
                        waiting = False
                if EVENT.type == KEYDOWN and EVENT.key == K_ESCAPE:
                    waiting = False

        display.flip()

    def get_data(self):
        with open(path.join(path.dirname(__file__), HS_FILE), 'r') as f:
            try:
                self.high_score = int(f.read())
            except:
                self.high_score = 0

    def save_score(self):
        with open(path.join(path.dirname(__file__), HS_FILE), 'w+') as f:
            f.write(str(self.score))

    def save_game(self):
        with open(path.join(path.dirname(__file__), CSV_FILE), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            for row in range(self.mMap.map_row):
                writer.writerow(self.mMap.get_row_string(row))

        with open(path.join(path.dirname(__file__), SAVE_FILE), 'w+') as f:
            f.write(str(self.score) + "-" + str(self.mPlayer.lives) )

    def load_map(self):
        self.reset()
        display.flip()
        with open(path.join(path.dirname(__file__), CSV_FILE), 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            row = 0
            for reader_row in reader:
                i = len(reader_row)
                column = 0
                for element in reader_row :
                    if element != "2":
                        if element == "3":
                            enemy = Enemy(row, column, self.images["enemy1"])
                            self.mEnemiesSpriteGroup.add(enemy)
                            self.mAllSpritesGroup.add(enemy)
                        if element == "1":
                            player = Player(row, column, self.images["player_ship"])
                            self.mPlayer  = player
                            self.mAllSpritesGroup.add(player)
                        self.mMap.grid[row][column] = TypeEnum(int(element))

                    column += 1
                row +=1
        with open(path.join(path.dirname(__file__), SAVE_FILE), 'r') as f:
            try:

                   s = f.read()
                   self.score = int(s.split("-")[0])
                   self.mPlayer.lives = int(s.split("-")[1])
            except:
                self.score = 0


    def reset(self):
        self.mPlayer.lives = 3
        self.score = 0
        self.mEnemiesSpriteGroup.empty()
        self.mAllSpritesGroup.empty()
        self.mMap.init_map()
        self.row = 1

    def main(self):

        while self.running:

            self.clock.tick(FPS)

            if self.load_screen:
                self.show_load_screen(time.get_ticks(), 700)
                self.load_screen = False

            if self.end_game:
                if self.game_over:
                    self.game_over = False
                    self.show_game_over_screen("GAME OVER", time.get_ticks(), 1000)
                else:
                    self.show_game_over_screen("CONGRATULATIONS", time.get_ticks(), 700)
                    self.save_score()
                self.reset()
                self.add_objects()
                display.flip()
                self.end_game = False

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
                    if coord_bullets.row == 0 < coord_bullets.row < 10:
                        self.mMap.update_map(coord_bullets, TypeEnum.BULLET)
                    if coord_bullets.row < -1 or coord_bullets.row > 10:
                        bullet.kill()

            for enemy in sprite.groupcollide(self.mEnemiesSpriteGroup, self.mPlayerBulletsSpriteGroup, True, True):
                self.mMap.grid[enemy.row][enemy.column] = TypeEnum.EMPTY
                self.sounds["expl3"].play()
                self.score += enemy.value

            for bullet in sprite.groupcollide(self.mPlayerBulletsSpriteGroup, self.mEnemiesBulletsSpriteGroup, True,
                                              True):
                self.mMap.grid[bullet.row][bullet.row] = TypeEnum.EMPTY

            if sprite.spritecollide(self.mPlayer, self.mEnemiesSpriteGroup, False):
                self.end_game = True

            if sprite.spritecollide(self.mPlayer, self.mEnemiesBulletsSpriteGroup, False):
                if self.mPlayer.lives >= 0 >= self.mPlayer.invulnerability_frame:
                    self.mPlayer.invulnerability_frame = 240
                    self.sounds["shipexplosion"].play()
                    self.mPlayer.lives -= 1

                if self.mPlayer.lives <= 0:
                    self.sounds["shipexplosion"].play()
                    self.end_game = True
                    self.game_over = True

            if not self.mEnemiesSpriteGroup:
                self.end_game = True

            if len(self.mEnemiesSpriteGroup) <= 5 and self.shoot_time != 1500:
                self.shoot_time = 1500

            self.screen.blit(self.background_img, (0, 0))
            self.mAllSpritesGroup.draw(self.screen)

            self.draw_text(self.screen, "SCORE ", 25, self.mMap.tile_width, 10, WHITE)
            self.draw_text(self.screen, str(self.score), 25, self.mMap.tile_width * 2, 10, BLUE)

            self.draw_lives(self.images["player_life"], self.mPlayer.lives)


            display.update()
            display.flip()
