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
    adaptIO.drawTick()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                print('AdaptIO is closed!')

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
        self.drawPlayerBoard(BLOCK_NUM * BLOCK_SIZE + 2, (5 * BLOCK_SIZE - 4)*0 + 2, PLAYER_1)
        self.drawPlayerBoard(BLOCK_NUM * BLOCK_SIZE + 2, (5 * BLOCK_SIZE - 4)*1 + 4, PLAYER_2)
        self.drawPlayerBoard(BLOCK_NUM * BLOCK_SIZE + 2, (5 * BLOCK_SIZE - 4)*2 + 6, PLAYER_3)
        self.drawPlayerBoard(BLOCK_NUM * BLOCK_SIZE + 2, (5 * BLOCK_SIZE - 4)*3 + 8, PLAYER_4)


    def drawBlock(self, num_x, num_y, color):
        """
        Draw one element of the map with the desired color.
        :param num_x: Grid element number from the left.
        :param num_y: Grid element number from the top.
        :param color: Desired color.
        """
        rect = pygame.Rect(num_x*BLOCK_SIZE+2, num_y*BLOCK_SIZE+2, BLOCK_SIZE-4, BLOCK_SIZE-4)
        pygame.draw.rect(SCREEN, color, rect, 0)

    def drawPlayerBoard(self, x, y, player):
        """
        Draw one Player Board with size and name texts.
        :param x: Top left corner x position
        :param y: Top left corner y position
        :param player: player number
        """
        width = WINDOW_WIDTH - (BLOCK_NUM * BLOCK_SIZE) - 8
        height = (5 * BLOCK_SIZE) - 8
        rect = pygame.Rect(x + 2, y + 2, width, height)
        pygame.draw.rect(SCREEN, BOARD_COLOR, rect, 0)
        flag = pygame.Rect(x+8, y+8, 20 , height - 12)
        pygame.draw.rect(SCREEN, numTOcolor[player], flag, 0)

        font = pygame.font.SysFont(None, 30)
        sttr = 'Player ' + str(player-3)
        text_player = font.render(sttr, True, TEXT_COLOR)
        text_name = font.render('#Name ', True, TEXT_COLOR)
        text_size = font.render('Size: ', True, TEXT_COLOR)
        SCREEN.blit(text_player, (x + 40, y + 8))
        SCREEN.blit(text_name,   (x + 50, y + 8 + 30))
        SCREEN.blit(text_size,   (x + 40, y + 8 + 60))

    def drawTick(self):
        font = pygame.font.SysFont(None, 40)
        text_tick_head = font.render('Tick Count', True, TEXT_COLOR)
        text_tick      = font.render('#Tick', True, TEXT_COLOR)
        SCREEN.blit(text_tick_head, (830, 540))
        SCREEN.blit(text_tick, (870, 600))

# Run the GUI.
if __name__ == '__main__':
    print('AdaptIO is started!')
    main()
