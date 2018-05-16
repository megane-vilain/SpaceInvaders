import sys, pygame, random, time
from os import path

#Variables
size = width, height = 900, 700
speed_move = 12
shoot_delay = 300
Fps = 60
running = True
Sound_dir = path.join(path.dirname(__file__),'Sounds')
Img_dir = path.join(path.dirname(__file__),'Images')

#pixel sizes for grid squares
TileWidth = 64                                
TileHeight = 64
TileMargin = 4
MapRow = 12 
MapColumn = 9


#Couleurs
Black = 0, 0, 0
White = 255,255,255
RED = (255, 0, 0)

#Initialisation pygame 
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Space Invaders')
pygame.mixer.music.load(path.join(Sound_dir,'main.wav'))
pygame.mixer.music.set_volume(0.05)
timer = pygame.time.get_ticks()
player_invulnerable_frames = 0

#Images
player_img = pygame.image.load(path.join(Img_dir,'ship.png'))
player_life_img = pygame.image.load(path.join(Img_dir, 'playerShip1_orange.png')).convert()
player_life_mini_img = pygame.transform.scale(player_life_img, (25, 19))
player_life_mini_img.set_colorkey(Black)
background_img = pygame.image.load(path.join(Img_dir,'space.jpg')).convert()
bullet_img = pygame.image.load(path.join(Img_dir,'bullet.png'))
ennemy_img = pygame.image.load(path.join(Img_dir, 'mysteryb.ico'))

#Musiques
bullet_sound = pygame.mixer.Sound(path.join(Sound_dir,'shoot.wav'))
bullet_sound.set_volume(0.1)
explosion_sound = pygame.mixer.Sound(path.join(Sound_dir,'expl3.wav'))

#Joue la musique du jeu en boucle
pygame.mixer.music.play(loops=-1)



#The main class for stationary things that inhabit the grid 
class MapTile(object):                       
	def __init__(self, Name, Column, Row):
		self.Name = Name
		self.Column = Column
		self.Row = Row

class ObjectBoard(pygame.sprite.Sprite):
	def __init__(self, image, collumn, row):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.left = (TileWidth * row + TileMargin)
		self.rect.top = (TileHeight * collumn + TileMargin)


class Player(ObjectBoard):
	def __init__(self, collumn, row):
		self.row = row
		self.collumn = collumn
		self.lives = 3
		super().__init__(player_img, self.collumn, self.row)
		
	def update(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT] or keys[pygame.K_q]:
			print(str(self.row))
			if self.row > 0:
				self.row = self.row -1
				print("Row : " + str(self.row))
				while self.rect.left != (TileWidth * (self.row ) + TileMargin):
					time.sleep(0.0050)
					self.rect.left =  self.rect.left - 4
					
		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			print("Droite")
			print(str(self.row))
			if self.row < 13:
				self.row = self.row +1
				print("Row : " + str(self.row))
				while self.rect.left != (TileWidth * (self.row ) + TileMargin):
					time.sleep(0.0050)
					self.rect.left =  self.rect.left + 4

class Ennemy(ObjectBoard):
	def __init__(self, collumn, row):
		self.row = row
		self.collumn = collumn
		super().__init__(ennemy_img, self.collumn, self.row)


class Map(object):
	global MapRow
	global MapColumn

	Grid = []

	# Creating grid
	for Row in range(MapRow):     
		Grid.append([])
		for Column in range(MapColumn):
			Grid[Row].append([])


Map = Map()
all_sprites = pygame.sprite.Group()
player = Player( 9, 6)
ennemey = Ennemy (0, 3) 
all_sprites.add(player)
all_sprites.add(ennemey)

#Boucle du jeu
while running:


	clock.tick(Fps) 
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()

	all_sprites.update()
	screen.blit(background_img, (0,0))
	all_sprites.draw(screen)
	pygame.display.flip()