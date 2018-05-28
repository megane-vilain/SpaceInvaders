from Game import *
from pygame import *

# Colors
Black = 0, 0, 0
White = 255, 255, 255
RED = (255, 0, 0)

SCREEN = display.set_mode((900, 700))

mGame = Game(SCREEN)

mGame.add_enemies(4, mGame.images["enemy1"])
mGame.add_player(mGame.images["player_ship"])

mGame.main()

