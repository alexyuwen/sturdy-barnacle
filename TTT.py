from game import *
from grid import *
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    QUIT,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    MOUSEMOTION,
)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (127, 0, 255)
GREEN = (0, 153, 0)
ORANGE = (255, 128, 0)

def home_screen():
    screen.fill(WHITE)

    font = pygame.font.SysFont('Comic Sans MS', 24)
    title = font.render('PLAY THIS GAME!', True, ORANGE)
    font2 = pygame.font.SysFont('Comic Sans MS', 14)
    text = font2.render('Press any key to continue', True, ORANGE)

    screen.blit(title, (20, 20))
    screen.blit(text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))


running = True
numPlayers = 2
whoseTurn = 1
hasGameStarted = False
isGameOver = False

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
grid = Grid(surface=screen, cellSize=24, marginSize = 20)
strategy = [Player(grid, numPlayers, playerNum) for playerNum in range(1, numPlayers + 1)]

RIGHT_BOUNDARY = grid.cellSize * ((SCREEN_WIDTH - 2 *  GRID_MARGIN_SIZE) // grid.cellSize)
BOTTOM_BOUNDARY = grid.marginSize + ((SCREEN_HEIGHT // grid.cellSize - 2) - 1) * grid.cellSize

while running:
    event_list = pygame.event.get()

    for event in event_list:
        if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
            running = False
    if not running:
        pygame.quit()
        break

    if not hasGameStarted:
        home_screen()
        for event in event_list:
            if event.type == KEYUP:
                hasGameStarted = True

    elif isGameOver:
        pass

    else:
        for event in event_list:
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if grid.marginSize < pos[0] < RIGHT_BOUNDARY and grid.marginSize < pos[1] < BOTTOM_BOUNDARY:
                    x = (pos[0] - grid.marginSize) // grid.cellSize
                    y = (pos[1] - grid.marginSize) // grid.cellSize
                    square = grid.grid[x][y]
                    if not square.isFilled:
                        coord = (x * grid.cellSize + grid.marginSize, y * grid.cellSize + grid.marginSize)
                        grid.shapes[whoseTurn - 1].add(coord)
                        square.isFilled = whoseTurn
                        strategy[whoseTurn - 1].update(square)
                        whoseTurn = (whoseTurn % numPlayers) + 1


        screen.fill(WHITE)
        grid.draw()

    pygame.display.flip()

for player in strategy:
    for play in player.plays:
        print(f"play = {play.play.coord}")
