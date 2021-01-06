
from game import *
from grid import *
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    KEYUP,
    K_h,
    K_p,
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

pygame.init()
pygame.font.init()

def home_screen():
    screen.fill(WHITE)
    font = pygame.font.SysFont('Comic Sans MS', 24)
    title = font.render('PLAY THIS GAME!', True, ORANGE)
    font2 = pygame.font.SysFont('Comic Sans MS', 14)
    text = font2.render('Press any key to continue', True, ORANGE)
    screen.blit(title, (20, 20))
    screen.blit(text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

def gameOverScreen(screen):
    font = pygame.font.SysFont('Comic Sans MS', 32)
    text = font.render('GAME OVER', True, PURPLE)
    font2 = pygame.font.SysFont('Comic Sans MS', 16)
    text2 = font2.render("To return to the home screen, press 'h'. To play again, press the space bar", True, PURPLE)
    screen.blit(text, (100, 100))
    screen.blit(text2, (180, 200))

hasGameStarted = False
isGameOver = False

while True:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    grid = Grid(surface=screen, cellSize=24, marginSize=20)
    numPlayers = 2
    whoseTurn = 1
    strategy = [Player(grid, numPlayers, playerNum) for playerNum in range(1, numPlayers + 1)]
    SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 720
    RIGHT_BOUNDARY, BOTTOM_BOUNDARY = grid.cellSize * ((SCREEN_WIDTH - 2 *  GRID_MARGIN_SIZE) // grid.cellSize), grid.marginSize + ((SCREEN_HEIGHT // grid.cellSize - 2) - 1) * grid.cellSize
    inSameGame = True
    while inSameGame:
        pygame.display.flip()
        event_list = pygame.event.get()
        for event in event_list:
            if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
                pygame.quit()
                exit()
        if not hasGameStarted:
            home_screen()
            for event in event_list:
                if event.type == KEYDOWN:
                    hasGameStarted = True
        elif isGameOver:
            gameOverScreen(screen)
            for event in event_list:
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        isGameOver = False
                        inSameGame = False
                    elif event.key == K_h:
                        hasGameStarted = False
                        isGameOver = False
                        inSameGame = False
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
                            for player in strategy:
                                player.update(square)
                                if player.plays and player.plays[0].strength == 7:
                                    isGameOver = True
                                    break
                            whoseTurn = (whoseTurn % numPlayers) + 1
                if (event.type == KEYDOWN and event.key == K_p):
                    for player in strategy:
                        player.print_plays()

            screen.fill(WHITE)
            grid.draw()
