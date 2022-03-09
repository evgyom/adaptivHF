# GameMaster
GAMEMASTER_NAME = "master"
IP = "localhost"
PORT = 42069
DEFAULT_TICK_LENGTH_S = 0.3
DISPLAY_ON = True

# Engine
MAPPATH          = "./maps/02_base.txt"
FIELDUPDATE_PATH = "./fieldupdate/01_corner.txt"
STARTING_SIZE    = 5
MIN_RATIO        = 1.1
STRATEGY_DICT    = {"Nata": "remoteplayer", "Teszt2": "naivehunterbot", "Teszt3": "naivehunterbot", "Teszt4": "naivehunterbot"}
VISION_RANGE     = 5
UPDATE_MODE      = "statistical" #static
DIFF_FROM_SIDE   = 1
FOODGEN_COOLDOWN = 10
FOODGEN_OFFSET   = 10
FOODGEN_SCALER = 0.3
MAXTICKS = 100
SOLO_ENABLED = True

#GUI
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1000
BLOCK_NUM    = 40
BLOCK_SIZE   = 20
FPS          = 40

# Colors
GRID_COLOR     = (60, 60, 60)
BACK_COLOR     = (100, 100, 100)
BOARD_COLOR    = (40, 40, 40)
TEXT_COLOR     = (180, 180, 180)
PLAYER_1_COLOR = (100, 51, 0)
PLAYER_2_COLOR = (204, 0, 153)
PLAYER_3_COLOR = (0, 0, 255)
PLAYER_4_COLOR = (255, 255, 0)
LOW_COLOR      = (102, 200, 153)
MID_COLOR      = (0, 200, 0)
HIGH_COLOR     = (0, 80, 0)
WALL_COLOR     = (0, 0, 0)
PLAYER_DEAD    = (255, 102, 102)

# Number representations in the Game
EMPTY    =  0
LOW      =  1
MID      =  2
HIGH     =  3
PLAYER_1 =  4
PLAYER_2 =  5
PLAYER_3 =  6
PLAYER_4 =  7
DEAD     =  8
WALL     =  9

