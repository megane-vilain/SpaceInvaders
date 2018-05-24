from Game import *
from pygame import *

# Colors
Black = 0, 0, 0
White = 255, 255, 255
RED = (255, 0, 0)

SCREEN = display.set_mode((900, 700))

Sound_dir = path.join(path.dirname(__file__), 'Sounds')

IMG_NAMES = ["player_ship", "player_life", "enemy1", "bullet"]
IMAGES = {name: image.load("Images/{}.ico".format(name)).convert_alpha()
          for name in IMG_NAMES}


mGame = Game(SCREEN)

mGame.add_enemies(8, IMAGES["enemy1"])
mGame.add_player(IMAGES["player_ship"])

mGame.main()

