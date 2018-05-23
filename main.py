import sys, pygame, random
from os import path

from Ennemy import *
from Player import *
from Map import *
from TypeEnum import *
from Game import *


# Couleurs
Black = 0, 0, 0
White = 255, 255, 255
RED = (255, 0, 0)


# Images
player_img = pygame.image.load(path.join(Img_dir, 'ship.png'))
player_life_img = pygame.image.load(path.join(Img_dir, 'playerShip1_orange.png')).convert()
player_life_mini_img = pygame.transform.scale(player_life_img, (25, 19))
player_life_mini_img.set_colorkey(Black)
background_img = pygame.image.load(path.join(Img_dir, 'space.jpg')).convert()
bullet_img = pygame.image.load(path.join(Img_dir, 'bullet.png'))
ennemy_img = pygame.image.load(path.join(Img_dir, 'mysteryb.ico'))

# Musiques
bullet_sound = pygame.mixer.Sound(path.join(Sound_dir, 'shoot.wav'))
bullet_sound.set_volume(0.1)
explosion_sound = pygame.mixer.Sound(path.join(Sound_dir, 'expl3.wav'))

# Joue la musique du jeu en boucle
pygame.mixer.music.play(loops=-1)


player_invulnerable_frames = 0

mMap = Map(9,12)

mAllSpritesGroup = pygame.sprite.Group()
mEnemiesSpriteGroup = pygame.sprite.Group()

mGame = Game()
mGame.addenemies(8, ennemy_img)


mPlayer = Player(9, 6, player_img)
mAllSpritesGroup.add(mPlayer)

# Boucle du jeu
while running:

    clock.tick(Fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    mAllSpritesGroup.update()
    screen.blit(background_img, (0, 0))
    mAllSpritesGroup.draw(screen)
    pygame.display.flip()


# def update(self):
# 	now = pygame.time.get_ticks()
# 	print("Row : " + str(self.row))
# 	if self.row <12 and self.row >= 2:
# 		# if self.row == 10:
# 		# 	self.speed = -1
# 		if  ((now - self.lastimemoved) > self.movedelay) :
# 			self.row += 1
# 			self.rect.left = (TileWidth * (self.row ) + TileMargin)
# 			self.lastimemoved = now