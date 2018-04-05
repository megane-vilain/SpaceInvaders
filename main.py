import sys, pygame, random
from os import path

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.bottom = height - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
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
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        bullet_sound.play()

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        screen.blit(bullet_img,(self.rect.x,self.rect.y))
        if self.rect.bottom < 0:
            self.kill()

#Variables
size = width, height = 650, 600
speed = 12
Fps = 60
bullets=[]
Sound_dir = path.join(path.dirname(__file__),'Sounds')
Img_dir = path.join(path.dirname(__file__),'Images')

#Couleurs
Black = 0, 0, 0
White = 255,255,255

#Images
player_img = pygame.image.load(path.join(Img_dir,'ship.png'))
background_img = pygame.image.load(path.join(Img_dir,'space.jpg'))
bullet_img = pygame.image.load(path.join(Img_dir,'bullet.png'))

#Initialisation pygame 
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('background_img Invaders')
pygame.mixer.music.load(path.join(Sound_dir,'main.wav'))
pygame.mixer.music.set_volume(0.4)

#Musiques
bullet_sound = pygame.mixer.Sound(path.join(Sound_dir,'shoot.wav'))
bullet_sound.set_volume(0.05)

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)


pygame.mixer.music.play(loops=-1)
#Boucle du jeu
while 1:
    clock.tick(Fps) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.shoot()

    all_sprites.update()
    screen.blit(background_img, (0,0))
    all_sprites.draw(screen)
    pygame.display.flip()