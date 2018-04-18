import sys, pygame, random
from os import path

class ObjectBoard(pygame.sprite.Sprite):
	def __init__(self, image):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.shoot_delay = shoot_delay
		self.last_shot = pygame.time.get_ticks()
		self.radius = int(self.rect.width * .85 / 2)

class Player(ObjectBoard):
	def __init__(self):
		super().__init__(player_img)
		self.rect.centerx = width / 2
		self.rect.bottom = height - 10
		self.lives = 3
		self.hidden = False
		self.hide_timer = pygame.time.get_ticks()
		

	def update(self):
		self.speedx = 0
		if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
			self.hidden = False
			self.rect.centerx = width / 2
			self.rect.bottom = height - 10
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speedx = -8
		if keystate[pygame.K_RIGHT]:
			self.speedx = 8
		self.rect.x += self.speedx
		if self.rect.right > width:
			self.rect.right = width
		if self.rect.left < 0:
			self.rect.left = 0

	def shoot(self):
		now = pygame.time.get_ticks()
		if now - self.last_shot > self.shoot_delay:
			self.last_shot = now
			bullet = Bullet(self.rect.centerx, self.rect.top,-10)
			all_sprites.add(bullet)
			bullets.add(bullet)
			bullet_sound.play()

	def hide(self):
		self.hidden = True
		self.hide_timer = pygame.time.get_ticks()
		self.rect.center = (width / 2, height + 200)

class Bullet(ObjectBoard):
	def __init__(self,centerx,y, speed_bullet):
		super().__init__(bullet_img)
		self.rect.bottom = y
		self.rect.centerx = centerx
		self.speedy = speed_bullet

	def update(self):
		self.rect.y += self.speedy
		screen.blit(bullet_img,(self.rect.x,self.rect.y))
		if self.rect.bottom < 0:
			self.kill()

class Ennemy(ObjectBoard):
	def __init__(self,x,y):
		super().__init__(ennemy_img)
		self.x = x
		self.y = y
		self.rect.x = x
		self.rect.y = y
		self.speedy = 1

	def update(self):
		self.rect.x  += self.speedy
		if self.rect.right > width:
			self.speedy = -self.speedy
			self.rect.x += self.speedy
			self.rect.y = self.rect.y + 50
		elif self.rect.left <=0:
			self.speedy = -self.speedy
			self.rect.x = self.speedy
			self.rect.y = self.rect.y + 50

	def shoot(self):
		now = pygame.time.get_ticks()
		if now - self.last_shot > self.shoot_delay:
			self.last_shot = now
			bullet = Bullet(self.rect.centerx, self.rect.bottom + 30,10)
			all_sprites.add(bullet)
			bullets.add(bullet)
			bullet_sound.play()

def draw_lives(surf, x, y ,lives, img):
	for i in range(lives):
		img_rect = img.get_rect()
		img_rect.x = x + 30 *i
		img_rect.y = y
		surf.blit(img, img_rect)

#Variables
size = width, height = 900, 700
speed_move = 12
shoot_delay = 300
Fps = 60
running = True
Sound_dir = path.join(path.dirname(__file__),'Sounds')
Img_dir = path.join(path.dirname(__file__),'Images')

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

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
ennemies = pygame.sprite.Group()

#Ajout du joeur
player = Player()
all_sprites.add(player)

#Ajout des ennemies
for i in range(10):
	ennemy = Ennemy(800/4+60*i,10)
	all_sprites.add(ennemy)
	ennemies.add(ennemy)

#Joue la musique du jeu en boucle
pygame.mixer.music.play(loops=-1)

#Boucle du jeu
while running:
	clock.tick(Fps) 
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		
		if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			player.shoot()

	all_sprites.update()

	if player_invulnerable_frames > 0:
		player_invulnerable_frames -= 1 

	ennemies_List = list(ennemies)
	random.shuffle(ennemies_List)
	for ennemy in ennemies_List:
		if (pygame.time.get_ticks() - timer) > 1000:
			ennemy.shoot()
			timer = pygame.time.get_ticks()


	# #Vérifie si un projectile touche un ennemi
	for ennemy in pygame.sprite.groupcollide(ennemies, bullets, True, True):
		explosion_sound.play()

	#Vérifie si un projectile touche le joeur
	if pygame.sprite.spritecollide(player, ennemies, False, pygame.sprite.collide_circle):
		player.hide()
		player.lives -= 1

		if player.lives == 0:
			running = False

	#Vérifie si le joueur est touché par une balle
	if pygame.sprite.spritecollide(player, bullets, False, pygame.sprite.collide_circle):
		if player_invulnerable_frames <=0 and player.lives != 0:
			player.lives -= 1
			player.hide()
			player_invulnerable_frames = 30

		if player.lives == 0:
			running = False
	#Quitte le jeu si il n'y a plus d'ennemies sur l'écran 
	if not ennemies:
		running = False

	screen.blit(background_img, (0,0))
	all_sprites.draw(screen)
	draw_lives(screen, width - 100, 5 , player.lives, player_life_mini_img)
	pygame.display.flip()