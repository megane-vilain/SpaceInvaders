import sys, pygame
pygame.init()

size = width, height = 650, 600
black = 0, 0, 0
white = 255,255,255
speed = 12

pygame.key.set_repeat(400, 30)

screen = pygame.display.set_mode(size)
ship = pygame.image.load("space-invaders.png")


shiprect = ship.get_rect()
shiprect.y = 500
shiprect.x = 300

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and shiprect.left > 0:
            shiprect = shiprect.move(-speed,0)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and shiprect.right < width:
            shiprect = shiprect.move(speed,0)
		
		if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            pass
			#futur fonction de tir
		

    screen.fill(white)
    screen.blit(ship, shiprect)
    pygame.display.flip()