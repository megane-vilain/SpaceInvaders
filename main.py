from Game import *
from pygame import *

# Colors
Black = 0, 0, 0
White = 255, 255, 255
RED = (255, 0, 0)

SCREEN = display.set_mode((900, 700))

mGame = Game(SCREEN)


mGame.add_enemies(8,1, mGame.images["enemy1"])
mGame.add_enemies(8,2, mGame.images["enemy1"])
mGame.add_enemies(8,3, mGame.images["enemy1"])

mGame.add_player(mGame.images["player_ship"])

mGame.main()

quit()

