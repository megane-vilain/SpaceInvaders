import sys, pygame
pygame.init()

size = width, height = 650, 600
speed = [2, 2]
black = 0, 0, 0
white = 255,255,255
speed = 12

screen = pygame.display.set_mode(size)

pygame.key.set_repeat(400, 30)
ship = pygame.image.load("space-invaders.png")
shiprect = ship.get_rect()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and shiprect.left > 0:
        	shiprect = shiprect.move(-speed,0)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and shiprect.right < width:
        	shiprect = shiprect.move(speed,0)

    # shiprect = shiprect.move(speed) 
    # if shiprect.left < 0 or shiprect.right > width:
    #     speed[0] = -speed[0]
    # if shiprect.top < 0 or shiprect.bottom > height:
    #     speed[1] = -speed[1]

    screen.fill(white)
    screen.blit(ship, shiprect)
    pygame.display.flip()