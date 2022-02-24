import numpy as np
import pygame

# Size (800 x 800 pixel map = 40 x 40 grid
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1000
BLOCK_NUM    = 40
BLOCK_SIZE   = 20

# Colors
GRID_COLOR     = (60, 60, 60)
BACK_COLOR     = (100, 100, 100)
PLAYER_1_COLOR = (100, 51, 0)
PLAYER_2_COLOR = (204, 0, 153)
PLAYER_3_COLOR = (0, 0, 255)
PLAYER_4_COLOR = (255, 255, 0)
LOW_COLOR      = (102, 200, 153)
MID_COLOR      = (0, 200, 0)
HIGH_COLOR     = (0, 80, 0)
WALL_COLOR     = (0, 0, 0)

# Number representations in the Game
COOLDOWN = -1 # Any negative number
EMPTY    =  0
LOW      =  1
MID      =  2
HIGH     =  3
PLAYER_1 =  4
PLAYER_2 =  5
PLAYER_3 =  6
PLAYER_4 =  7
WALL     =  9

# Convert Numbers to Colors
numTOcolor = {
    COOLDOWN: BACK_COLOR,
    EMPTY:    BACK_COLOR,
    LOW:      LOW_COLOR,
    MID:      MID_COLOR,
    HIGH:     HIGH_COLOR,
    PLAYER_1: PLAYER_1_COLOR,
    PLAYER_2: PLAYER_2_COLOR,
    PLAYER_3: PLAYER_3_COLOR,
    PLAYER_4: PLAYER_4_COLOR,
    WALL:     WALL_COLOR,
}

def main():
    global SCREEN, CLOCK
    run = True

    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("AdaptIO")
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BACK_COLOR)
    # Init game Class
    adaptIO = AdaptIO()

    # Draw static display elements
    adaptIO.drawGrid()
    adaptIO.drawScoreBoard()

    # Load map
    str_map = 'maps/base_field.txt'
    adaptIO.loadMap(str_map)
    print('Map loaded with shape of', adaptIO.map_original.shape)

    # Span players random
    adaptIO.spanPlayers()

    adaptIO.updateMap()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                print('AdaptIO is closed!')


        #update grid (firs player, second grown)
        """
        adaptIO.drawBlock(1, 1, HIGH_COLOR)
        adaptIO.drawBlock(1, 2, MID_COLOR)
        adaptIO.drawBlock(1, 3, LOW_COLOR)

        adaptIO.drawBlock(5, 1, PLAYER_1_COLOR)
        adaptIO.drawBlock(5, 2, PLAYER_2_COLOR)
        adaptIO.drawBlock(5, 3, PLAYER_3_COLOR)
        adaptIO.drawBlock(5, 4, PLAYER_4_COLOR)
        """

        pygame.display.update()

    pygame.quit()

class AdaptIO():
    """
    Contains the essential game elements.
    """
    def __init__(self):
        """
        Initialize AdaptIO class.
        """
        self.map_original = np.zeros([BLOCK_NUM, BLOCK_NUM])
        self.map_actual   = np.zeros([BLOCK_NUM, BLOCK_NUM])

    def loadMap(self, str_map):
        """
        Load the desired map.
        :param str_map: Path to the map file.
        """
        self.map_original = np.transpose(np.loadtxt(str_map))
        self.map_actual   = np.transpose(np.loadtxt(str_map))

    def updateMap(self):
        """
        Update the map grid by grid according to the map_actual.
        """
        for x in range(0, BLOCK_NUM):
            for y in range(0, BLOCK_NUM):
                rect = pygame.Rect(x * BLOCK_SIZE + 2, y * BLOCK_SIZE + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4)
                pygame.draw.rect(SCREEN, numTOcolor[self.map_actual[x,y]], rect, 0)

    def spanPlayers(self):
        """
        Span the players on the map
        """
        # Spaning positions
        span_1 = np.array([0 + 1        , 0 + 1])
        span_2 = np.array([BLOCK_NUM - 2, 0 + 1])
        span_3 = np.array([0 + 1        , BLOCK_NUM - 2])
        span_4 = np.array([BLOCK_NUM - 2, BLOCK_NUM - 2])

        span_points = np.random.permutation([span_1, span_2, span_3, span_4])
        players = [PLAYER_1, PLAYER_2, PLAYER_3, PLAYER_4]

        for i in range(len(players)):
            self.map_actual[span_points[i][0], span_points[i][1]] = players[i]

    def drawGrid(self):
            """
            Draw the grid pattern of the map.
            """
            blockSize = BLOCK_SIZE #Set the size of the grid block
            width     = BLOCK_NUM*BLOCK_SIZE
            height    = BLOCK_NUM*BLOCK_SIZE

            for x in range(0, width, blockSize):
                for y in range(0, height, blockSize):
                    rect = pygame.Rect(x, y, blockSize, blockSize)
                    pygame.draw.rect(SCREEN, GRID_COLOR, rect, 1)

    def drawScoreBoard(self):
            """
            Draw the scoreboard on the GUI.
            """
            rect = pygame.Rect(BLOCK_NUM*BLOCK_SIZE, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
            pygame.draw.rect(SCREEN, GRID_COLOR, rect, 0)

    def drawBlock(self, num_x, num_y, color):
            """
            Draw one element of the map with the desired color.
            :param num_x: Grid element number from the left.
            :param num_y: Grid element number from the top.
            :param color: Desired color.
            """
            rect = pygame.Rect(num_x*BLOCK_SIZE+2, num_y*BLOCK_SIZE+2, BLOCK_SIZE-4, BLOCK_SIZE-4)
            pygame.draw.rect(SCREEN, color, rect, 0)

# Run the GUI.
if __name__ == '__main__':
    print('AdaptIO is started!')
    main()
