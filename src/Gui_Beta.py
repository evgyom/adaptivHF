import time
import numpy as np
import pygame
from threading import Thread
from Player import Player
from Config import *

# Convert Numbers to Colors
numTOcolor = {
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

def gui():
    # Teszt data
    # ====================================================
    # Players
    Player_1 = Player('BOB', 'naivebot', 1)
    Player_1.pos = (1,1)
    Player_2 = Player('ROB', 'naivebot', 1)
    Player_2.pos = (38, 1)
    Player_3 = Player('ZOD', 'naivebot', 1)
    Player_3.pos = (38, 38)
    Player_4 = Player('POO', 'naivebot', 1)
    Player_4.pos = (1, 38)
    # Player list
    players = [Player_1, Player_2, Player_3, Player_4]
    # Map load
    str_map = MAPPATH
    map = np.transpose(np.loadtxt(str_map))
    # Tick
    tick = 6
    # ====================================================

    # Init game Class
    adaptIO = AdaptIO()                            # init gui
    adaptIO.updateDisplayInfo(tick, players, map)  # update gui
    adaptIO.launch()                               # running loop

class AdaptIO():
    """
    Contains the essential game gui elements.
    """
    def __init__(self):
        """
        Initialize AdaptIO class.
        """
        pygame.init()

        self.run = True
        self.updated = True
        self.SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.CLOCK = pygame.time.Clock()
        pygame.display.set_caption("AdaptIO")
        self.SCREEN.fill(BACK_COLOR)

        # Draw static display elements
        self.drawGrid()

        self.tick = 0
        self.players = []
        self.map = []

        print('AdaptIO is started!')

    def updateDisplayInfo(self, tick, players, map):
        self.updated = True
        self.tick = tick
        self.map = map
        self.players = players

    def updateDisplay(self):
        self.updateTick()
        self.updateMap()
        self.updatePlayers()
        self.updateScoreBoard()

    def launch(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    print('AdaptIO is closed!')
            if self.updated:
                self.updateDisplay()
                self.updated = False
            pygame.display.update()
            self.CLOCK.tick(FPS)
        pygame.quit()

    def kill(self):
        self.run = False
        print('AdaptIO is closed!')
        pygame.quit()

    '''
    def loadMap(self, str_map):
        """
        Load the desired map.
        :param str_map: Path to the map file.
        """
        self.map_original = np.transpose(np.loadtxt(str_map))
        self.map_actual   = np.transpose(np.loadtxt(str_map))
    '''

    def updateMap(self):
        """
        Update the map grid by grid according to the map_actual.
        """
        for x in range(0, BLOCK_NUM):
            for y in range(0, BLOCK_NUM):
                rect = pygame.Rect(x * BLOCK_SIZE + 2, y * BLOCK_SIZE + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4)
                pygame.draw.rect(self.SCREEN, numTOcolor[self.map[x,y]], rect, 0)

    def spanPlayers(self):
        """
        Span the players on the map. (not needed here)
        """
        # Spaning positions
        span_1 = np.array([1        , 1])
        span_2 = np.array([BLOCK_NUM - 2, 1])
        span_3 = np.array([1        , BLOCK_NUM - 2])
        span_4 = np.array([BLOCK_NUM - 2, BLOCK_NUM - 2])

        span_points = np.random.permutation([span_1, span_2, span_3, span_4])
        players = [PLAYER_1, PLAYER_2, PLAYER_3, PLAYER_4]

        for i in range(len(players)):
            self.map_actual[span_points[i][0], span_points[i][1]] = players[i]

    def updatePlayers(self):
        for i in range(len(self.players)):
            x = self.players[i].pos[0]
            y = self.players[i].pos[1]
            rect = pygame.Rect(x * BLOCK_SIZE + 2, y * BLOCK_SIZE + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4)
            pygame.draw.rect(self.SCREEN, numTOcolor[i+3], rect, 0)

    def drawGrid(self):
        """
        Draw the grid pattern of the map. (static element)
        """
        blockSize = BLOCK_SIZE #Set the size of the grid block
        width     = BLOCK_NUM*BLOCK_SIZE
        height    = BLOCK_NUM*BLOCK_SIZE

        rect = pygame.Rect(BLOCK_NUM * BLOCK_SIZE, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(self.SCREEN, GRID_COLOR, rect, 0)

        for x in range(0, width, blockSize):
            for y in range(0, height, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(self.SCREEN, GRID_COLOR, rect, 1)

    def updateScoreBoard(self):
        """
        Draw the scoreboard on the GUI. (static element)
        """
        for i in range(0, len(self.players)):
            self.drawPlayerBoard(i, self.players[i].name, self.players[i].size)


    def drawBlock(self, num_x, num_y, color):
        """
        Draw one element of the map with the desired color.
        :param num_x: Grid element number from the left.
        :param num_y: Grid element number from the top.
        :param color: Desired color.
        """
        rect = pygame.Rect(num_x*BLOCK_SIZE+2, num_y*BLOCK_SIZE+2, BLOCK_SIZE-4, BLOCK_SIZE-4)
        pygame.draw.rect(self.SCREEN, color, rect, 0)

    def drawPlayerBoard(self, player_id, player_name, player_size):
        """
        Draw one Player Board with size and name texts.
        :param x: Top left corner x position
        :param y: Top left corner y position
        :param player_id: player number (1-4)
        :param player_name: name of the player
        :param player_size: size of the player
        """
        x = BLOCK_NUM * BLOCK_SIZE + 2
        y = (5 * BLOCK_SIZE - 4) * (player_id) + player_id * 2

        width = WINDOW_WIDTH - (BLOCK_NUM * BLOCK_SIZE) - 8
        height = (5 * BLOCK_SIZE) - 8
        rect = pygame.Rect(x + 2, y + 2, width, height)
        pygame.draw.rect(self.SCREEN, BOARD_COLOR, rect, 0)
        flag = pygame.Rect(x+8, y+8, 20 , height - 12)
        pygame.draw.rect(self.SCREEN, numTOcolor[player_id+3], flag, 0)

        font = pygame.font.SysFont(None, 30)
        sttr = 'Player ' + str(player_id)
        text_player = font.render(sttr, True, TEXT_COLOR)
        text_name = font.render(player_name, True, TEXT_COLOR)
        text_size = font.render(f'Size: {player_size}', True, TEXT_COLOR)
        self.SCREEN.blit(text_player, (x + 40, y + 8))
        self.SCREEN.blit(text_name,   (x + 50, y + 8 + 30))
        self.SCREEN.blit(text_size,   (x + 40, y + 8 + 60))

    def updateTick(self):
        font = pygame.font.SysFont(None, 40)
        text_tick = font.render(f'Tick: {self.tick}', True, TEXT_COLOR)
        self.SCREEN.blit(text_tick, (830, 420))

# Run the GUI.
if __name__ == '__main__':
    t = Thread(target=gui)
    t.start()
    time.sleep(10)
    t.join()